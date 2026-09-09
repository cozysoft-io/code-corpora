"""Upload an OCI archive using a short-lived, object-specific Cloud Storage URL."""
import argparse
import json
from pathlib import Path
import urllib.parse
import urllib.request

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('archive', type=Path)
parser.add_argument('signed_url', type=Path, help='JSON output from gcloud storage sign-url')
arguments = parser.parse_args()
record = json.loads(arguments.signed_url.read_text())
url = record[0]['signed_url']
parsed = urllib.parse.urlsplit(url)
if parsed.scheme != 'https' or parsed.netloc != 'storage.googleapis.com':
    raise ValueError('Expected the Cloud Storage HTTPS endpoint')
size = arguments.archive.stat().st_size
with arguments.archive.open('rb') as source:
    request = urllib.request.Request(url, data=source, method='PUT', headers={
        'Content-Length':str(size), 'Content-Type':'application/octet-stream'})
    try:
        with urllib.request.urlopen(request, timeout=300) as response:
            if response.status != 200: raise RuntimeError('Unexpected upload response')
    except Exception:
        raise RuntimeError('Signed archive upload failed; URL omitted from diagnostics') from None
print('Uploaded', arguments.archive.name, size, 'bytes', flush=True)
