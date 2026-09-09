#!/usr/bin/env python3
"""Import locally built artifacts into the VM's aggregate without running them."""
import argparse
from datetime import datetime, timezone
import fcntl
import hashlib
import json
from pathlib import Path
import re
import shutil
import tomllib
import uuid


def validate(directory, selection):
    label = directory.name
    directory = directory.resolve(strict=True)
    metadata = directory/'artifact.json'
    if metadata.is_symlink() or not metadata.is_file():
        raise ValueError('Invalid artifact manifest')
    artifact = json.loads(metadata.read_text())
    name = artifact['name']
    if not re.fullmatch(r'[A-Za-z0-9_.+-]+', name) or label != name:
        raise ValueError('Invalid artifact name')
    selected = selection.get(name, {})
    if not selected or artifact.get('sha') != selected['sha']:
        raise ValueError('Artifact does not match selected pin: '+name)
    if artifact.get('selected_sha') != selected['sha'] or artifact.get('source_head') != selected['sha']:
        raise ValueError('Local source provenance does not match selected pin: '+name)
    files = set()
    for path in directory.rglob('*'):
        if path.is_symlink():
            if not path.resolve(strict=True).is_relative_to(directory):
                raise ValueError('Escaping artifact link: '+str(path))
        elif path.is_file():
            relative = str(path.relative_to(directory))
            if relative != 'artifact.json': files.add(relative)
        elif not path.is_dir():
            raise ValueError('Special artifact file: '+str(path))
    if files != set(artifact['hashes']):
        raise ValueError('Artifact file inventory mismatch: '+name)
    for relative, expected in artifact['hashes'].items():
        with (directory/relative).open('rb') as stream:
            if hashlib.file_digest(stream, 'sha256').hexdigest() != expected:
                raise ValueError('Artifact checksum mismatch: '+relative)
    for executable in artifact['executables']:
        path = (directory/executable['path']).resolve(strict=True)
        if not path.is_relative_to(directory) or not path.is_file():
            raise ValueError('Invalid executable path: '+name)
        if not executable.get('interpreter') and not path.stat().st_mode & 0o111:
            raise ValueError('Artifact is not executable: '+name)
    if not artifact['executables']: raise ValueError('No executables: '+name)
    return artifact


def import_one(directory, root, selection):
    artifact = validate(directory, selection)
    name = artifact['name']
    locks = root/'jobs/.locks'
    locks.mkdir(parents=True, exist_ok=True)
    with (locks/(name+'.lock')).open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        destination = root/'artifacts/servers'/name
        # A completed cloud build may have appeared while the bundle was in transit.
        if destination.exists():
            raise FileExistsError('Existing artifact retained: '+name)
        record = dict(artifact, image=artifact['builder_image'], artifact=artifact,
                      status='built-unverified', phase='build', exit_code=0,
                      imported_at=datetime.now(timezone.utc).isoformat(),
                      build_origin='local-rootless-podman')
        destination.parent.mkdir(parents=True, exist_ok=True)
        temporary_root = root/'artifacts/server-imports'/uuid.uuid4().hex
        staging = temporary_root/name
        try:
            shutil.copytree(directory, staging, symlinks=True)
            # Check the copied bytes before making the distribution visible.
            if validate(staging, selection) != artifact:
                raise ValueError('Artifact changed during import: '+name)
            record['artifact_metadata_sha256'] = hashlib.sha256((staging/'artifact.json').read_bytes()).hexdigest()
            text = json.dumps(record, indent=2)+'\n'
            (staging/'build.json').write_text(text)
            staging.rename(destination)
        finally:
            if temporary_root.exists(): shutil.rmtree(temporary_root)
        job = root/'jobs'/('server-'+name)
        job.mkdir(parents=True, exist_ok=True)
        previous = job/'result.json'
        if previous.exists():
            shutil.copyfile(previous, job/('result-before-local-import-'+uuid.uuid4().hex+'.json'))
        temporary = job/('result-'+uuid.uuid4().hex+'.tmp')
        temporary.write_text(text)
        temporary.replace(previous)
    return {'name':name, 'status':'imported', 'sha':artifact['sha']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--root', type=Path, default=Path('/srv/corpus'))
    parser.add_argument('--check', action='store_true', help='Validate without importing')
    arguments = parser.parse_args()
    selection = {row['name']:row for row in tomllib.loads(
        (arguments.root/'repo/selected-servers.toml').read_text())['repo']}
    for directory in sorted(arguments.source.iterdir()):
        if arguments.check:
            artifact = validate(directory, selection)
            print(json.dumps({'name':artifact['name'], 'status':'validated'}), flush=True)
        else:
            print(json.dumps(import_one(directory, arguments.root, selection)), flush=True)


if __name__ == '__main__': main()
