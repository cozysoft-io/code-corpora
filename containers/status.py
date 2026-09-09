#!/usr/bin/env python3
"""Read-only live progress summary on the build VM."""
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import subprocess
import tomllib

root = Path('/srv/corpus')
report = {'observed_at': datetime.now(timezone.utc).isoformat(), 'images': {}}
for name in ('build', 'grammars', 'servers'):
    path = root/'artifacts'/(name+'-image.json')
    if path.is_file():
        image = json.loads(path.read_text())[0]
        report['images'][name] = {'local_id': image['Id'], 'bytes': image['Size']}
path = root/'images/grammars/grammar-catalog.json'
if path.is_file(): report['grammars'] = dict(Counter(r['status'] for r in json.loads(path.read_text())))
rows = [json.loads(p.read_text()) for p in (root/'jobs').glob('server-*/result.json')]
selection = {row['name']: row['sha'] for row in tomllib.loads(
    (root/'repo/selected-servers.toml').read_text())['repo']}
current_rows = [row for row in rows if row.get('sha') == selection.get(row['name'])]
report['superseded_build_results'] = len(rows)-len(current_rows)
rows = current_rows
report['server_builds'] = dict(Counter(r['status'] for r in rows))
path = root/'artifacts/version-rebuild-current.json'
if path.is_file():
    rebuild = json.loads(path.read_text())
    directory = Path(rebuild['directory'])
    coverage = {row['name']: row for row in json.loads((directory/'coverage.json').read_text())}
    for row in rows:
        if row['name'] in coverage:
            coverage[row['name']] = row
    report['version_rebuild'] = {'directory': str(directory), 'changed': rebuild['changed'],
        'queued': rebuild['queued'], 'results': dict(Counter(row['status'] for row in coverage.values()))}
    limits = directory/'parallelism.json'
    if limits.is_file(): report['version_rebuild']['ordinary_jobs'] = json.loads(limits.read_text())['jobs']
path = root/'artifacts/server-recipes.json'
if path.is_file(): report['first_pass_recipe_count'] = len(json.loads(path.read_text()))
path = root/'artifacts/server-coverage.json'
if path.is_file():
    covered = {r['name'] for p in (root/'artifacts').glob('server-recipes*.json') for r in json.loads(p.read_text())}
    report['total_recipe_count'] = len(covered)
    report['additional_recipes_needed'] = sum(r['status']=='needs-recipe' and r['name'] not in covered for r in json.loads(path.read_text()))
path = root/'artifacts/build-expanded-image.json'
if path.is_file():
    image = json.loads(path.read_text())[0]
    report['expanded_builder'] = {'local_id': image['Id'], 'bytes': image['Size']}
path = root/'artifacts/build-compat-image.json'
if path.is_file():
    image = json.loads(path.read_text())[0]
    report['compat_builder'] = {'local_id': image['Id'], 'bytes': image['Size']}
path = root/'artifacts/server-parallelism.json'
if path.is_file(): report['main_worker_limit'] = json.loads(path.read_text())['jobs']
path = root/'artifacts/server-supplement-parallelism.json'
if path.is_file(): report['supplement_worker_limit'] = json.loads(path.read_text())['jobs']
summaries = sorted((root/'artifacts/runtime-checks/servers').glob('*/summary.json'), key=lambda p:p.stat().st_mtime)
if summaries:
    summary = json.loads(summaries[-1].read_text())
    report['latest_server_smoke'] = {'image': summary['image'], 'complete': summary['complete'],
        'target_count': summary['target_count'], 'results': dict(Counter(r['status'] for r in summary['results']))}
report['active_units'] = subprocess.check_output(['systemctl', 'list-units', 'corpus-*', '--state=active', '--no-legend', '--plain'], text=True).splitlines()
report['free_disk_gib'] = round(shutil.disk_usage(root).free/1024**3, 1)
path = root/'artifacts/published-images.json'
published = json.loads(path.read_text())['images'] if path.exists() else {}
report['published_to_ghcr'] = len(published) == 3
report['published_images'] = {name: r['reference'] for name, r in published.items()}
print(json.dumps(report, indent=2))
