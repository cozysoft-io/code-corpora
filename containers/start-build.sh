#!/bin/bash
set -euo pipefail
cd /srv/corpus/repo/containers
export XDG_RUNTIME_DIR="/run/user/$(id -u)"
base=$(podman image inspect docker.io/library/ubuntu:24.04 --format '{{index .RepoDigests 0}}')
printf '%s\n' "$base" > /srv/corpus/artifacts/base-image.txt
podman build --network=slirp4netns --build-arg "BASE_IMAGE=$base" \
  -f Containerfile.build -t "localhost/code-corpora-build:${1:-initial}" .
podman image inspect "localhost/code-corpora-build:${1:-initial}" > /srv/corpus/artifacts/build-image.json
