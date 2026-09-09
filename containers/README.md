# Corpus container builds

The build VM is `corpus-builder` in `mgsloan-compute/us-central1-a`.
[cloud.json](cloud.json) records its configuration. It has no service account,
uses IAP for SSH, and automatically stops after 12 hours from startup. The 450 GiB
data disk is preserved when the VM is deleted; retained disks still incur charges.
The batch finisher reassembles/tests the server image, exports portable OCI
archives, and powers off the VM after the first pass. To keep it running afterward,
create `/srv/corpus/keep-running`. The 12-hour Compute Engine stop remains a backstop.
The E2 machine has 16 vCPUs/64 GB RAM; N2 was unavailable and the SSD quota limited
the combined boot/data disks to 500 GiB.

These are initial images and build automation, not a completed all-server release.
The builder includes common SDKs plus checksum-pinned Rust, Go, and Node releases.
Per-target dependency caches and additional toolchains still need to be folded
into the final builder as coverage expands. See [the plan](../containers.md).

## Inspect the live build

```bash
containers/cloud
containers/cloud 'tail -20 /srv/corpus/logs/server-build.log'
containers/cloud 'sudo systemctl status corpus-server-build --no-pager'
containers/cloud 'cd /srv/corpus && python3 repo/containers/status.py'
```

The current release-pin rebuild runs as `corpus-server-versions-heavy` and
`corpus-server-versions-regular`. `artifacts/version-rebuild-current.json` points
to its queues, logs, source-update results, and archived old artifacts. It includes
all 194 previously built servers whose commits changed, plus 48 additional attempts.
The other changed entries are 64 needing recipes and nine extension-only repositories.
Four ordinary jobs run alongside the eight-CPU clangd build, increasing to eight
when clangd finishes. Grammars keep their existing pins and artifacts.

`rebuild_versions.py --prepare` applies `server-releases.json` after compilation
is paused; `--start` launches its queues. Checkouts with unexpected commits or local
changes are preserved and reported. Image assembly rejects stale server artifacts,
and status counts only results matching the current selection.
The finisher assembles `code-corpora-servers:versions-RUN_ID`, runs startup probes,
exports OCI archives, and stops the VM. It does not publish another GHCR snapshot.

Host supervision runs as root only to allocate XFS quotas and configure network
rules. All compiler, installation, parser, and LSP processes run as the unprivileged
`corpus` user inside rootless containers. A separate container performs public
dependency preparation with Internet access; compilation runs with no network.
Build contexts contain only the reviewed Containerfiles/scripts and staged outputs.
Do not run upstream build commands directly on the VM host.

The first-pass server queue uses generated recipes for Cargo, Go, npm, and Python.
Reviewed overrides in `recipes.extra.json` and `recipes.next.json` add pinned
submodule fetching, nested packages, CMake, pnpm, and .NET builds. The extra and
next queues run separately from the first pass and checkpoint their own reports.
`recipes.more.json` adds repairs plus Gradle, Cabal, Zig, Erlang, and Meson jobs.
`recipes.jvm.json` adds Maven and Java 25 targets after that queue finishes.
`status.py` merges their recipe coverage for a current summary.
The main queue now maintains eight concurrent builds. `run-supplement.sh` assigns
six main workers and two supplemental workers, then restores eight main workers
when the supplement finishes. Each job is capped at two CPUs and 10 GiB.
The newer supplemental queue increases to eight workers after the main queue
finishes, or four while the separately scheduled eight-CPU LLVM build is active.
The `corpus` user slice has a shared 50 GiB
memory throttle and 56 GiB hard limit to leave room for the host. Individual
download and single-threaded stages can still leave CPUs idle.
`artifacts/server-parallelism.json` controls the main queue's live worker limit;
replace it atomically to adjust concurrency without restarting compilation.
`--resume-work` retains intermediate files only for an identical recipe and
builder image. Per-target locks prevent overlapping new supervisors.
Complex monorepos, other build systems, and integrations require additional recipes;
`needs-recipe` is unfinished work, not a claim that those targets cannot be built.
Each build has its own source copy, dependency cache, disk quota, deadline, and
logs. Explicit submodule mirrors retain the exact commit recorded by the parent
repository. Internal absolute symlinks are made relative when packaging, and
links outside the package are rejected. Completed artifacts are checkpointed under `/srv/corpus/artifacts/`.

