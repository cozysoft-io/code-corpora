#!/usr/bin/env python3
"""Install SDKs from checksum-locked official release metadata."""
import hashlib
import json
from pathlib import Path
import tarfile
import tempfile
import urllib.request

for name, spec in json.loads(Path('/opt/corpus/toolchains.extra.json').read_text()).items():
    if not name.startswith('dotnet-'): raise ValueError(name)
    destination = Path('/opt/toolchains/dotnet')
    destination.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        archive = Path(tmp)/'sdk.tar.gz'
        urllib.request.urlretrieve(spec['url'], archive)
        with archive.open('rb') as stream:
            digest = hashlib.file_digest(stream, 'sha512').hexdigest()
        if digest.lower() != spec['sha512'].lower(): raise ValueError('SDK checksum mismatch: '+name)
        with tarfile.open(archive) as tar: tar.extractall(destination, filter='data')
