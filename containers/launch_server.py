#!/usr/bin/env python3
"""Explicitly select one installed executable from the aggregate image."""
import argparse
import json
import os
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('repository')
p.add_argument('executable')
p.add_argument('args', nargs=argparse.REMAINDER)
args = p.parse_args()
root = Path('/opt/corpus/servers')
if Path(args.repository).name != args.repository: p.error('Invalid repository name')
directory = root/args.repository
meta = json.loads((directory/'artifact.json').read_text())
entry = next((x for x in meta['executables'] if x['name'] == args.executable), None)
if entry is None: p.error('Executable is not in the artifact catalog')
target = directory/entry['path']
if not target.resolve().is_relative_to(directory): p.error('Executable escapes its prefix')
os.makedirs('/work/home', exist_ok=True)
os.environ['HOME'] = '/work/home'
command = ([entry['interpreter']] if entry.get('interpreter') else []) + [str(target), *args.args]
os.execvp(command[0], command)
