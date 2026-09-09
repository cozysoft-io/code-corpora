#!/usr/bin/env python3
"""Upload prepared private release assets and dispatch the trusted publisher."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

p = argparse.ArgumentParser()
p.add_argument('--release', required=True)
p.add_argument('--directory', type=Path, required=True)
p.add_argument('--kind', choices=('build', 'grammars', 'servers'), action='append', required=True)
args = p.parse_args()
repo = 'cozysoft-io/corpus-containers'
if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,100}', args.release): p.error('Unsafe release tag')
private = json.loads(subprocess.check_output(['gh', 'api', 'repos/'+repo]))['private']
if not private: raise RuntimeError('Publisher repository is not private')
manifest_path = args.directory/'manifest.json'
manifest = json.loads(manifest_path.read_text())
assets = []
for kind in args.kind:
    if manifest['images'][kind].get('archive_url'): continue
    for part in manifest['images'][kind]['parts']:
        if Path(part['name']).name != part['name']: raise ValueError('Unsafe asset path')
        path = args.directory/part['name']
        with path.open('rb') as source: actual = hashlib.file_digest(source, 'sha256').hexdigest()
        if actual != part['sha256']: raise ValueError('Asset checksum mismatch: '+str(path))
        assets.append(str(path))
if assets:
    subprocess.run(['gh', 'release', 'upload', args.release, '--repo', repo, '--clobber', *assets], check=True)
# Publish the manifest last; a dispatched job will only see complete assets.
subprocess.run(['gh', 'release', 'upload', args.release, '--repo', repo, '--clobber', str(manifest_path)], check=True)
subprocess.run(['gh', 'workflow', 'run', 'publish.yml', '--repo', repo,
                '-f', 'release='+args.release, '-f', 'kinds='+json.dumps(args.kind)], check=True)
