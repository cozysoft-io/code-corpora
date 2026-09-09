#!/usr/bin/env python3
"""Trusted root supervisor; target compilers run in rootless offline containers."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
import os
from pathlib import Path
import pwd
import shutil
import subprocess
import time

ROOT = Path('/srv/corpus')
USER = pwd.getpwnam('corpus')
PODMAN = ['sudo', '-u', 'corpus', '-H', 'env', f'XDG_RUNTIME_DIR=/run/user/{USER.pw_uid}', 'podman']


def atomic_json(path, value):
    temp = path.with_suffix('.tmp')
    temp.write_text(json.dumps(value, indent=2)+'\n')
    temp.replace(path)


def build(index, job, image):
    worker_hash = hashlib.sha256((ROOT/'repo/containers/worker.py').read_bytes()).hexdigest()
    name = job['name']
    directory = ROOT/'jobs'/('grammar-'+name)
    if job['status'] != 'staged': return job
    cached = ROOT/'artifacts/grammars'/name
    if (cached/'build.json').exists():
        record = json.loads((cached/'build.json').read_text())
        if record.get('image') == image and record.get('sha') == job['sha'] and record.get('worker_sha256') == worker_hash:
            return record
    # Delete only our own previous job workspace, after confirming no active container.
    cname = 'corpus-grammar-'+name
    inspect = subprocess.run([*PODMAN, 'container', 'exists', cname], capture_output=True)
    if inspect.returncode == 0: raise RuntimeError(f'Container still exists: {cname}')
    if directory.exists(): shutil.rmtree(directory)
    directory.mkdir(parents=True)
    for d in ('out', 'work'):
        path = directory/d
        path.mkdir()
        os.chown(path, USER.pw_uid, USER.pw_gid)
    atomic_json(directory/'job.json', job)
    # XFS project quotas bound each complete job's scratch, output, and logs.
    project = 10000+index
    subprocess.run(['xfs_quota', '-x', '-c', f'project -s -p {directory} {project}', str(ROOT)], check=True, capture_output=True)
    subprocess.run(['xfs_quota', '-x', '-c', f'limit -p bhard=4g {project}', str(ROOT)], check=True, capture_output=True)
    command = [*PODMAN, 'run', '--rm', '--name='+cname, '--pull=never',
        '--network=none', '--http-proxy=false', '--userns=keep-id',
        f'--user={USER.pw_uid}:{USER.pw_gid}', '--cap-drop=ALL',
        '--security-opt=no-new-privileges', '--read-only', '--read-only-tmpfs=false',
        '--pids-limit=256', '--memory=8g', '--memory-swap=8g', '--cpus=2',
        '--timeout=600', '--ulimit=core=0:0', '--log-driver=none',
        '--tmpfs=/tmp:rw,nosuid,nodev,noexec,size=256m,mode=1777',
        '-v', f'{ROOT}/repo/grammars/{name}:/input/source:ro',
        '-v', f'{directory}/job.json:/input/job.json:ro',
        '-v', f'{ROOT}/repo/containers/worker.py:/opt/corpus/worker.py:ro',
        '-v', f'{directory}/work:/work:rw', '-v', f'{directory}/out:/out:rw',
        '-e', 'HOME=/work/home', '-e', 'XDG_CACHE_HOME=/work/cache',
        image, 'build-grammar', '/input/job.json']
    started = time.monotonic()
    try:
        with (directory/'build.log').open('wb') as log:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            count = 0
            while data := process.stdout.read(65536):
                if count < 4*1024*1024:
                    log.write(data[:4*1024*1024-count])
                count += len(data)
            code = process.wait()
    finally:
        subprocess.run([*PODMAN, 'rm', '-f', cname], capture_output=True)
    result = dict(job, status='built' if code == 0 else 'failed', image=image,
                  worker_sha256=worker_hash,
                  exit_code=code, seconds=round(time.monotonic()-started, 2),
                  log=str(directory/'build.log'))
    if code == 0:
        # Only copy regular bounded files, never workload-created links.
        files = list((directory/'out').iterdir())
        for file in files:
            if file.is_symlink() or not file.is_file() or file.stat().st_size > 256*1024*1024:
                raise ValueError(f'Unexpected output: {file}')
        if cached.exists(): shutil.rmtree(cached)
        cached.mkdir(parents=True)
        for file in files: shutil.copyfile(file, cached/file.name)
        result['artifact'] = json.loads((cached/'artifact.json').read_text())
        result['sha256'] = hashlib.sha256((cached/'parser.so').read_bytes()).hexdigest()
        atomic_json(cached/'build.json', result)
    atomic_json(directory/'result.json', result)
    print(json.dumps({k: result[k] for k in ('name', 'status', 'seconds')}), flush=True)
    return result


def main():
    os.chdir(ROOT)
    p = argparse.ArgumentParser()
    p.add_argument('--image', required=True)
    p.add_argument('--jobs', type=int, default=6)
    p.add_argument('--name', action='append')
    args = p.parse_args()
    image = subprocess.check_output([*PODMAN, 'image', 'inspect', '--format={{.Id}}', args.image], text=True).strip()
    rows = json.loads((ROOT/'repo/grammar-inputs.json').read_text())
    catalog = {}
    path = ROOT/'artifacts/grammar-catalog.json'
    if path.exists(): catalog = {r['name']: r for r in json.loads(path.read_text())}
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures = {pool.submit(build, n, r, image): r for n, r in enumerate(rows) if not args.name or r['name'] in args.name}
        for future in as_completed(futures):
            row = futures[future]
            try: result = future.result()
            except Exception as error: result = dict(row, status='failed', error=str(error))
            catalog[row['name']] = result
            atomic_json(path, sorted(catalog.values(), key=lambda r: r['name']))


if __name__ == '__main__': main()
