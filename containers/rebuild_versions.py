#!/usr/bin/env python3
"""Update cloud checkouts and rebuild changed server pins using isolated batch workers."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess

from build_grammars import ROOT, PODMAN, atomic_json


def read(path, default=None):
    return json.loads(path.read_text()) if path.is_file() else default


def git(directory, *arguments):
    command = ['sudo', '-u', 'corpus', '-H', 'env', 'GIT_LFS_SKIP_SMUDGE=1',
               'GIT_TERMINAL_PROMPT=0', 'git', '-c', 'core.hooksPath=/dev/null',
               '-c', 'credential.helper=', '-C', str(directory), *arguments]
    result = subprocess.run(command, capture_output=True, text=True, timeout=600)
    if result.returncode:
        raise RuntimeError(result.stderr[-2000:])
    return result.stdout.strip()


def fetch_source(row):
    directory = ROOT/'repo/servers'/row['name']
    try:
        current = git(directory, 'rev-parse', 'HEAD')
        if current == row['sha']:
            return dict(row, source_status='ready')
        if current != row['previous_sha']:
            raise RuntimeError('Checkout moved independently: '+current)
        if git(directory, 'status', '--porcelain'):
            raise RuntimeError('Checkout has local changes; preserved')
        git(directory, 'fetch', '--no-tags', '--depth=1', row['url'], row['sha'])
        git(directory, 'checkout', '--detach', row['sha'])
        if git(directory, 'rev-parse', 'HEAD') != row['sha']:
            raise RuntimeError('Checkout pin mismatch')
        return dict(row, source_status='ready')
    except Exception as error:
        return dict(row, source_status='failed', source_error=str(error))


def version_recipe(row, recipe):
    recipe = dict(recipe, sha=row['sha'], url=row['url'])
    # Zabby's pinned release needs the Node agent, not the main Rust service.
    if row['name'] == 'tabby':
        recipe.update(kind='pnpm', package_manager='pnpm@9.15.9',
            before_prepare=[['python3', '-c',
                "from pathlib import Path; Path('pnpm-workspace.yaml').write_text('packages:\\n  - clients/tabby-agent\\n  - clients/tabby-openapi\\n')"]],
            before_build=[['pnpm', '--recursive', '--workspace-concurrency=2',
                           '--filter=tabby-agent...', 'run', 'build']],
            node_bins={'tabby-agent':'clients/tabby-agent/dist/node/index.js'})
        for key in ('cargo_packages', 'package', 'rust_toolchain', 'directory', 'script'):
            recipe.pop(key, None)
    return recipe


def prepare(plan, directory):
    previous = directory/'previous'
    previous.mkdir(exist_ok=True)
    for path in (ROOT/'artifacts').glob('server-*.json'):
        target = previous/path.name
        if not target.exists():
            shutil.copyfile(path, target)
    recipes = {}
    for filename in ('server-recipes.json', 'server-recipes-extra.json', 'server-recipes-next.json',
                     'server-recipes-monorepos.json', 'server-recipes-repairs.json',
                     'server-recipes-heavy.json', 'server-recipes-more.json',
                     'server-recipes-jvm.json', 'server-recipes-resumed-fixes.json'):
        for row in read(previous/filename, []):
            recipes[row['name']] = row
    pins = {row['name']:row['sha'] for row in plan['repositories']}
    for name, recipe in read(ROOT/'repo/containers/recipes.local-fixes.json', {}).items():
        if recipe['sha'] == pins.get(name):
            recipes[name] = recipe
    changed = [row for row in plan['repositories'] if row['changed']]
    source_results = {}
    with ThreadPoolExecutor(max_workers=6) as pool:
        for future in as_completed([pool.submit(fetch_source, row) for row in changed]):
            row = future.result()
            source_results[row['name']] = row
            atomic_json(directory/'sources.json', sorted(source_results.values(), key=lambda r:r['name']))
            print(json.dumps({'name':row['name'], 'source_status':row['source_status'],
                              'error':row.get('source_error')}), flush=True)
    # Regenerate basic recipes against the new source layouts, then apply reviewed
    # target-specific recipes. Old reports are retained in this run's snapshot.
    subprocess.run(['python3', 'repo/containers/inventory_servers.py'], check=True)
    subprocess.run(['python3', 'repo/containers/plan_servers.py'], check=True)
    basic = {row['name']:row for row in read(ROOT/'artifacts/server-recipes.json', [])}
    basic_coverage = {row['name']:row for row in read(ROOT/'artifacts/server-coverage.json', [])}
    queues = {'regular':[], 'heavy':[]}
    coverage = []
    for row in changed:
        source = source_results[row['name']]
        cached = ROOT/'artifacts/servers'/row['name']
        prior_build = read(cached/'build.json', {})
        if prior_build and prior_build.get('sha') != row['sha']:
            archived = directory/'artifacts'/row['name']/prior_build['sha']
            archived.parent.mkdir(parents=True, exist_ok=True)
            if archived.exists():
                raise RuntimeError('Prior artifact archive already exists: '+str(archived))
            shutil.move(cached, archived)
        job_directory = ROOT/'jobs'/('server-'+row['name'])
        for filename in ('job.json', 'result.json', 'prepare.log', 'build.log'):
            path = job_directory/filename
            if path.is_file():
                target = previous/'jobs'/row['name']/filename
                target.parent.mkdir(parents=True, exist_ok=True)
                if not target.exists():
                    shutil.copyfile(path, target)
        recipe = recipes.get(row['name'], basic.get(row['name']))
        if source['source_status'] != 'ready' or not recipe:
            status = 'source-failed' if source['source_status'] != 'ready' else basic_coverage[row['name']]['status']
            coverage.append(dict(row, status=status,
                                 source_error=source.get('source_error'), previously_built=bool(prior_build)))
            continue
        recipe = version_recipe(row, recipe)
        category = 'heavy' if row['name'] == 'llvm-project' else 'regular'
        queues[category].append(recipe)
        coverage.append(dict(row, status='pending', previously_built=bool(prior_build)))
    for category, rows in queues.items():
        atomic_json(directory/(category+'.json'), rows)
    atomic_json(directory/'coverage.json', coverage)
    atomic_json(ROOT/'artifacts/version-rebuild-current.json', {'directory':str(directory),
                'changed':len(changed), 'queued':sum(map(len, queues.values())),
                'blocked':[r for r in coverage if r['status']!='pending']})
    print(json.dumps({'queues':{name:len(rows) for name,rows in queues.items()},
                      'blocked':[r['name'] for r in coverage if r['status']!='pending']}), flush=True)


def start(directory):
    coverage = read(directory/'coverage.json', [])
    missing = [row['name'] for row in coverage if row['previously_built'] and row['status'] != 'pending']
    if missing:
        raise RuntimeError('Previously built servers missing rebuild recipes: '+', '.join(missing))
    image = 'localhost/code-corpora-build:compat'
    subprocess.run([*PODMAN, 'image', 'exists', image], check=True)
    heavy = read(directory/'heavy.json', [])
    regular = read(directory/'regular.json', [])
    for category, rows in [('heavy',heavy), ('regular',regular)]:
        if not rows:
            continue
        filename = str((directory/(category+'.json')).relative_to(ROOT/'artifacts'))
        report = str((directory/(category+'-coverage.json')).relative_to(ROOT/'artifacts'))
        if not (directory/(category+'-coverage.json')).exists():
            shutil.copyfile(directory/'coverage.json', directory/(category+'-coverage.json'))
        command = ['python3', 'repo/containers/build_servers.py', '--image', image,
                   '--jobs', '1' if category=='heavy' else ('4' if heavy else '8'),
                   '--recipes', filename, '--report', report, '--resume-work']
        if category == 'regular':
            limits = directory/'parallelism.json'
            atomic_json(limits, {'jobs':4 if heavy else 8})
            command += ['--jobs-file',str(limits)]
        subprocess.run(['systemd-run', '--collect', '--unit=corpus-server-versions-'+category,
                        '--working-directory='+str(ROOT), '--property=StandardOutput=append:'+str(directory/(category+'.log')),
                        '--property=StandardError=append:'+str(directory/(category+'.log')), *command], check=True)
    # Raise ordinary concurrency once LLVM releases its eight CPUs.
    if heavy and regular:
        subprocess.run(['systemd-run', '--collect', '--unit=corpus-versions-parallelism',
                        '--working-directory='+str(ROOT), 'python3', str(Path(__file__).resolve()),
                        '--release-cpus'], check=True)
    subprocess.run(['systemd-run', '--collect', '--unit=corpus-finish-versions',
                    '--working-directory='+str(ROOT),
                    '--property=StandardOutput=append:'+str(directory/'finish.log'),
                    '--property=StandardError=append:'+str(directory/'finish.log'),
                    'bash', 'repo/containers/finish-batch.sh', 'versions-'+directory.name], check=True)
    (ROOT/'keep-running').unlink(missing_ok=True)


def main():
    os.chdir(ROOT)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prepare', action='store_true')
    parser.add_argument('--start', action='store_true')
    parser.add_argument('--release-cpus', action='store_true')
    arguments = parser.parse_args()
    plan_path = ROOT/'repo/server-releases.json'
    directory = ROOT/'artifacts/version-rebuilds'/hashlib.sha256(plan_path.read_bytes()).hexdigest()[:12]
    directory.mkdir(parents=True, exist_ok=True)
    if arguments.release_cpus:
        import time
        while subprocess.run(['systemctl','is-active','--quiet','corpus-server-versions-heavy']).returncode==0:
            time.sleep(15)
        atomic_json(directory/'parallelism.json', {'jobs':8})
        return
    (ROOT/'keep-running').touch()
    if subprocess.check_output([*PODMAN, 'ps', '--format={{.Names}}'], text=True).strip():
        raise RuntimeError('Pause all existing containers first')
    if arguments.prepare:
        prepare(read(plan_path), directory)
    if arguments.start:
        start(directory)
    print(directory)


if __name__ == '__main__':
    main()
