#!/bin/bash
# Finish the first automatic pass, preserve results, then stop idle VM billing.
set -euo pipefail
cd /srv/corpus
while systemctl list-units --state=active --no-legend --plain \
      'corpus-server-*' 'corpus-sdk-*' 'corpus-runtime-*' 'corpus-export-*' \
      'corpus-go-python-retry.service' | grep -q .; do
  sleep 30
done
# Once compilation finishes, also stop if assembly, tests, or export fail.
# Install this trap after waiting so restarting the waiting service is safe.
finish() {
  local result=$?
  trap - EXIT
  printf '%s\n' "$result" > artifacts/finish-batch-exit-code
  if [ ! -e /srv/corpus/keep-running ]; then systemctl poweroff; fi
  exit "$result"
}
trap finish EXIT
tag="${1:-batch1}"
builder=localhost/code-corpora-build:toolchains
if [ -s artifacts/build-expanded-image.json ]; then builder=localhost/code-corpora-build:expanded; fi
if [ -s artifacts/build-compat-image.json ]; then builder=localhost/code-corpora-build:compat; fi
python3 repo/containers/assemble.py servers --tag "$tag" --builder "$builder"
python3 repo/containers/runtime_checks.py servers --image "localhost/code-corpora-servers:$tag"
sudo -u corpus -H bash repo/containers/export-images.sh "$tag"
python3 repo/containers/status.py > "artifacts/$tag-status.json"
