#!/usr/bin/env python3
"""Trusted supervisor for separate online-prepare/offline-build containers."""
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import time

from build_grammars import ROOT, USER, PODMAN, atomic_json


def phase(directory, job, image, phase_name):
    name = 'corpus-server-'+job['name']+'-'+phase_name
    command = [*PODMAN, 'run', '--rm', '--name='+name, '--pull=never',
        '--network='+('slirp4netns:allow_host_loopback=false' if phase_name == 'prepare' else 'none'),
        '--http-proxy=false', '--userns=keep-id', f'--user={USER.pw_uid}:{USER.pw_gid}',
        '--cap-drop=ALL', '--security-opt=no-new-privileges', '--read-only',
        '--read-only-tmpfs=false', '--pids-limit=512', '--memory='+job.get('memory', '10g'),
        '--memory-swap='+job.get('memory', '10g'), '--cpus='+str(job.get('cpus', 2)),
        '--timeout='+str(job.get(phase_name+'_timeout', 900 if phase_name == 'prepare' else 3600)),
        '--ulimit=core=0:0', '--log-driver=none',
        '--tmpfs=/tmp:rw,nosuid,nodev,size=1g,mode=1777',
        '--tmpfs=/dev/shm:rw,nosuid,nodev,noexec,size=64m,mode=1777',
        '-v', f'{ROOT}/repo/servers/{job["name"]}:/input/source:ro',
        '-v', f'{directory}/worker.py:/input/worker.py:ro',
        '-v', f'{directory}/job.json:/input/job.json:ro',
        '-v', f'{directory}/work:/work:rw', '-v', f'{directory}/out:/out:rw',
        '-v', f'{directory}/out:/opt/corpus/servers/{job["name"]}:rw',
        '-e', 'HOME=/work/home', '--entrypoint=python3', image, '/input/worker.py', phase_name]
    with (directory/(phase_name+'.log')).open('wb') as log:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        count = 0
        try:
            while data := process.stdout.read1(65536):
                if count < 8*1024*1024:
                    log.write(data[:8*1024*1024-count])
                    log.flush()
                count += len(data)
            return process.wait()
        finally: subprocess.run([*PODMAN, 'rm', '-f', name], capture_output=True)


def build(index, job, image, resume_work=False):
    locks = ROOT/'jobs/.locks'
    locks.mkdir(exist_ok=True)
    with (locks/(job['name']+'.lock')).open('w') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        try:
            return build_locked(index, job, image, resume_work)
        except Exception as error:
            # Keep supervisor failures visible alongside compiler failures.
            # The target lock is still held, so this cannot overwrite a live peer.
            directory = ROOT/'jobs'/('server-'+job['name'])
            directory.mkdir(parents=True, exist_ok=True)
            result = dict(job, image=image, status='failed', phase='supervisor', error=str(error))
            atomic_json(directory/'result.json', result)
            print(json.dumps({'name': job['name'], 'status': 'failed', 'error': str(error)[:1000]}), flush=True)
            return result