## Images and reports

- `localhost/code-corpora-build:toolchains`: current build image.
- `localhost/code-corpora-build:expanded`: adds checksum-pinned .NET 9 and 10 SDKs.
- `localhost/code-corpora-build:compat`: additional pinned Rust, Go, Zig, Elixir, GHC, Java,
  and Cabal toolchains, plus native dependencies for the repair queues. Consult
  `artifacts/build-compat-image.json` for the completed revision; an expansion
  may still be building.
- `localhost/code-corpora-grammars:initial`: grammar runtime, including an explicit
  quarantine directory for parsers that failed smoke tests.
- `localhost/code-corpora-servers:initial`: an early snapshot based on that grammar image.
  Reassemble it to include servers built after the snapshot.
- `localhost/code-corpora-servers:progress2`: later snapshot with 63 successful LSP
startup probes, 14 without an initialize response, and one catalog entry whose
  artifact missed the snapshot. A finished batch becomes
  `localhost/code-corpora-servers:batch1`.

`runtime_checks.py servers --image BUILDER --artifacts /srv/corpus/artifacts/servers`
checks completed artifacts before aggregate assembly. These preliminary results
live under `runtime-checks/build-artifacts/` and do not validate the final runtime
image. Each probe mounts only its own server read-only. Probe versions are copied
into each report directory, and failures include bounded stderr/protocol diagnostics.

Use full image IDs/digests for execution. Host-local IDs and runtime test reports
are stored in `/srv/corpus/artifacts/*-image.json` and
`/srv/corpus/artifacts/runtime-checks/`. The canonical per-server outcomes are
`/srv/corpus/jobs/server-NAME/result.json`; aggregate reports are checkpoints.
`built-unverified` means compilation succeeded but LSP startup has not been verified.
A successful LSP `initialize` is a smoke test, not correctness validation.
Server probes use a fresh offline container per repository, with an independent
home, process namespace, resource limits, and report directory. Results are
checkpointed under `runtime-checks/servers/IMAGE-PROBE-RUN/summary.json`.
Portable archives and their SHA-256 files are stored in
`/srv/corpus/artifacts/oci/`; these can be loaded without reconstructing the
original Podman user's UID mapping.

The selected Rust grammar was recovered from the 0.24.2 crate after checking its
archive checksum and `.cargo_vcs_info.json` against the selected Git SHA.
`recover_rust.py` records that provenance without changing the selection.

## Runtime use

The local host needs Podman, `newuidmap`/`newgidmap`, subordinate UID/GID ranges,
and cgroup v2 delegation. Both the cloud host and local development host have
these configured. Online preparation also needs a Podman network helper
(`slirp4netns` or `pasta`) on `PATH`.

After securely pulling a published image by digest, use the rootless wrapper:

```bash
containers/run IMAGE_DIGEST STAGED_INPUT_DIRECTORY -- \
  /opt/corpus/python/bin/python /opt/corpus/worker.py \
  smoke-grammar /opt/corpus/grammars/python

containers/run SERVER_IMAGE_DIGEST STAGED_INPUT_DIRECTORY -- \
  python3 /opt/corpus/launch_server.py REPOSITORY EXECUTABLE
```

`/input` is read-only. `/work`, `/tmp`, and `/out` are bounded temporary filesystems.
Stream results through stdout; temporary output disappears when the container exits.
The cloud batch supervisors additionally support persistent output directories
protected by XFS quotas. No host home, credentials, or runtime sockets are mounted.

## Editing grammars and servers locally

`containers/dev` builds working-tree contents, including uncommitted files, without
modifying the checkout. Outputs, caches, logs, and a dedicated Zed profile live in
`.corpus/dev/`. Builds use rootless containers capped at two CPUs and 4 GiB.
Only the selected source and target's build/output directories are mounted.

Extend a locally available builder with pinned Tree-sitter and WASI tools:

