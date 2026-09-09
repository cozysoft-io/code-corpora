#!/usr/bin/env python3
"""Export pinned Git objects, never local generated/untracked artifacts."""
import argparse
import io
import json
from pathlib import Path, PurePosixPath
import subprocess
import tarfile
import tomllib

p = argparse.ArgumentParser()
p.add_argument('output')
args = p.parse_args()
root = Path(__file__).resolve().parent.parent
rows = tomllib.loads((root/'selected-grammars.toml').read_text())['repo']
report = []
with tarfile.open(args.output, 'w:gz', compresslevel=3) as target:
    for r in rows:
        repo = root/'grammars'/r['name']
        if not (repo/'.git').exists():
            report.append(dict(r, status='unavailable-pin'))
            continue
        raw = subprocess.check_output(['git', 'archive', '--format=tar', r['sha']], cwd=repo)
        with tarfile.open(fileobj=io.BytesIO(raw)) as source:
            for member in source:
                name = PurePosixPath(member.name)
                if name.is_absolute() or '..' in name.parts:
                    raise ValueError(member.name)
                if not (member.isfile() or member.isdir() or member.issym()):
                    raise ValueError(f'Unsupported archive entry: {member.name}')
                if member.issym():
                    parts = list(name.parent.parts)
                    link = PurePosixPath(member.linkname)
                    if link.is_absolute(): raise ValueError(member.linkname)
                    for part in link.parts:
                        if part == '..':
                            if not parts: raise ValueError(member.linkname)
                            parts.pop()
                        elif part != '.': parts.append(part)
                member.name = f"grammars/{r['name']}/{member.name}"
                target.addfile(member, source.extractfile(member) if member.isfile() else None)
        report.append(dict(r, status='staged'))
        print(r['name'], flush=True)
    data = json.dumps(report, indent=2).encode()
    member = tarfile.TarInfo('grammar-inputs.json')
    member.size = len(data)
    target.addfile(member, io.BytesIO(data))
