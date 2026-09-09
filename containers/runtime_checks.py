#!/usr/bin/env python3
"""Trusted host entry point for tests in the assembled runtime images."""
import argparse
import os
from pathlib import Path
import subprocess
from build_grammars import ROOT, USER, PODMAN

os.chdir(ROOT)
p = argparse.ArgumentParser()
p.add_argument('kind', choices=['grammars', 'servers'])
p.add_argument('--image')
p.add_argument('--name', action='append')
p.add_argument('--jobs', type=int, default=2)
p.add_argument('--artifacts', type=Path, help='Preliminary checks of read-only artifacts in a builder image; does not validate the final runtime')
args = p.parse_args()
image = args.image or f'localhost/code-corpora-{args.kind}:initial'
if args.kind == 'servers':
    from check_servers import check
    check(image, jobs=args.jobs, names=args.name, artifacts=args.artifacts)
    raise SystemExit(0)
out = ROOT/'artifacts/runtime-checks'/args.kind
out.mkdir(parents=True, exist_ok=True)
os.chown(out, USER.pw_uid, USER.pw_gid)
script = 'smoke_runtime.py' if args.kind == 'grammars' else 'smoke_servers.py'
project = 30000+(args.kind == 'servers')
subprocess.run(['xfs_quota', '-x', '-c', f'project -s -p {out} {project}', '-c', f'limit -p bhard=1g {project}', str(ROOT)], check=True)
command = [*PODMAN, 'run', '--rm', '--pull=never', '--network=none', '--http-proxy=false',
           '--userns=keep-id', f'--user={USER.pw_uid}:{USER.pw_gid}', '--cap-drop=ALL',
           '--security-opt=no-new-privileges', '--read-only', '--read-only-tmpfs=false',
           '--memory=4g', '--memory-swap=4g', '--cpus=2', '--pids-limit=256', '--timeout=1800',
           '--ulimit=core=0:0', '--log-driver=none', '--tmpfs=/work:rw,nosuid,nodev,size=1g,mode=1777',
           '--tmpfs=/tmp:rw,nosuid,nodev,size=256m,mode=1777', '-e', 'HOME=/work/home',
           '-v', f'{ROOT}/repo/containers:/input:ro', '-v', f'{out}:/out:rw',
           '--entrypoint=python3', image, '/input/'+script]
with (out/'stdout.json').open('w') as stdout, (out/'stderr.log').open('w') as stderr:
    result = subprocess.run(command, stdout=stdout, stderr=stderr)
print(f'{args.kind}: runtime check exited {result.returncode}; results in {out}')
raise SystemExit(result.returncode)