```bash
podman build --pull=never --http-proxy=false --network=private \
  --cpu-period=100000 --cpu-quota=200000 --memory=4g \
  --build-arg BUILDER_IMAGE=BUILDER_IMAGE_ID \
  -f containers/Containerfile.build-dev -t localhost/code-corpora-build:dev containers

containers/dev grammar csv --image localhost/code-corpora-build:dev
containers/dev server bruno-language-server --image localhost/code-corpora-build:dev \
  --recipe containers/recipes.resumed-fixes.json --prepare-online
```

The inherited builder must contain the target's SDKs. Grammar builds regenerate
`parser.c` and compile native and WASM artifacts; use `--no-generate` to test edits
to generated C directly. `--source PATH` selects an alternate checkout. Server
recipes use the same format as the batch recipes. Builds default to 2 CPUs and
4 GB RAM; use `--memory 8g` for targets that need more memory. `--timeout 600`
limits each phase to ten minutes for inexpensive repair attempts. Dependency preparation is
offline unless `--prepare-online` is explicit; compilation is always offline.
Local online preparation does not have the VM's private-address firewall rules,
so use public inputs only. Source snapshots must already contain required nested
checkouts. Successful builds atomically replace the target's override; failed
builds retain the previous artifact. Artifact metadata records input hashes,
source HEAD when available, and the resolved builder image ID.

To include completed local outputs in the VM's next aggregate, copy their target
directories to the VM and run `sudo python3 repo/containers/import_servers.py
/path/to/servers` from `/srv/corpus`. `--check` validates without importing. Imports
verify pins and hashes, respect build locks, retain previous failure records, and
still require the aggregate's runtime checks.

For additions to an already assembled image, run `assemble.py servers --add-to
BASE_SERVER_IMAGE --tag TAG`. This preserves existing layers and copies only new
distributions. It rejects changed source selections or replaced base artifacts;
those require full assembly. Check the added servers in the resulting image before
publishing it.

Prepare exact registered extension versions from `zed-sources.toml`:

```bash
containers/dev extension csv --image localhost/code-corpora-build:dev
containers/dev extension bruno --image localhost/code-corpora-build:dev
```

Downloads are cached with SHA-256 provenance and unpacked inside an offline
container. For a grammar-only Zed profile:

```bash
containers/dev profile --extension csv
containers/dev zed /absolute/path/to/example.csv
```

To enable servers, provide a JSON map keyed by every language-server ID in the
selected extensions. For Bruno, save this as `.corpus/server-map.json`:

```json
{"bruno-language-server": {
  "repository": "bruno-language-server",
  "executable": "bruno-language-server",
  "arguments": ["--stdio"]
}}
```

```bash
containers/dev profile --extension csv --extension bruno \
  --server-map .corpus/server-map.json \
  --server-image localhost/code-corpora-build:dev --project /absolute/path/to/project
containers/dev zed /absolute/path/to/project
```

Prepared extensions retain their registered manifests and receive matching local
WASM overrides. Stock Zed discovers them through profile-local symlinks. The
profile disables audited extension auto-install/update, extension capabilities,
and telemetry. Every enabled server has an explicit launcher into an offline
container. The project is mounted read-only at its original absolute path so LSP
URIs agree; only that server's override is mounted over the image. No host home
or credentials are mounted into the server container. The launcher clears the
LSP initialization process ID, since the editor's host PID is not visible inside
the container, and stops the container when the editor closes its input stream.

After editing, rebuild the target, close the dedicated Zed instance, rerun
`profile`, and reopen it. Avoid Zed's extension rebuild action: it rebuilds the
manifest's Git revision instead of these staged working-tree contents.
`containers/dev reset grammars csv` (or `reset servers NAME`) removes an override
without deleting its outputs. Reprepare/restart afterward; grammar fallback uses
the registered extension package, and server fallback requires an artifact in
`--server-image`. A builder image alone does not supply those server artifacts.

The local pilot verified a CSV edit in both native and WASM execution and an edited
Bruno server's hover response through the generated container launcher.
The dedicated stock-Zed profile also loaded both extensions and kept Bruno running.
Bulk WASM and extension packaging, launch maps for all servers, and corpus dependency
bundling are still pending; these are not yet contents of the published images.

