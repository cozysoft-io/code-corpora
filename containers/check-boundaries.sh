#!/bin/bash
# Run as the trusted host administrator, after installing the builder image.
set -euo pipefail
cd /srv/corpus
uid=$(id -u corpus)
gid=$(id -g corpus)
printf 'isolation probe\n' > /srv/corpus/host-only-sentinel
chmod 600 /srv/corpus/host-only-sentinel
bash /srv/corpus/repo/containers/restrict-build-network.sh
for profile in offline online; do
  network=none
  extra=()
  if [ "$profile" = online ]; then
    network=slirp4netns:allow_host_loopback=false
    extra=(--online)
  fi
  sudo -u corpus -H env XDG_RUNTIME_DIR="/run/user/$uid" podman run --rm \
    --pull=never --network="$network" --http-proxy=false --userns=keep-id \
    --user="$uid:$gid" --cap-drop=ALL --security-opt=no-new-privileges \
    --read-only --read-only-tmpfs=false --pids-limit=64 \
    --memory=512m --memory-swap=512m --cpus=1 --timeout=60 --log-driver=none \
    --tmpfs /work:rw,nosuid,nodev,size=64m,mode=1777 \
    -v /srv/corpus/repo/containers:/input:ro -e HOME=/work/home \
    --entrypoint=python3 "${1:-localhost/code-corpora-build:initial}" \
    /input/check_boundary.py "${extra[@]}"
done
