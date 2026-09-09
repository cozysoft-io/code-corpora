"""Install a single checksum-pinned tarball toolchain inside the builder."""
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
import sys
import urllib.request

spec = json.loads(Path(sys.argv[1]).read_text())
with tempfile.TemporaryDirectory() as temporary:
    root = Path(temporary)
    archive = root/'archive'
    with urllib.request.urlopen(spec['url'], timeout=120) as response, archive.open('wb') as out:
        shutil.copyfileobj(response, out)
    with archive.open('rb') as stream:
        if hashlib.file_digest(stream, 'sha256').hexdigest() != spec['sha256']:
            raise ValueError('Toolchain checksum mismatch')
    with tarfile.open(archive) as package:
        package.extractall(root/'unpacked', filter='data')
    [directory] = list((root/'unpacked').iterdir())
    if not directory.is_dir(): raise ValueError('Expected one toolchain directory')
    shutil.move(directory, Path('/opt/toolchains')/sys.argv[2])
print(spec['version'], spec['sha256'])
