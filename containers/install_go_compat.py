"""Install the Go version required by dependencies that exclude Go 1.27."""
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
import urllib.request

spec = json.loads(Path('/opt/corpus/toolchains.go-compat.json').read_text())
with tempfile.TemporaryDirectory() as temporary:
    root = Path(temporary)
    archive = root/'go.tar.gz'
    with urllib.request.urlopen(spec['url'], timeout=120) as response, archive.open('wb') as out:
        shutil.copyfileobj(response, out)
    with archive.open('rb') as stream:
        if hashlib.file_digest(stream, 'sha256').hexdigest() != spec['sha256']:
            raise ValueError('Go compatibility SDK checksum mismatch')
    with tarfile.open(archive) as package:
        package.extractall(root, filter='data')
    shutil.move(root/'go', '/opt/toolchains/go-1.26')
print(spec['version'], spec['sha256'])
