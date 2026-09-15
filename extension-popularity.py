#!/usr/bin/env python3
"""Fetch exact Zed download counts without installing extensions or cloning sources."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import tomllib
from urllib.parse import urlencode
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parent
API = 'https://api.zed.dev/extensions'
LANGUAGE_PROVIDES = {'languages', 'grammars', 'language-servers'}
CATALOG_LIMIT = 1000


def collect(min_downloads):
    started = datetime.now(timezone.utc).isoformat()
    audit_bytes = (ROOT / 'zed-sources.toml').read_bytes()
    audit = tomllib.loads(audit_bytes.decode())
    audited = {
        row['id']: row for row in audit['extension']
        if row.get('grammars') or row.get('language_servers')
    }
    requests = []

    def fetch(**parameters):
        # Without this parameter the API omits modern extension manifests.
        url = API + '?' + urlencode({'max_schema_version': 1, **parameters})
        request = Request(url, headers={
            'User-Agent': 'code-corpora/1.0', 'Accept': 'application/json',
        })
        with urlopen(request, timeout=30) as response:
            body = response.read()
        rows = json.loads(body)['data']
        if not isinstance(rows, list):
            raise ValueError(f'Expected a data array from {url}')
        identifiers = set()
        for row in rows:
            identifier = row['id']
            count = row['download_count']
            if (not isinstance(identifier, str) or identifier in identifiers
                    or type(count) is not int or count < 0
                    or not isinstance(row.get('provides'), list)):
                raise ValueError(f'Invalid or duplicate extension metadata from {url}')
            identifiers.add(identifier)
        requests.append({
            'url': url, 'fetched_at': datetime.now(timezone.utc).isoformat(),
            'response_sha256': hashlib.sha256(body).hexdigest(),
            'count': len(rows), 'at_result_limit': len(rows) >= CATALOG_LIMIT,
        })
        return rows

    # The general list supplies older entries whose provides metadata is empty.
    by_id = {row['id']: row for row in fetch()}
    for category in sorted(LANGUAGE_PROVIDES):
        # Comma-separated provides filters intersect categories; union separate
        # requests so syntax-only and LSP-only extensions are both represented.
        rows = fetch(provides=category)
        if len(rows) >= CATALOG_LIMIT:
            raise ValueError(f'{category} hit the API result limit; enumeration needs updating')
        by_id.update((row['id'], row) for row in rows)

    unavailable = []
    for identifier in sorted(audited.keys() - by_id.keys()):
        matches = [row for row in fetch(filter=identifier) if row['id'] == identifier]
        if matches:
            by_id[identifier] = matches[0]
        else:
            unavailable.append(identifier)

    languages = []
    for identifier, row in by_id.items():
        evidence = []
        if LANGUAGE_PROVIDES.intersection(row['provides']):
            evidence.append('api-provides')
        if identifier in audited:
            evidence.append('source-audit')
        if evidence:
            languages.append(dict(row, language_evidence=evidence))
    languages.sort(key=lambda row: (-row['download_count'], row['id']))
    selected = [row for row in languages if row['download_count'] > min_downloads]
    download_total = sum(row['download_count'] for row in languages)
    comparisons = []
    for threshold in sorted({0, 1000, 10000, 100000, min_downloads}):
        qualifying = [row for row in languages if row['download_count'] > threshold]
        comparisons.append({
            'more_than_downloads': threshold, 'extension_count': len(qualifying),
            'known_language_download_share': (
                sum(row['download_count'] for row in qualifying) / download_total
                if download_total else None
            ),
        })
    return {
        'schema_version': 1, 'started_at': started,
        'finished_at': datetime.now(timezone.utc).isoformat(),
        'source_audit_sha256': hashlib.sha256(audit_bytes).hexdigest(),
        'source_audit_snapshot_date': audit['snapshot_date'],
        'requests': requests,
        'selection': {'more_than_downloads': min_downloads, 'ids': [r['id'] for r in selected]},
        'comparisons': comparisons,
        'audited_language_ids_missing_from_api': unavailable,
        'unreadable_audit_ids': [r['id'] for r in audit['extension'] if r.get('audit_error')],
        'limitations': [
            'Counts are cumulative downloads, not unique users; requests are not an atomic snapshot.',
            'General catalog is capped; complete marketplace enumeration is not claimed.',
            'New extensions with missing provides metadata may escape classification.',
            'Audit classification describes audited versions, not necessarily current packages.',
            'Selection does not check WASM API/platform compatibility or installation success.',
            'Corpus-required overrides and provider conflicts still need review before installation.',
        ],
        'extensions': languages,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--min-downloads', type=int, default=1000,
                        help='Select counts strictly greater than this value (default: 1000)')
    parser.add_argument('--output', type=Path, default=ROOT / '.corpus/zed/popularity.json')
    args = parser.parse_args()
    if args.min_downloads < 0:
        parser.error('--min-downloads must be nonnegative')
    report = collect(args.min_downloads)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({
        'output': str(args.output), 'language_extensions': len(report['extensions']),
        'selected': len(report['selection']['ids']),
        'missing_from_api': report['audited_language_ids_missing_from_api'],
        'comparisons': report['comparisons'],
    }, indent=2))


if __name__ == '__main__':
    main()
