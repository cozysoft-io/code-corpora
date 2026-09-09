#!/bin/bash
# Run as the corpus user; OCI archives are portable backups of the image store.
set -euo pipefail
cd /srv/corpus
export XDG_RUNTIME_DIR="/run/user/$(id -u)"
mkdir -p artifacts/oci
for kind in build grammars servers; do
  tag=initial
  if [ "$kind" = build ]; then
    tag=toolchains
    if [ -s artifacts/build-expanded-image.json ]; then tag=expanded; fi
    if [ -s artifacts/build-compat-image.json ]; then tag=compat; fi
  fi
  if [ "$kind" = servers ]; then tag="${1:-initial}"; fi
  path="artifacts/oci/corpus-$kind-$tag.tar"
  podman save --format oci-archive -o "$path.partial" "localhost/code-corpora-$kind:$tag"
  mv "$path.partial" "$path"
  sha256sum "$path" > "$path.sha256"
done
