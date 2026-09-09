#!/usr/bin/env python3
"""Install checksum-locked official SDK distributions during image assembly."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tarfile
import tempfile
import urllib.request

lock = json.loads(Path('/opt/corpus/toolchains.json').read_text())
target = Path('/opt/toolchains')
target.mkdir(exist_ok=True)
for name, spec in lock.items():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        archive = tmp/'sdk.tar'
        urllib.request.urlretrieve(spec['url'], archive)
        digest = hashlib.file_digest(archive.open('rb'), 'sha256').hexdigest()
        if digest != spec['sha256']: raise ValueError(f'{name}: checksum mismatch')
        with tarfile.open(archive) as tar:
            tar.extractall(tmp/'unpacked', filter='data')
        unpacked, = (tmp/'unpacked').iterdir()
        if name == 'rust':
            subprocess.run(['bash', str(unpacked/'install.sh'), '--prefix=/opt/toolchains/rust',
                            '--components=rustc,cargo,rust-std-x86_64-unknown-linux-gnu',
                            '--disable-ldconfig'], check=True)
        else: shutil.move(unpacked, target/name)
