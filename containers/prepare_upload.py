#!/usr/bin/env python3
"""Split local OCI archives into private GitHub release assets; never execute them."""
import argparse
import hashlib
import json
from pathlib import Path
import re

p = argparse.ArgumentParser()
p.add_argument('--output', type=Path, required=True)
p.add_argument('--image', nargs=3, action='append', metavar=('KIND', 'ARCHIVE', 'IMAGE_ID'), required=True)
args = p.parse_args()
args.output.mkdir(parents=True, exist_ok=True)
manifest_path = args.output/'manifest.json'
manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {'format_version': 1, 'images': {}}
for kind, archive, image_id in args.image:
    if kind not in ('build', 'grammars', 'servers'): p.error('Invalid kind')
    if not re.fullmatch(r'(sha256:)?[a-f0-9]{64}', image_id): p.error('Invalid image ID')
    image_id = 'sha256:'+image_id.removeprefix('sha256:')
    whole = hashlib.sha256()
    parts = []
    with open(archive, 'rb') as source:
        number = 0
        while True:
            name = f'corpus-{kind}.tar.part{number:03}'
            path = args.output/name
            digest = hashlib.sha256()
            size = 0
            with path.open('wb') as output:
                while size < 1800*1024*1024:
                    block = source.read(min(8*1024*1024, 1800*1024*1024-size))
                    if not block: break
                    output.write(block)
                    whole.update(block)
                    digest.update(block)
                    size += len(block)
            if not size:
                path.unlink()
                break
            parts.append({'name': name, 'sha256': digest.hexdigest(), 'bytes': size})
            number += 1
    manifest['images'][kind] = {'image_id': image_id, 'sha256': whole.hexdigest(), 'parts': parts}
manifest_path.write_text(json.dumps(manifest, indent=2)+'\n')
print(json.dumps(manifest, indent=2))
