#!/usr/bin/env python3
"""Run inside the grammar runtime image; quarantine entries are never loaded."""
import json
from pathlib import Path
import subprocess

catalog = json.loads(Path('/opt/corpus/grammar-catalog.json').read_text())
results = []
for row in catalog:
    if row['status'] != 'built':
        results.append({'name': row['name'], 'status': row['status']})
        continue
    try:
        result = subprocess.run(['/opt/corpus/python/bin/python', '/opt/corpus/worker.py',
                                 'smoke-grammar', '/opt/corpus/grammars/'+row['name']],
                                capture_output=True, text=True, timeout=20)
        results.append({'name': row['name'], 'status': 'passed' if result.returncode == 0 else 'failed',
                        'exit_code': result.returncode, 'output': (result.stdout+result.stderr)[-2000:]})
    except subprocess.TimeoutExpired:
        results.append({'name': row['name'], 'status': 'timeout'})
print(json.dumps(results, indent=2))
raise SystemExit(int(any(r['status'] in ('failed', 'timeout') for r in results)))
