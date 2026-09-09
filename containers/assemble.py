#!/usr/bin/env python3
"""Assemble aggregate runtime images from validated, completed artifacts."""
import argparse
import json
import os
import re
import shlex
from collections import defaultdict
from pathlib import Path
import shutil
import subprocess
import tomllib
from build_grammars import ROOT, USER, PODMAN, atomic_json
from runtime_layers import stage_layers


def call(args):
    subprocess.run(args, check=True)


def check_server_pin(record, selection):
    expected = selection.get(record['name'])
    if not expected or record.get('sha') != expected['sha']:
        raise ValueError('Artifact does not match selected server commit: '+record['name'])


def main():
    os.chdir(ROOT)
    p = argparse.ArgumentParser()
    p.add_argument('kind', choices=['grammars', 'servers'])
    p.add_argument('--tag', default='initial')
    p.add_argument('--builder', default='localhost/code-corpora-build:toolchains')
    p.add_argument('--grammar-image', default='localhost/code-corpora-grammars:initial')
    args = p.parse_args()
    context = ROOT/'images'/args.kind
    context.mkdir(parents=True, exist_ok=True)
    os.chown(context, USER.pw_uid, USER.pw_gid)
    if args.kind == 'grammars':
        source = ROOT/'artifacts/grammars'
        if (context/'grammars').exists(): shutil.rmtree(context/'grammars')
        shutil.copytree(source, context/'grammars')
        rows = json.loads((ROOT/'artifacts/grammar-catalog.json').read_text())
        quarantine = context/'quarantine'
        if quarantine.exists(): shutil.rmtree(quarantine)
        quarantine.mkdir()
        for row in rows:
            failed = ROOT/'jobs'/('grammar-'+row['name'])/'out'
            if row['status'] == 'failed' and (failed/'artifact.json').is_file() and (failed/'parser.so').is_file():
                dest = quarantine/row['name']
                dest.mkdir()
                for name in ('artifact.json', 'parser.so'):
                    if (failed/name).is_symlink(): raise ValueError('Invalid quarantined output')
                    shutil.copyfile(failed/name, dest/name)
                row['status'] = 'quarantined-smoke-failure'
                row['quarantine_path'] = '/opt/corpus/quarantine/grammars/'+row['name']
        atomic_json(context/'grammar-catalog.json', rows)
        base = (ROOT/'artifacts/base-image.txt').read_text().strip()
        build_args = ['--build-arg', 'BASE_IMAGE='+base]
        export_paths = ['python']
    else:
        selection = {row['name']: row for row in tomllib.loads(
            (ROOT/'repo/selected-servers.toml').read_text())['repo']}
        if (context/'servers').exists(): shutil.rmtree(context/'servers')
        shutil.copytree(ROOT/'artifacts/servers', context/'servers', symlinks=True)
        rows = {r['name']: r for r in json.loads((ROOT/'artifacts/server-coverage.json').read_text())}
        # Earlier supervisors recorded exceptions only in queue reports.
        for report in sorted((ROOT/'artifacts').glob('server-coverage*.json'), key=lambda p:p.stat().st_mtime):
            for row in json.loads(report.read_text()):
                if row.get('error') and row.get('status') == 'failed':
                    rows[row['name']] = row
        for path in (ROOT/'jobs').glob('server-*/result.json'):
            row = json.loads(path.read_text())
            rows[row['name']] = row
        current = ROOT/'artifacts/version-rebuild-current.json'
        if current.is_file():
            coverage = Path(json.loads(current.read_text())['directory'])/'coverage.json'
            for row in json.loads(coverage.read_text()):
                if rows.get(row['name'], {}).get('sha') != row['sha']:
                    rows[row['name']] = row
        rows = {name: rows.get(name, dict(selected, status='needs-rebuild'))
                for name, selected in selection.items()}
        for name, row in list(rows.items()):
            if row.get('sha') != selection[name]['sha']:
                rows[name] = dict(selection[name], status='needs-rebuild', previous_sha=row.get('sha'))
        # Builds may finish while staging this snapshot. Describe exactly the
        # distributions copied into the context, not newer host-side results.
        for row in rows.values():
            if row.get('artifact'):
                row.pop('artifact')
                row['status'] = 'not-in-this-snapshot'
        for directory in (context/'servers').iterdir():
            record = directory/'build.json'
            if record.is_file():
                row = json.loads(record.read_text())
                check_server_pin(row, selection)
                rows[row['name']] = row
            else:
                raise ValueError('Missing server build record: '+str(directory))
        atomic_json(context/'server-catalog.json', sorted(rows.values(), key=lambda r:r['name']))
        # Unique command names let servers find other installed servers (e.g. templ -> gopls).
        commands = defaultdict(list)
        for directory in (context/'servers').iterdir():
            manifest = directory/'artifact.json'
            if not manifest.is_file(): continue
            for entry in json.loads(manifest.read_text())['executables']:
                name = entry['name']
                if not re.fullmatch(r'[A-Za-z0-9_.+-]+', name): raise ValueError('Unsafe executable name')
                if name.startswith(('python', 'pip')): continue
                target = directory/entry['path']
                if not target.resolve().is_relative_to(directory.resolve()): raise ValueError('Escaping executable')
                runtime = '/opt/corpus/servers/'+directory.name+'/'+entry['path']
                command = ([entry['interpreter']] if entry.get('interpreter') else [])+[runtime]
                commands[name].append(command)
        bin_dir = context/'bin'
        if bin_dir.exists(): shutil.rmtree(bin_dir)
        bin_dir.mkdir()
        for name, candidates in commands.items():
            if len(candidates) != 1: continue
            launcher = bin_dir/name
            launcher.write_text('#!/bin/sh\nexec '+shlex.join(candidates[0])+' "$@"\n')
            launcher.chmod(0o755)
        grammar_id = subprocess.check_output([*PODMAN, 'image', 'inspect', '--format={{.Id}}', args.grammar_image], text=True).strip()
        build_args = ['--build-arg', 'GRAMMARS_IMAGE='+grammar_id]
        export_paths = ['toolchains']
    name = 'corpus-export-'+args.kind
    call([*PODMAN, 'create', '--name='+name, '--network=none', args.builder])
    try:
        for item in export_paths:
            dest = context/item
            if dest.exists(): shutil.rmtree(dest)
            src = '/opt/corpus/python' if item == 'python' else '/opt/toolchains'
            call([*PODMAN, 'cp', name+':'+src, str(dest)])
    finally: call([*PODMAN, 'rm', name])
    for name in ('worker.py', 'launch_server.py'):
        path = ROOT/'repo/containers'/name
        if path.exists(): shutil.copyfile(path, context/name)
    shutil.copyfile(ROOT/'repo/containers'/('Containerfile.'+args.kind), context/'Containerfile')
    if args.kind == 'servers':
        layers = stage_layers(context/'servers', context/'server-layers')
        containerfile = context/'Containerfile'
        copies = '\n'.join('COPY '+str(layer.relative_to(context))+'/ /opt/corpus/servers/' for layer in layers)
        containerfile.write_text(containerfile.read_text().replace('COPY servers /opt/corpus/servers', copies))
        (context/'.containerignore').write_text('servers/\n')
    image = f'localhost/code-corpora-{args.kind}:{args.tag}'
    call([*PODMAN, 'build', '--network=slirp4netns', *build_args, '-t', image, str(context)])
    result = json.loads(subprocess.check_output([*PODMAN, 'image', 'inspect', image]))
    atomic_json(ROOT/'artifacts'/(args.kind+'-image.json'), result)


if __name__ == '__main__': main()
