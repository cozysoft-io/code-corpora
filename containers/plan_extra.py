#!/usr/bin/env python3
"""Resolve reviewed recipe overrides against the unchanged source selection."""
import argparse
import json
from pathlib import Path

root = Path('/srv/corpus')
p = argparse.ArgumentParser()
p.add_argument('--overrides', default='recipes.extra.json')
p.add_argument('--output', default='server-recipes-extra.json')
args = p.parse_args()
inventory = {r['name']: r for r in json.loads((root/'artifacts/server-inventory.json').read_text())}
overrides = json.loads((root/'repo/containers'/args.overrides).read_text())
jobs = []
for name, override in overrides.items():
    row = inventory[name]
    jobs.append(dict({k: row[k] for k in ('name', 'url', 'sha', 'references')}, **override))
(root/'artifacts'/args.output).write_text(json.dumps(jobs, indent=2)+'\n')
print(f'{len(jobs)} additional/retry recipes; original source pins retained')
