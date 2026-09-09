#!/usr/bin/env python3
"""Generate inspectable first-pass recipes; leave complex targets explicit."""
import json
from pathlib import Path
import tomllib

root = Path('/srv/corpus/repo')
inventory = json.loads((root.parent/'artifacts/server-inventory.json').read_text())
jobs, coverage = [], []
for row in inventory:
    repo = root/'servers'/row['name']
    recipe = {k: row[k] for k in ('name', 'url', 'sha', 'references')}
    manifests = row['manifests']
    cargo = manifests.get('Cargo.toml', {})
    node = manifests.get('package.json', {})
    if row['name'] == 'tools' and (repo/'gopls/go.mod').exists():
        recipe.update(kind='go', directory='gopls')
    elif cargo and (cargo.get('workspace') or cargo.get('bin') or (repo/'src/main.rs').exists()):
        recipe['kind'] = 'cargo'
        if cargo.get('package') and (cargo.get('bin') or (repo/'src/main.rs').exists()):
            recipe['package'] = cargo['package']['name']
    elif 'go.mod' in manifests:
        recipe['kind'] = 'go'
    elif (repo/'gopls/go.mod').exists():
        recipe.update(kind='go', directory='gopls')
    elif node.get('bin'):
        recipe['kind'] = 'npm'
        scripts = node.get('scripts', {})
        recipe['script'] = next((s for s in ('build', 'compile') if s in scripts), None)
    elif 'pyproject.toml' in manifests or 'setup.py' in manifests:
        project = manifests.get('pyproject.toml', {}).get('project', {})
        poetry = manifests.get('pyproject.toml', {}).get('tool', {}).get('poetry', {})
        if not (project.get('scripts') or poetry.get('scripts') or 'setup.py' in manifests):
            coverage.append(dict(recipe, status='needs-recipe', reason='Python source has no declared CLI entry point'))
            continue
        recipe['kind'] = 'python'
    else:
        dependencies = cargo.get('dependencies', {})
        is_extension = 'zed_extension_api' in dependencies and not cargo.get('workspace')
        coverage.append(dict(recipe, status='extension-only' if is_extension else 'needs-recipe',
                             reason='No standalone binary in this Zed extension crate' if is_extension else 'Requires a target-specific build recipe'))
        continue
    recipe['network_exception'] = 'Public dependency preparation only; no credentials/private data; host egress rejects internal and metadata HTTP endpoints'
    jobs.append(recipe)
    coverage.append(dict(recipe, status='pending'))
out = root.parent/'artifacts'
(out/'server-recipes.json').write_text(json.dumps(jobs, indent=2)+'\n')
(out/'server-coverage.json').write_text(json.dumps(coverage, indent=2)+'\n')
from collections import Counter
print(json.dumps({'recipes': dict(Counter(r['kind'] for r in jobs)), 'coverage': dict(Counter(r['status'] for r in coverage))}))
