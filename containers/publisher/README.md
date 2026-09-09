# Private corpus image publisher

This repository transfers checksum-verified OCI archives from private release
assets to three private GHCR packages. It never builds or executes image contents.
The publish job uses GitHub's temporary `GITHUB_TOKEN`; the build VM has no GitHub
credentials. Source/build automation lives in `cozysoft-io/code-corpora`.

Dispatch `publish.yml` with the release tag after uploading `manifest.json` and
all archive chunks. Each manifest records archive/chunk SHA-256 values and the
expected image configuration digest. Jobs refuse a public repository or an
existing public package, then verify package privacy after upload.

Incomplete snapshots are deliberately tagged as progress releases. A published
image is not a claim of complete server coverage or successful upstream tests.
