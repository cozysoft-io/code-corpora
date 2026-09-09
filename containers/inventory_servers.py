#!/usr/bin/env python3
"""Read source manifests without executing upstream code."""
import collections
import json
from pathlib import Path
import tomllib

root = Path('/srv/corpus/repo')
selection = tomllib.loads((root/'selected-servers.toml').read_text())['repo']
audit = tomllib.loads((root/'zed-sources.toml').read_text())
references = collections.defaultdict(list)
for group in ('extension', 'bundled_extension', 'builtin_server'):
    for entry in audit[group]:
        for path in entry.get('server_repositories', [entry['repository']] if 'repository' in entry else []):
            references[path].append({'extension': entry['id'], 'ids': entry.get('language_servers', [entry['id']])})
rows = []
for row in selection:
    source = root/'servers'/row['name']
    record = dict(row, references=references['servers/'+row['name']], status='pending')
    manifests = {}
    for name in ('package.json', 'Cargo.toml', 'go.mod', 'pyproject.toml', 'setup.py', 'pom.xml', 'build.gradle', 'CMakeLists.txt', 'Makefile', 'build.zig', 'mix.exs'):
        file = source/name
        if file.is_file():
            try:
                manifests[name] = json.loads(file.read_text()) if name.endswith('.json') else (tomllib.loads(file.read_text()) if name.endswith('.toml') else file.read_text()[:5000])
            except Exception as error: manifests[name] = {'error': str(error)}
    record['manifests'] = manifests
    record['present'] = (source/'.git').is_dir()
    rows.append(record)
target = root.parent/'artifacts/server-inventory.json'
target.write_text(json.dumps(rows, indent=2)+'\n')
print(json.dumps({'repositories': len(rows), 'present': sum(r['present'] for r in rows), 'manifests': dict(collections.Counter(k for r in rows for k in r['manifests']))}))
