#!/bin/bash
# Trusted host setup, supplied as Compute Engine startup metadata.
set -euo pipefail
exec > >(tee -a /var/log/corpus-bootstrap.log) 2>&1
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y podman buildah uidmap slirp4netns fuse-overlayfs git python3 \
  python3-venv rsync jq curl ca-certificates xfsprogs
device=/dev/disk/by-id/google-corpus-data
if ! blkid "$device"; then mkfs.xfs "$device"; fi
mkdir -p /srv/corpus
if ! mountpoint -q /srv/corpus; then mount -o prjquota "$device" /srv/corpus; fi
if ! grep -q 'google-corpus-data' /etc/fstab; then
  echo '/dev/disk/by-id/google-corpus-data /srv/corpus xfs defaults,prjquota,nofail 0 2' >> /etc/fstab
fi
if ! id corpus >/dev/null 2>&1; then useradd -m -d /srv/corpus/home -s /bin/bash corpus; fi
mkdir -p /srv/corpus/{repo,jobs,artifacts,logs,storage}
# Preserve existing subordinate-UID ownership in Podman's image store on reboot.
chown corpus:corpus /srv/corpus /srv/corpus/{home,repo,jobs,artifacts,logs,storage}
loginctl enable-linger corpus
mkdir -p /srv/corpus/home/.config/containers
cat > /srv/corpus/home/.config/containers/storage.conf <<'EOF'
[storage]
driver = "overlay"
graphroot = "/srv/corpus/storage"
EOF
chown -R corpus:corpus /srv/corpus/home/.config
touch /srv/corpus/bootstrap-complete