## Resume and assemble on the VM

For the batch halted on 2026-09-09, `resume-batch.py` prints the remaining queues
without starting work. Add `--start` to launch them after restarting the VM:

```bash
containers/cloud 'sudo python3 /srv/corpus/repo/containers/resume-batch.py'
containers/cloud 'sudo python3 /srv/corpus/repo/containers/resume-batch.py --start'
```

It preserves completed targets, uses saved SDK images for interrupted LLVM and
Buck2 builds, and serializes supplemental queues. It refuses to start alongside
active build services or containers. The plan is saved in
`artifacts/resume-batch-plan.json`; service logs end in `-resumed.log`.
It removes the halt marker so the batch finisher again assembles, checks, exports,
and powers off the VM. This does not publish a new registry snapshot.

Run these through the trusted administrator in `/srv/corpus`, avoiding overlapping
invocations for the same target:

```bash
sudo python3 repo/containers/build_grammars.py --image localhost/code-corpora-build:initial --jobs 6
sudo python3 repo/containers/build_servers.py --image localhost/code-corpora-build:toolchains --jobs 8 --resume-work
sudo python3 repo/containers/assemble.py grammars
sudo python3 repo/containers/assemble.py servers
sudo python3 repo/containers/runtime_checks.py grammars
sudo python3 repo/containers/runtime_checks.py servers
```

Run `check-boundaries.sh` before real workloads on a new host/profile. The boundary
probes cover namespace/privilege/resource settings, read-only inputs, missing host
files/sockets, and offline/metadata/internal network denial. They do not prove
resistance to kernel vulnerabilities. Keep the VM disposable and patched.

The existing progress release uses private
`ghcr.io/mgsloan/code-corpora-{build,grammars,servers}` packages. The intended
namespace for the next release is `ghcr.io/cozysoft-io/`; existing lock records
continue to identify the actual published digests.
The private [publishing repository](https://github.com/cozysoft-io/corpus-containers)
is deployed from `publisher/`.
`upload_release.py` targets this organization repository; the workflow publishes
under its owner's GHCR namespace and checks organization package visibility.
Associate the packages with `cozysoft-io/code-corpora` and grant the publisher
Actions access. The publisher uses GitHub Actions' temporary package token. No additional personal access token
is needed for upload. `publisher/` contains the reviewed workflow and transfer code.
`prepare_upload.py` splits OCI archives into checksummed private release assets;
the workflow verifies those hashes and image IDs before copying to GHCR without
executing image contents. Both repository and package privacy are checked.
No GitHub credentials belong in the images, build jobs, or source tree.
Pulling private packages locally still requires host-side registry authentication.

Registry references and verified visibility are recorded in
[`published-images.json`](published-images.json); [`images.lock.toml`](images.lock.toml)
also records coverage and immutable IDs. Publishing a progress snapshot does not
mean every selected server is built or runnable.

Keep the existing progress release as a checkpoint; wait for the remaining builds
and validation before the next publication. Do not publish periodic snapshots.
The workflow runs only on manual dispatch. Local compilation and checkpointing
continue independently of publication.

For small snapshots, download OCI archives and SHA-256 files through IAP.
For large archives, use temporary private Cloud Storage: a dedicated signer grants
object-specific PUT/GET URLs, and `upload_signed.py` uploads directly from the VM.
Run `prepare_upload.py --manifest-only` there and set each image's `archive_url`
in the private release manifest to its signed GET URL. No cloud or GitHub account
credentials are copied to the VM. Keep URL files private, and delete the temporary
bucket and signer after verifying publication.

Run `prepare_upload.py --help`, create
a private prerelease in the publisher repository, then run:

```bash
python3 containers/upload_release.py --release RELEASE --directory STAGED_ASSETS \
  --kind grammars
# After the grammar job succeeds, publish the builder and derived server image.
python3 containers/upload_release.py --release RELEASE --directory STAGED_ASSETS \
  --kind build --kind servers
```

The server publisher verifies that its initial layers match the grammar image
published under the same release tag. Record the `CORPUS_PUBLISHED` results from
the completed workflow logs before updating the image lock file.
