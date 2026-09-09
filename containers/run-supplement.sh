#!/bin/bash
# Run a separate recipe queue while keeping the main queue's CPU budget bounded.
set -euo pipefail
cd /srv/corpus
# SDK expansion is serialized separately; choose the image only after it settles.
while systemctl list-units --state=active --no-legend --plain 'corpus-sdk-*' | grep -q .; do
  sleep 10
done
set_jobs() {
  python3 - "$1" "$2" <<'PY'
import os, pathlib, sys
path = pathlib.Path('/srv/corpus/artifacts')/sys.argv[1]
temporary = path.with_suffix('.tmp')
temporary.write_text('{"jobs": '+str(int(sys.argv[2]))+'}\n')
os.replace(temporary, path)
PY
}
set_jobs server-parallelism.json 6
adjust_workers() {
  local previous=0 workers
  while true; do
    workers=8
    if systemctl is-active --quiet corpus-server-build; then
      workers=2
    elif systemctl is-active --quiet corpus-server-heavy; then
      workers=4
    fi
    if [ "$workers" != "$previous" ]; then
      set_jobs server-supplement-parallelism.json "$workers"
      previous=$workers
    fi
    sleep 10
  done
}
# Write an initial limit before dispatch and keep it synchronized thereafter.
set_jobs server-supplement-parallelism.json 2
adjust_workers &
controller=$!
cleanup() {
  kill "$controller" 2>/dev/null || true
  wait "$controller" 2>/dev/null || true
  set_jobs server-parallelism.json 8
}
trap cleanup EXIT
builder=localhost/code-corpora-build:expanded
if [ -s artifacts/build-compat-image.json ]; then builder=localhost/code-corpora-build:compat; fi
python3 repo/containers/build_servers.py --image "$builder" \
  --jobs 2 --resume-work --jobs-file /srv/corpus/artifacts/server-supplement-parallelism.json \
  --recipes "$1" --report "$2"
