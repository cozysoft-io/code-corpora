#!/usr/bin/env python3
"""Development builds and package extraction; run only inside the builder."""
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys
import tarfile


def source_files(root):
    for path in sorted(root.rglob('*')):
        relative = path.relative_to(root)
        if '.git' in relative.parts:
            continue
        if path.is_symlink():
            if not path.resolve().is_relative_to(root.resolve()):
                raise ValueError(f'Source symlink escapes checkout: {relative}')
        elif not (path.is_dir() or path.is_file()):
            raise ValueError(f'Special source file: {relative}')
        yield path, relative


def source_hash(root):
    digest = hashlib.sha256()
    for path, relative in source_files(root):
        mode = path.lstat().st_mode
        digest.update(json.dumps([str(relative), stat.S_IFMT(mode), mode & 0o111]).encode()+b'\0')
        if path.is_symlink():
            digest.update(os.readlink(path).encode()+b'\0')
        elif path.is_file():
            with path.open('rb') as stream:
                digest.update(hashlib.file_digest(stream, 'sha256').digest())
    return digest.hexdigest()


def stage_source(source, destination):
    # Validate links before copying, and convert internal absolute links so the
    # staged tree cannot accidentally read from the mounted checkout afterward.
    links = [(relative, path.resolve().relative_to(source.resolve()))
             for path, relative in source_files(source) if path.is_symlink()]
    if destination.is_symlink():
        destination.unlink()
    elif destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(source, destination, symlinks=True, ignore=shutil.ignore_patterns('.git'))
    for relative, target in links:
        link = destination/relative
        link.unlink()
        link.symlink_to(os.path.relpath(destination/target, link.parent))


def grammar(job):
    from worker import build_grammar, run
    root = Path('/work/source')
    stage_source(Path('/input/source'), root)
    provenance = dict(job, source_sha256=source_hash(root), local_development=True)
    directory = root/job.get('directory', '')
    if not directory.resolve().is_relative_to(root):
        raise ValueError('Grammar directory escapes checkout')
    if job.get('generate', True):
        parser = directory/'src/parser.c'
        match = re.search(r'#define LANGUAGE_VERSION (\d+)', parser.read_text()) if parser.exists() else None
        abi = match.group(1) if match else '15'
        subprocess.run(['/opt/toolchains/tree-sitter', 'generate', '--abi', abi], cwd=directory, check=True)
    provenance['generated_source_sha256'] = source_hash(root)
    if Path('/work/build').exists():
        shutil.rmtree('/work/build')
    build_grammar(provenance, source_root=root)
    output = Path('/out')
    manifest = json.loads((output/'artifact.json').read_text())
    scanners = [path for path in (directory/'src').glob('scanner.*') if path.suffix in ('.c', '.cc', '.cpp', '.cxx')]
    if directory/'src/scanner.c' in scanners:
        scanners = [directory/'src/scanner.c']
    compiler = '/opt/toolchains/wasi-sdk/bin/clang++' if any(p.suffix != '.c' for p in scanners) else '/opt/toolchains/wasi-sdk/bin/clang'
    run([compiler, '-fPIC', '-shared', '-Os', '-Wl,--export='+manifest['symbol'],
         '-I', directory/'src', '-I', directory, '-I', root,
         directory/'src/parser.c', *scanners, '-o', output/'parser.wasm'])
    manifest['wasm_sha256'] = hashlib.sha256((output/'parser.wasm').read_bytes()).hexdigest()
    manifest['toolchains'] = json.loads(Path('/opt/corpus/toolchains.dev.json').read_text())
    (output/'artifact.json').write_text(json.dumps(manifest, indent=2)+'\n')


def extension(job):
    output = Path('/out')
    with tarfile.open('/input/package') as archive:
        members = archive.getmembers()
        if sum(member.size for member in members) > 512*1024**2:
            raise ValueError('Extension expands beyond 512 MiB')
        if any(not (member.isfile() or member.isdir()) for member in members):
            raise ValueError('Extension package contains links or special files')
        archive.extractall(output, filter='data')
    import tomllib
    manifest = tomllib.loads((output/'extension.toml').read_text())
    if (manifest['id'], manifest['version']) != (job['id'], job['version']):
        raise ValueError('Extension package does not match the selected version')
    (output/'corpus-provenance.json').write_text(json.dumps(job, indent=2)+'\n')


def server(job, phase):
    root = Path('/work/source')
    if phase == 'prepare':
        stage_source(Path('/input/source'), root)
        Path('/work/input-provenance.json').write_text(json.dumps({
            'source_sha256': source_hash(root), 'source_head': job.get('source_head'),
            'selected_sha': job['sha'], 'local_development': True}, indent=2)+'\n')
    subprocess.run(['python3', '/opt/corpus/server_worker.py', phase], check=True)
    if phase == 'build':
        path = Path('/out/artifact.json')
        manifest = json.loads(path.read_text())
        manifest.update(json.loads(Path('/work/input-provenance.json').read_text()))
        path.write_text(json.dumps(manifest, indent=2)+'\n')


if __name__ == '__main__':
    job = json.loads(Path('/input/job.json').read_text())
    if sys.argv[1] == 'grammar':
        grammar(job)
    elif sys.argv[1] == 'extension':
        extension(job)
    else:
        server(job, sys.argv[1])
