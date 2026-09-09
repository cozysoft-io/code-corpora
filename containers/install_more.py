"""Install checksum-pinned Zig and Elixir SDKs inside the rootless builder."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tarfile
import tempfile
import urllib.request
import zipfile

for name, spec in json.loads(Path('/opt/corpus/toolchains.more.json').read_text()).items():
    with tempfile.TemporaryDirectory() as temporary:
        temp = Path(temporary)
        archive = temp/'archive'
        with urllib.request.urlopen(spec['url'], timeout=120) as response, archive.open('wb') as out:
            shutil.copyfileobj(response, out)
        with archive.open('rb') as stream:
            if hashlib.file_digest(stream, 'sha256').hexdigest() != spec['sha256']:
                raise ValueError('Checksum mismatch: '+name)
        prefix = Path('/opt/toolchains')/name
        if spec['url'].endswith('.zip'):
            prefix.mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(archive) as package:
                for item in package.infolist():
                    if not (prefix/item.filename).resolve().is_relative_to(prefix):
                        raise ValueError('Escaping archive path')
                package.extractall(prefix)
            for path in (prefix/'bin').iterdir():
                if path.is_file(): path.chmod(0o755)
        else:
            with tarfile.open(archive) as package:
                package.extractall(temp/'unpacked', filter='data')
            if spec.get('flat'):
                shutil.move(temp/'unpacked', prefix)
            else:
                [directory] = list((temp/'unpacked').iterdir())
                if spec.get('configure'):
                    subprocess.run(['./configure', '--prefix='+str(prefix)], cwd=directory, check=True)
                    subprocess.run(['make', 'install', '-j2'], cwd=directory, check=True)
                else:
                    shutil.move(directory, prefix)
        print(name, spec['version'], spec['sha256'], flush=True)
