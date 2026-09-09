"""Install pinned development tools inside the builder."""
import gzip
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
import urllib.request

specifications = json.loads(Path('/opt/corpus/toolchains.dev.json').read_text())
with tempfile.TemporaryDirectory() as temporary:
    root = Path(temporary)
    for name, specification in specifications.items():
        archive = root/name
        with urllib.request.urlopen(specification['url'], timeout=120) as response, archive.open('wb') as output:
            shutil.copyfileobj(response, output)
        with archive.open('rb') as stream:
            if hashlib.file_digest(stream, 'sha256').hexdigest() != specification['sha256']:
                raise ValueError('Checksum mismatch: '+name)
        if name == 'tree_sitter':
            executable = Path('/opt/toolchains/tree-sitter')
            with gzip.open(archive) as source, executable.open('wb') as output:
                shutil.copyfileobj(source, output)
            executable.chmod(0o755)
        else:
            with tarfile.open(archive) as package:
                package.extractall(root/'wasi', filter='data')
            [directory] = (root/'wasi').iterdir()
            shutil.move(directory, '/opt/toolchains/wasi-sdk')
