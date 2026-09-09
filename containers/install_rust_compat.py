"""Install historical Rust toolchains required by pinned upstream sources."""
import hashlib
import json
from pathlib import Path
import subprocess
import tarfile
import tempfile
import urllib.request

for name, spec in json.loads(Path('/opt/corpus/toolchains.rust-compat.json').read_text()).items():
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        archive = root/'sdk.tar.xz'
        urllib.request.urlretrieve(spec['url'], archive)
        with archive.open('rb') as stream:
            if hashlib.file_digest(stream, 'sha256').hexdigest() != spec['sha256']:
                raise ValueError('Rust SDK checksum mismatch')
        with tarfile.open(archive) as tar: tar.extractall(root/'unpacked', filter='data')
        unpacked, = (root/'unpacked').iterdir()
        subprocess.run(['bash', str(unpacked/'install.sh'), '--prefix=/opt/toolchains/'+name,
                        '--components=rustc,cargo,rust-std-x86_64-unknown-linux-gnu',
                        '--disable-ldconfig'], check=True)
