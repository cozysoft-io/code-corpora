#!/usr/bin/env python3
"""Resume the halted cloud batch, preserving completed artifacts and build caches."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shlex
import subprocess

ROOT = Path('/srv/corpus')
ARTIFACTS = ROOT/'artifacts'
PODMAN = ['sudo', '-u', 'corpus', '-H', 'env', 'XDG_RUNTIME_DIR=/run/user/1002', 'podman']


def read(path, default=None):
    return json.loads(path.read_text()) if path.is_file() else default


def recipe_hash(row):
    return hashlib.sha256(json.dumps(row, sort_keys=True).encode()).hexdigest()


def finished(row, any_recipe=False, successful_only=False):
    paths = [ROOT/'jobs'/('server-'+row['name'])/'result.json',
             ARTIFACTS/'servers'/row['name']/'build.json']
    for path in paths:
        result = read(path, {})
        if result.get('sha') != row['sha']:
            continue
        if not any_recipe and result.get('recipe_sha256') != recipe_hash(row):
            continue
        if result.get('status') == 'built-unverified':
            return True
        if not successful_only and result.get('status') == 'failed':
            return True
    return False


def saved_image(row, fallback):
    directory = ROOT/'jobs'/('server-'+row['name'])
    if read(directory/'job.json') == row and (directory/'work/source').is_dir():
        record = read(directory/'work-image.json', {})
        if record.get('image'):
            subprocess.run([*PODMAN, 'image', 'exists', record['image']], check=True)
            return record['image']
    return fallback


def main():
    os.chdir(ROOT)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--start', action='store_true', help='Launch the reviewed resume plan')
    args = parser.parse_args()
    queues = {name: read(ARTIFACTS/f'server-recipes-{name}.json')
              for name in ('remaining', 'repairs', 'more', 'jvm', 'heavy')}
    later = {row['name'] for name in ('repairs', 'more', 'jvm', 'heavy') for row in queues[name]}
    plan = {
        'main': [r for r in queues['remaining'] if r['name'] not in later and not finished(r, any_recipe=True)],
        'repairs': [r for r in queues['repairs'] if not finished(r)],
        'more': [r for r in queues['more'] if not finished(r, successful_only=True)],
        'jvm': [r for r in queues['jvm'] if not finished(r, successful_only=True)],
        'heavy': [r for r in queues['heavy'] if not finished(r, successful_only=True)],
    }
    # Buck2 already has a large interrupted Cargo cache in an older compatible SDK.
    plan['buck2'] = [r for r in plan['repairs'] if r['name'] == 'buck2']
    plan['repairs'] = [r for r in plan['repairs'] if r['name'] != 'buck2']
    print(json.dumps({name: [r['name'] for r in rows] for name, rows in plan.items()}, indent=2), flush=True)
    if not args.start:
        return
    active = subprocess.check_output(['systemctl', 'list-units', '--state=active', '--no-legend', '--plain', 'corpus-*'], text=True)
    if active.strip():
        raise RuntimeError('Refusing to overlap active corpus services: '+active)
    if subprocess.check_output([*PODMAN, 'ps', '--format={{.Names}}'], text=True).strip():
        raise RuntimeError('Refusing to overlap running containers')
    # Validate saved SDKs before starting any work.
    images = {name: saved_image(rows[0], 'localhost/code-corpora-build:expanded')
              for name, rows in plan.items() if name in ('heavy', 'buck2') and rows}
    for name, rows in plan.items():
        (ARTIFACTS/f'server-recipes-resume-{name}.json').write_text(json.dumps(rows, indent=2)+'\n')
    (ARTIFACTS/'resume-batch-plan.json').write_text(json.dumps(plan, indent=2)+'\n')
    (ARTIFACTS/'server-parallelism.json').write_text('{"jobs": 8}\n')
    # Restore idle shutdown after the explicit halt temporarily suppressed it.
    (ROOT/'keep-running').unlink(missing_ok=True)
    subprocess.run(['bash', str(ROOT/'repo/containers/restrict-build-network.sh')], check=True)

    def start(unit, command, waits=()):
        prefix = ''
        if waits:
            prefix = 'while '+ ' || '.join('systemctl is-active --quiet '+shlex.quote(w) for w in waits)+'; do sleep 10; done; '
        command = prefix+command+' >> '+shlex.quote('logs/'+unit+'-resumed.log')+' 2>&1'
        subprocess.run(['systemd-run', '--collect', '--unit='+unit, '--working-directory='+str(ROOT),
                        '/bin/bash', '-c', command], check=True)

    def build(name, image, jobs, dynamic=False):
        cmd = ['python3', 'repo/containers/build_servers.py', '--image', image,
               '--resume-work', '--jobs', str(jobs), '--recipes', f'server-recipes-resume-{name}.json',
               '--report', f'server-coverage-resume-{name}.json']
        if dynamic:
            cmd += ['--jobs-file', str(ARTIFACTS/'server-parallelism.json')]
        return shlex.join(cmd)

    for name in ('heavy', 'buck2'):
        if plan[name]:
            start('corpus-server-'+name, build(name, images[name], 1))
    if plan['main']:
        start('corpus-server-build', build('main', 'localhost/code-corpora-build:toolchains', 8, True))
    previous = None
    for name in ('repairs', 'more', 'jvm'):
        if plan[name]:
            unit = 'corpus-server-'+name
            start(unit, shlex.join(['bash', 'repo/containers/run-supplement.sh',
                  f'server-recipes-resume-{name}.json', f'server-coverage-resume-{name}.json']),
                  [previous] if previous else [])
            previous = unit
    start('corpus-finish-batch', 'bash repo/containers/finish-batch.sh')


if __name__ == '__main__':
    main()
