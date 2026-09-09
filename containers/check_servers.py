#!/usr/bin/env python3
"""Run one disposable, offline runtime container per built repository."""
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import uuid

from build_grammars import ROOT, USER, PODMAN, atomic_json


def check(image, jobs=2, names=None, artifacts=None):
    image_id = subprocess.check_output([*PODMAN, 'image', 'inspect', '--format={{.Id}}', image], text=True).strip()
    script = ROOT/'repo/containers/smoke_servers.py'
    script_hash = hashlib.sha256(script.read_bytes()).hexdigest()
    category = 'build-artifacts' if artifacts else 'servers'
    root = ROOT/'artifacts/runtime-checks'/category/(image_id[:12]+'-'+script_hash[:8]+'-'+uuid.uuid4().hex[:8])
    root.mkdir(parents=True, exist_ok=True)
    os.chown(root, USER.pw_uid, USER.pw_gid)
    shutil.copyfile(script, root/'smoke_servers.py')
    script = root/'smoke_servers.py'
    if hashlib.sha256(script.read_bytes()).hexdigest() != script_hash:
        raise RuntimeError('Probe changed while creating the run; retry with a stable script')
    if artifacts:
        artifacts = artifacts.resolve(strict=True)
        atomic_json(root/'catalog.json', [json.loads(p.read_text()) for p in sorted(artifacts.glob('*/build.json'))])
    else:
        export = 'corpus-catalog-'+uuid.uuid4().hex[:12]
        subprocess.run([*PODMAN, 'create', '--name='+export, '--network=none', image_id], check=True, stdout=subprocess.DEVNULL)
        try:
            subprocess.run([*PODMAN, 'cp', export+':/opt/corpus/server-catalog.json', str(root/'catalog.json')], check=True)
        finally: subprocess.run([*PODMAN, 'rm', export], check=True, stdout=subprocess.DEVNULL)
    rows = json.loads((root/'catalog.json').read_text())
    targets = [r['name'] for r in rows if r.get('artifact', {}).get('executables') and (not names or r['name'] in names)]
    if any(not re.fullmatch(r'[A-Za-z0-9_.+-]+', name) for name in targets): raise ValueError('Unsafe repository name')
    if not targets: raise ValueError('No selected runtime targets')

    def one(name):
        out = root/name
        out.mkdir(exist_ok=True)
        os.chown(out, USER.pw_uid, USER.pw_gid)
        project = 400000000+int(hashlib.sha256(str(out).encode()).hexdigest()[:7], 16)
        subprocess.run(['xfs_quota', '-x', '-c', f'project -s -p {out} {project}', '-c', f'limit -p bhard=100m {project}', str(ROOT)], check=True, capture_output=True)
        container = 'corpus-check-'+uuid.uuid4().hex[:12]
        command = [*PODMAN, 'run', '--rm', '--name='+container, '--pull=never', '--network=none',
            '--http-proxy=false', '--userns=keep-id', f'--user={USER.pw_uid}:{USER.pw_gid}',
            '--cap-drop=ALL', '--security-opt=no-new-privileges', '--read-only', '--read-only-tmpfs=false',
            '--memory=2g', '--memory-swap=2g', '--cpus=1', '--pids-limit=128', '--timeout=300',
            '--ulimit=core=0:0', '--log-driver=none',
            '--tmpfs=/work:rw,nosuid,nodev,size=512m,mode=1777',
            '--tmpfs=/tmp:rw,nosuid,nodev,size=256m,mode=1777',
            '--tmpfs=/dev/shm:rw,nosuid,nodev,noexec,size=32m,mode=1777',
            '-v', f'{script}:/input/smoke_servers.py:ro', '-v', f'{out}:/out:rw',
            *(['-v', f'{artifacts/name}:/opt/corpus/servers/{name}:ro'] if artifacts else []),
            '--entrypoint=python3', image_id, '/input/smoke_servers.py', name]
        code = None
        try:
            # Logs share the per-target disk quota. No unbounded capture_output.
            with (out/'stdout.jsonl').open('wb') as stdout, (out/'stderr.log').open('wb') as stderr:
                code = subprocess.run(command, stdout=stdout, stderr=stderr, timeout=330).returncode
        except subprocess.TimeoutExpired: code = 124
        finally: subprocess.run([*PODMAN, 'rm', '-f', container], capture_output=True)
        result = {'name': name, 'status': 'probe-process-failed', 'exit_code': code}
        path = out/'server-smoke.json'
        if code == 0 and path.is_file() and not path.is_symlink() and path.stat().st_size < 1024*1024:
            try:
                records = json.loads(path.read_text())
                if len(records) == 1 and records[0]['name'] == name: result.update(records[0])
            except (ValueError, TypeError, KeyError): pass
        print(json.dumps(result), flush=True)
        return result

    results = {}
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        futures = {pool.submit(one, name): name for name in targets}
        for future in as_completed(futures):
            name = futures[future]
            try: result = future.result()
            except Exception as error: result = {'name': name, 'status': 'supervisor-error', 'error': str(error)}
            results[name] = result
            atomic_json(root/'summary.json', {'image': image_id, 'probe_sha256': script_hash,
                'scope': 'build-artifacts' if artifacts else 'assembled-runtime',
                'complete': len(results) == len(targets), 'target_count': len(targets),
                'results': sorted(results.values(), key=lambda r:r['name'])})
    print(f'Runtime results: {root}/summary.json', flush=True)
    return results
