#!/usr/bin/env python3
"""Run only in the private publishing repository's GitHub Actions job."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess


def api(path):
    return json.loads(subprocess.check_output(['gh', 'api', path]))


repo = os.environ['GITHUB_REPOSITORY']
owner = repo.split('/')[0]
kind = os.environ['CORPUS_KIND']
tag = os.environ['CORPUS_RELEASE']
if kind not in ('build', 'grammars', 'servers'): raise ValueError('Unexpected image kind')
if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,100}', tag): raise ValueError('Unsafe release tag')
if not api('repos/'+repo)['private']: raise ValueError('Publishing repository must remain private')
package_api = f'users/{owner}/packages/container/code-corpora-{kind}'
before = subprocess.run(['gh', 'api', package_api], capture_output=True, text=True)
if before.returncode == 0:
    if json.loads(before.stdout)['visibility'] != 'private': raise ValueError('Existing package is not private')
elif 'HTTP 404' not in before.stderr:
    raise RuntimeError('Cannot verify existing package visibility: '+before.stderr)

subprocess.run(['gh', 'release', 'download', tag, '--repo', repo,
                '--pattern', 'manifest.json', '--dir', 'incoming'], check=True)
manifest = json.loads(Path('incoming/manifest.json').read_text())
spec = manifest['images'][kind]
archive = Path('image.tar')
whole = hashlib.sha256()
with archive.open('wb') as output:
    for part in spec['parts']:
        name = part['name']
        if not re.fullmatch(r'[A-Za-z0-9_.-]+', name): raise ValueError('Unsafe asset name')
        subprocess.run(['gh', 'release', 'download', tag, '--repo', repo,
                        '--pattern', name, '--dir', 'incoming'], check=True)
        path = Path('incoming')/name
        digest = hashlib.sha256()
        with path.open('rb') as source:
            while block := source.read(8*1024*1024):
                digest.update(block)
                whole.update(block)
                output.write(block)
        if digest.hexdigest() != part['sha256']: raise ValueError('Chunk checksum mismatch')
        path.unlink()
if whole.hexdigest() != spec['sha256']: raise ValueError('Archive checksum mismatch')
transport = 'oci-archive:'+str(archive)
image_manifest = json.loads(subprocess.check_output(['skopeo', 'inspect', '--raw', transport]))
if image_manifest['config']['digest'] != spec['image_id']: raise ValueError('Image config digest mismatch')

auth = Path(os.environ['RUNNER_TEMP'])/'corpus-registry-auth.json'
os.environ['REGISTRY_AUTH_FILE'] = str(auth)
try:
    subprocess.run(['skopeo', 'login', '--username', owner, '--password-stdin', 'ghcr.io'],
                   input=os.environ['GH_TOKEN'], text=True, check=True)
    parent = None
    if kind == 'servers':
        parent_target = f'docker://ghcr.io/{owner}/code-corpora-grammars:{tag}'
        parent_manifest = json.loads(subprocess.check_output(['skopeo', 'inspect', '--raw', parent_target]))
        if parent_manifest['config']['digest'] != manifest['images']['grammars']['image_id']:
            raise ValueError('Published grammar parent does not match this release')
        parent_layers = [layer['digest'] for layer in parent_manifest['layers']]
        if [layer['digest'] for layer in image_manifest['layers'][:len(parent_layers)]] != parent_layers:
            raise ValueError('Server image does not preserve the grammar image layers')
        parent = subprocess.check_output(['skopeo', 'inspect', '--format', '{{.Digest}}', parent_target], text=True).strip()
    target = f'ghcr.io/{owner}/code-corpora-{kind}:{tag}'
    subprocess.run(['skopeo', 'copy', '--all', '--preserve-digests', '--digestfile', 'digest.txt',
                   transport, 'docker://'+target], check=True)
    package = api(package_api)
    if package['visibility'] != 'private': raise ValueError('Published package visibility is not private')
    record = {'kind': kind, 'reference': target.split(':')[0]+'@'+Path('digest.txt').read_text().strip(),
              'tag': target, 'image_id': spec['image_id'], 'visibility': package['visibility']}
    if parent: record['grammar_parent_digest'] = parent
    print('CORPUS_PUBLISHED '+json.dumps(record), flush=True)
    with open(os.environ['GITHUB_STEP_SUMMARY'], 'a') as summary:
        summary.write('Published private image: `'+record['reference']+'`\n')
finally:
    auth.unlink(missing_ok=True)
    archive.unlink(missing_ok=True)