def build_locked(index, job, image, resume_work):
    worker_hash = hashlib.sha256((ROOT/'repo/containers/server_worker.py').read_bytes()).hexdigest()
    recipe_hash = hashlib.sha256(json.dumps(job, sort_keys=True).encode()).hexdigest()
    if shutil.disk_usage(ROOT).free < 40*1024**3: raise RuntimeError('Less than 40 GiB disk headroom')
    directory = ROOT/'jobs'/('server-'+job['name'])
    cached = ROOT/'artifacts/servers'/job['name']
    if (cached/'build.json').is_file():
        record = json.loads((cached/'build.json').read_text())
        if record.get('image') == image and record['sha'] == job['sha'] and record.get('worker_sha256') == worker_hash and record.get('recipe_sha256') == recipe_hash: return record
    for stage in ('prepare', 'build'):
        if subprocess.run([*PODMAN, 'container', 'exists', 'corpus-server-'+job['name']+'-'+stage], capture_output=True).returncode == 0:
            raise RuntimeError('A container already exists for '+job['name'])
    resumable = False
    if resume_work and (directory/'job.json').is_file() and (directory/'work/source').is_dir() and (directory/'work-image.json').is_file():
        prior = json.loads((directory/'job.json').read_text())
        resumable = prior == job and json.loads((directory/'work-image.json').read_text())['image'] == image
    if directory.exists() and not resumable: shutil.rmtree(directory)
    directory.mkdir(parents=True, exist_ok=True)
    if resumable and (directory/'out').exists(): shutil.rmtree(directory/'out')
    for name in ('work', 'out'):
        (directory/name).mkdir(exist_ok=True)
        os.chown(directory/name, USER.pw_uid, USER.pw_gid)
    atomic_json(directory/'job.json', job)
    atomic_json(directory/'work-image.json', {'image': image})
    shutil.copyfile(ROOT/'repo/containers/server_worker.py', directory/'worker.py')
    # Independent recipe queues must not share a quota just because their row
    # indices happen to match. Stable IDs also survive recipe reordering.
    project = 100000+int(hashlib.sha256(job['name'].encode()).hexdigest()[:7], 16)
    subprocess.run(['xfs_quota', '-x', '-c', f'project -s -p {directory} {project}', '-c', f'limit -p bhard=24g {project}', str(ROOT)], check=True, capture_output=True)
    start = time.monotonic()
    for stage in ('prepare', 'build'):
        code = phase(directory, job, image, stage)
        if code: break
    result = dict(job, image=image, worker_sha256=worker_hash, recipe_sha256=recipe_hash, status='built-unverified' if code == 0 else 'failed',
                  phase=stage, exit_code=code, seconds=round(time.monotonic()-start, 2),
                  log=str(directory/(stage+'.log')))
    if code == 0:
        # Validate before moving results. No upstream files are executed by this host.
        output = directory/'out'
        for path in output.rglob('*'):
            if path.is_symlink():
                if not path.resolve().is_relative_to(output): raise ValueError(f'Escaping output link: {path}')
            elif not (path.is_file() or path.is_dir()): raise ValueError(f'Special output file: {path}')
        if cached.exists(): shutil.rmtree(cached)
        cached.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(output, cached)
        result['artifact'] = json.loads((cached/'artifact.json').read_text())
        atomic_json(cached/'build.json', result)
    atomic_json(directory/'result.json', result)
    # Build caches are retained for debugging/offline dependency snapshot assembly.
    # Remove bulky disposable compilation intermediates; keep downloaded packages.
    for path in (directory/'work/source'/job.get('directory', '')/'target', directory/'work/gocache', directory/'work/tmp'):
        if path.is_dir() and not path.is_symlink() and path.resolve().is_relative_to(directory/'work'):
            shutil.rmtree(path)
    print(json.dumps({k: result[k] for k in ('name', 'status', 'phase', 'seconds')}), flush=True)
    return result


def main():
    os.chdir(ROOT)
    subprocess.run(['bash', str(ROOT/'repo/containers/restrict-build-network.sh')], check=True)
    p = argparse.ArgumentParser()
    p.add_argument('--image', required=True)
    p.add_argument('--jobs', type=int, default=3)
    p.add_argument('--jobs-file', type=Path, help='Optional JSON object with live jobs limit (1..16)')
    p.add_argument('--resume-work', action='store_true', help='Reuse work only when the complete saved recipe matches')
    p.add_argument('--name', action='append')
    p.add_argument('--report', default='server-coverage.json')
    p.add_argument('--recipes', default='server-recipes.json')
    args = p.parse_args()
    if not 1 <= args.jobs <= 16: p.error('--jobs must be between 1 and 16')
    image = subprocess.check_output([*PODMAN, 'image', 'inspect', '--format={{.Id}}', args.image], text=True).strip()
    rows = json.loads((ROOT/'artifacts'/args.recipes).read_text())
    path = ROOT/'artifacts'/args.report
    baseline = path if path.exists() else ROOT/'artifacts/server-coverage.json'
    catalog = {r['name']: r for r in json.loads(baseline.read_text())}
    pending = iter(enumerate(r for r in rows if not args.name or r['name'] in args.name))
    exhausted = False
    with ThreadPoolExecutor(max_workers=16) as pool:
        futures = {}
        while futures or not exhausted:
            limit = args.jobs
            if args.jobs_file and args.jobs_file.exists():
                limit = int(json.loads(args.jobs_file.read_text())['jobs'])
                if not 1 <= limit <= 16: raise ValueError('Live jobs limit must be between 1 and 16')
            while not exhausted and len(futures) < limit:
                item = next(pending, None)
                if item is None:
                    exhausted = True
                    break
                n, row = item
                futures[pool.submit(build, n, row, image, args.resume_work)] = row
            finished, _ = wait(futures, timeout=5, return_when=FIRST_COMPLETED)
            for future in finished:
                row = futures.pop(future)
                try: result = future.result()
                except Exception as error: result = dict(row, status='failed', error=str(error))
                catalog[row['name']] = result
                atomic_json(path, sorted(catalog.values(), key=lambda r: r['name']))


if __name__ == '__main__': main()
