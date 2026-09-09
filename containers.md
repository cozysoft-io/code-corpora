# Container isolation plan

Publish **three OCI images to private GitHub Container Registry (GHCR)**, built
using rootless Podman on the Google Cloud build server:

1. `code-corpora-build`: everything needed to build all selected grammars and servers.
2. `code-corpora-grammars`: all compiled native/WASM grammars, registered Zed extensions, and runtime support.
3. `code-corpora-servers`: based on `code-corpora-grammars`, adding all built servers and their
   runtime support.

Run disposable instances of these images locally or on Google Compute Engine.
Use a fresh container per build or grammar/server test job; three published
images does not mean three long-lived, shared processes. Prepare dependencies
separately, then build and run offline. Add Google Cloud Batch when scheduling
becomes tedious.

Implementation lives in [containers/](containers/README.md); `./corpus` itself
still does not impose isolation. All three images are published privately under
`ghcr.io/cozysoft-io/` with tag `progress-20260909-2`.
The grammar image has 544 validated parsers, two quarantined parsers, and one
unavailable DuckyScript pin. The server image contains 292 distributions; 248
passed offline LSP initialization, including all 15 newly repaired builds.
The other 44 need runtime or project-configuration investigation. Builder/server
coverage remains incomplete; the remaining 24 version-rebuild failures were
deferred under the limit on expensive repairs.
[images.lock.toml](containers/images.lock.toml) records immutable registry
digests and coverage; the private release includes the detailed runtime report.
The GCE VM is stopped, with its 50 GB boot disk and 450 GB data disk retained.
Build artifacts, logs, caches, and OCI archives remain on the data disk.

The deliverables remain three reusable images, a small runner, and reproducible
build recipes. Documentation and local command availability were checked
on 2026-09-08; local Podman reports version 5.8.6.

## Local source edits and Zed

Use [`containers/dev`](containers/README.md#editing-grammars-and-servers-locally)
to build editable checkouts into persistent `.corpus/dev/` outputs and prepare a
dedicated stock-Zed profile. A CSV native/WASM build and Bruno server have been
exercised locally. Generalize this verified path into the three release images:
include registered extensions and both grammar formats in the grammar image,
and explicit server launch maps in the derived server image. Preserve source
hashes for local overrides; keep released inputs pinned. Bulk packaging remains
pending and does not change the contents of the existing progress release.

## The three images

| Image | Contents | Base and intended use |
| --- | --- | --- |
| `code-corpora-build` | All required compilers, SDKs, build tools, pinned toolchain versions, dependency sources/packages for offline builds, and build recipes | Pinned Linux distribution; build every selected target and prepare project dependencies |
| `code-corpora-grammars` | All compiled parsers/scanners, grammar catalog, Tree-sitter runtime, shared libraries, and grammar test/benchmark harness | Compatible minimal Linux runtime; grammar-only tests and benchmarks |
| `code-corpora-servers` | Everything in `code-corpora-grammars`, plus all server distributions, launchers, runtime dependencies, and LSP harness | `FROM code-corpora-grammars@sha256:...`; LSP collection and combined tests |

Use the same distribution release and `linux/amd64` initially for all three.
Build against runtime-compatible system libraries and test on a clean runtime
image. A later ARM release needs its own native builds and validation.
`code-corpora-grammars` copies validated outputs from build staging; it does not inherit
the builder's SDKs, dependency caches, or intermediate files. `code-corpora-servers`
inherits the exact released grammar image digest, preserving its layers.

Install grammars at `/opt/corpus/grammars/NAME/` and servers at
`/opt/corpus/servers/ID/`, with machine-readable catalogs mapping the existing
selection names, grammar subdirectories, and LSP IDs to artifacts and launch
commands. Keep incompatible toolchain/server versions in separate prefixes;
launchers set their own environment rather than changing a global default.
Include interpreters, JREs, Node packages, DLLs, and similar dependencies where
required: a built server is a runnable distribution, not necessarily one native
binary. Include toolchains needed during indexing as well as server startup.

The builder must support the entire selection, not just a few language families.
Inventory recipes first and add every required SDK/version and offline dependency
snapshot. Selected source checkouts remain separate pinned inputs; the published
builder carries the other prerequisites. Per-project corpus dependencies remain
job inputs prepared with the builder, rather than being bundled into the runtime
images. No image contains corpus checkouts, private `lsp-data`, credentials, or
benchmark results.

"All" is the coverage goal. The 432 source repositories are not 432 independently
runnable servers; resolve the actual server IDs and their implementations first.
Attempt every selected grammar and server, and record `built`, `unavailable-pin`,
`unsupported-platform`, `license-restricted`, or `failed` with concrete reasons.
Keep working through failures; do not quietly shrink the selection. Known missing
pins and unavailable/proprietary implementations in [SOURCES.md](SOURCES.md) may
prevent literal completeness. Publish the coverage report with the images, and
label incomplete releases honestly. No silent replacement with latest versions.

## What needs isolation

The selection files currently pin 547 grammar checkouts and 432 server/source
repositories. Fetching them does not install or run them. Source pins also do
**not** identify the server binaries used by Zed or historical LSP collection;
see [SOURCES.md](SOURCES.md).

Treat these operations as execution of untrusted code:

- Compiling grammars, evaluating `grammar.js`, running generators, and loading
  native parsers or external scanners. Put the **process loading the grammar**
  inside the container; containerizing only compilation is insufficient.
- Installing servers and dependencies, including package lifecycle scripts,
  Python build backends, Cargo build scripts/proc macros, and project build tools.
- Starting servers, indexing projects, and running upstream tests. Repository
  configuration can select plugins, commands, toolchains, and downloads.
- Dependency verification: `./corpus verify` can execute a repository's virtualenv
  Python and run `cargo metadata`. Move these checks inside the same environment
  used for collection. Metadata-only checks should eventually be separable.

Protect home-directory files, credentials, other projects, the network, and
existing results. Bound CPU, memory, processes, storage, and elapsed time.
Isolation does not prove that a server's answers are correct or that a downloaded
artifact is trustworthy.

Rootless Podman avoids a privileged container daemon and uses user namespaces;
configure subordinate UID/GID ranges and cgroup v2 resource delegation. See the
[Podman rootless documentation](https://docs.podman.io/en/latest/markdown/podman.1.html#rootless-mode).
Containers still share the host kernel. Keep the kernel/runtime patched; for
deliberately hostile code or sensitive workloads, run this design inside a
disposable VM too. A dedicated local Unix account with an empty home is a useful
additional boundary, particularly for download/build work.

## Three phases, with narrow inputs

| Phase | Network | Inputs and persistent writes |
| --- | --- | --- |
| Fetch | Enabled explicitly | Public source pins and dependency manifests; disposable download staging |
| Build/prepare | Off by default | Selected source and downloaded dependencies; job-specific build workspace |
| Test/benchmark/collect | Off | Prepared image, selected project and fixtures; one new result directory |

Use a trusted downloader with clean Git/package-manager configuration. Do not
inherit host credential helpers, SSH agents, Git hooks, filters, or global package
configuration. The current `git_environment()` inherits the host environment;
its LFS and prompt settings are not a sandbox. Fetch into dedicated staging and
verify pins/hashes there. Handle archive extraction inside isolation too.

Some package managers execute code even during dependency preparation. Run those
steps in a disposable container without secrets or private corpus data. Prefer
download-only modes with scripts disabled, then execute scripts offline. If a
tool genuinely requires an online build, give that job an explicit exception in
its recipe, restricted egress, and only public inputs. A normal container network
does not constitute an egress allowlist: implement restrictions outside the
untrusted process, such as a controlled proxy plus enforced network rules. Use a
disposable VM if enforcing this locally becomes complicated.

Private `lsp-data` is optional. Fetch it through a trusted process separately and
stage only the files a particular offline job needs. Never provide private data
to an online preparation job. Disabling telemetry in server configuration is
useful, but offline execution supplies the enforceable privacy boundary.

Build our own reviewed Containerfiles with small, explicit build contexts; never
use the entire checkout as the context or automatically execute upstream
Dockerfiles. Pin base images by digest and dependencies by lockfile/checksum.
Podman build networking is controlled separately from run networking; explicitly
set it for build `RUN` steps. See [Podman build options](https://docs.podman.io/en/latest/markdown/podman-build.1.html#network-mode-net).

## Local runner contract

Add a small `containers/run` wrapper that owns the isolation policy. Accept a job
description, not arbitrary extra Podman flags. The trusted launcher chooses the
image, paths, resource profile, timeout, and output destination. The image contains
the harness and launches the selected server or grammar worker. LSP can use stdio
within the container; loopback also works for servers needing local TCP.

Start with these rules:

- Mount only a staged job input directory read-only. Do not mount the repository
  root, home directory, `.ssh`, cloud configuration, runtime directories, devices,
  or Docker/Podman sockets. Avoid host PID, IPC, and network namespaces.
- Supply a fresh writable workspace and home. Copy the project into that workspace
  when servers need generated files, `node_modules`, or adjacent build products.
  Use fixed paths such as `/work/corpus/train/NAME` and
  `/work/corpus/.corpus/build/train/NAME`, also for `test/NAME` jobs.
- Stage source without `.git` by default; never expose host worktree metadata or
  local Git configuration. Jobs needing Git get a sanitized disposable repository.
  Preserve relative source symlinks, but reject staging that follows links outside
  the selected inputs. Rebuild path-dependent artifacts at their container paths.
- Pass an explicit environment allowlist. Keep credentials, proxy secrets, and
  host paths out of image layers, arguments, and job metadata.
- Only a new, empty per-job output directory is writable on the host. Existing
  observations and inventories remain inputs, never an output mount.

The following is the intended launch shape, **not a complete runnable wrapper**.
`JOB_INPUT`, `JOB_OUTPUT`, and `JOB_IMAGE` are supplied by that wrapper; the image
is already present under an immutable digest or local image ID. The reviewed
image must provide `/opt/harness/run` and its mount points. Input staging is
immutable during execution; output lives on scratch storage with an enforced
per-job quota. The wrapper captures stdout/stderr with byte limits.

```bash
podman run --rm --pull=never \
  --network=none --http-proxy=false \
  --userns=keep-id --user "$(id -u):$(id -g)" \
  --cap-drop=ALL --security-opt=no-new-privileges \
  --read-only --read-only-tmpfs=false \
  --pids-limit=512 --memory=8g --memory-swap=8g --cpus=2 \
  --timeout=1800 --ulimit=core=0:0 --log-driver=none \
  --tmpfs /tmp:rw,nosuid,nodev,noexec,size=512m,mode=1777 \
  --tmpfs /work:rw,nosuid,nodev,size=4g,mode=1777 \
  --volume "$JOB_INPUT:/input:ro,Z" \
  --volume "$JOB_OUTPUT:/out:rw,Z" \
  --env HOME=/work/home --env XDG_CACHE_HOME=/work/cache \
  --workdir /work --entrypoint /opt/harness/run \
  "$JOB_IMAGE" /input/job.json
```

These options remove networking and privilege escalation, preserve caller-owned
outputs, and limit resources. Retain the default seccomp policy and host
SELinux/AppArmor confinement. `:Z` relabels dedicated staging for a private
container; do not apply it to original shared checkouts. See the
[Podman run reference](https://docs.podman.io/en/latest/markdown/podman-run.1.html).

The numeric limits are a starting profile, not universal requirements. `/work`
allows execution for compilers and generated binaries; direct temporary build
files there if `/tmp` being `noexec` causes problems. Tmpfs consumes the memory
budget. Larger projects should use bounded disk scratch with the same layout.
Memory/PID limits and deadlines do not limit total output bytes: enforce disk
quotas or use a capacity-limited scratch filesystem, and cap logs separately.
Fail early when required limits cannot be enforced, rather than silently omitting
them. Track the container ID so cancellation and launcher failure also clean up
the whole container, including child processes.

## Building on the supplied Google Cloud server

The VM is `corpus-builder` in `mgsloan-compute/us-central1-a`; connect through IAP.
It uses `e2-standard-16` (16 vCPUs/64 GB RAM), a 50 GiB boot disk, and a preserved
450 GiB XFS data disk. N2 capacity was unavailable, and the 500 GiB SSD quota
limited disk sizing. [cloud.json](containers/cloud.json) records this configuration.
Use private GHCR packages under `cozysoft-io`; a separate private GitHub Actions
publisher supplies its own temporary package credential.
The Linux x86-64 VM has cgroup v2 and expandable storage.
Size parallelism from measured peak memory/disk use, starting with
low concurrency for large builds such as LLVM/JVM projects. Keep Podman storage,
source snapshots, and resumable build artifacts on a dedicated data disk; impose
per-job bounds so a failed build cannot fill the boot disk. Build-server capacity
is separate from the smaller runtime benchmark profiles below.

The main server queue maintains eight workers; while a supplemental recipe queue
runs, it uses six main workers plus two supplemental workers. Each job is capped
at two CPUs and 10 GiB; the shared `corpus` user slice
throttles above 50 GiB and has a 56 GiB hard limit. Watch CPU, memory pressure,
and failures when adjusting concurrency; dependency downloads and single-threaded
build stages will not keep all 16 CPUs busy.

The host supervisor performs this sequence:

1. Resolve the selection into pinned recipes and dependency locks. Assemble and
   validate `code-corpora-build`, including everything needed for offline compilation.
2. Start fresh instances of that builder for each target, with selected inputs
   read-only and a private build directory. Never let one upstream build modify
   the toolchains or another target's output. Checkpoint successful artifacts so
   interrupted builds resume without rebuilding the entire collection.
3. Assemble `code-corpora-grammars` from validated grammar artifacts, then assemble
   `code-corpora-servers` using that grammar image digest as its base. Use reviewed
   Containerfiles, not `podman commit` of a mutable build session.
4. Run every artifact's smoke tests in its final image, plus boundary checks and
   representative harness tests. A successful compilation alone is insufficient.
5. Push all three images and their coverage/build metadata to private GHCR.
   Pull by digest onto a clean worker and repeat the smoke tests before
   marking the release ready. Preserve required source/license notices with the
   artifacts and publish no credentials or private data.

The builder is an image used by host Podman; it does not need Podman-in-Podman or
a mounted runtime socket. Keep registry authentication in the trusted publishing
process. Prefer no service account on the compilation VM, transferring artifacts
to a trusted publisher or authenticating only after untrusted jobs stop. If a host
identity is used for Google Cloud storage or job reporting, grant only the needed
permissions and keep metadata unreachable from build containers, including any
online preparation exceptions. That identity does not authenticate to GHCR.

## Caches and results

Cache downloads by content hash and builds by source SHA, dependency lock hashes,
toolchain/image digest, architecture, and build flags. Give each preparation job
its own writable cache. Promote validated artifacts into immutable snapshots;
consumers copy them into private writable caches when tools require writes. Do
not share mutable package caches or build directories between untrusted jobs.
Hashing identifies an artifact; it does not establish that its producer was safe.

Record an explicit executable lock: server package/release version, download URL
and checksum or build recipe, source SHA where applicable, and final image
digest. Also record grammar subdirectory, parser/scanner hashes, Tree-sitter ABI
and runtime version. Keep missing source pins or unsupported servers as explicit
skips; never substitute upstream HEAD or a latest binary silently.

Write each run under `.corpus/runs/RUN_ID/`, including a job manifest, structured
results, bounded logs, and exit status. The trusted supervisor records image and
input digests, limits, timings, timeout/OOM status, and harness revision separately
from the workload's claims. Use JSON/JSONL for interchange; do not deserialize
untrusted pickle files or execute generated scripts on the host.

After the container exits, validate output names, sizes, schemas, and hashes;
accept regular files only and reject links, devices, and path traversal. Escape
control characters when displaying logs. Import approved observations into
`lsp-data` in a separate trusted step, respecting its inventory and
[migration rules](lsp-data/MIGRATION.md). Containers cannot overwrite old results
or commit/publish data. Logs and observations can contain source text, so keep
them private by default and apply a retention policy.

## Reproducible benchmarks

Use exactly the same immutable image, input snapshot, harness, and internal paths
locally and in Google Cloud. Containerization reproduces userspace, not the CPU,
kernel, filesystem, or scheduling behavior.

- Separate preparation time, container startup, server startup/indexing, and
  steady-state requests or parsing. Never download dependencies during timing.
- Run one benchmark job per worker VM; reuse its container for multiple samples
  to amortize startup. Specify warmups, repetitions, seeds, request order, cache
  state, and thread counts. A fresh container does not clear host page caches.
- Record CPU model/architecture, VM machine type and CPU platform, kernel,
  Podman/runtime versions, storage, resource limits, compiler flags, and image
  digest. Avoid emulation and accidental `-march=native` differences.
- Use CPU quotas for ordinary tests. For precise timing, use a dedicated worker
  and explicit CPU affinity; avoid quota throttling during measured work, and
  record the chosen policy. Keep memory, process, and wall-clock bounds.
- Compare implementations on the same worker with interleaved trials and report
  distributions. Treat OOM, timeouts, and interrupted trials as failures, not
  unusually fast samples. Use ordinary VMs for timing; Spot capacity is suitable
  for retryable correctness matrices.

## Image storage: private GitHub Container Registry

Use **GitHub Container Registry (`ghcr.io`)** for all three images, under the
`cozysoft-io` organization. Keep each package private:

```text
ghcr.io/cozysoft-io/code-corpora-build:RELEASE
ghcr.io/cozysoft-io/code-corpora-grammars:RELEASE
ghcr.io/cozysoft-io/code-corpora-servers:RELEASE
```

Record immutable digests in `containers/images.lock.toml`; release tags are human
labels, while builds and benchmarks resolve by digest. Keep the grammar parent
digest in the server image metadata. This storage can outlive the build VM; do
not treat its local Podman cache as the only copy.

As checked on 2026-09-08, GitHub provides free container image storage and
bandwidth, including private container images; this is a specific Container
Registry policy, separate from ordinary
GitHub Packages quotas. It is not a promise of perpetual free hosting. See
[GitHub's billing policy](https://docs.github.com/en/billing/concepts/product-billing/github-packages).
Public visibility is unnecessary for the current free policy. GHCR supports OCI
images but limits each layer to 10 GB and upload duration to 10 minutes.
Split large SDK/dependency bundles into modest layers;
avoid one enormous `COPY`. See [GHCR documentation](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry).

Keep the already published progress snapshot as a recovery checkpoint. Wait for
the remaining builds and validation to finish before publishing another release;
do not upload periodic progress snapshots. Local build results still checkpoint
normally. The publisher is manually dispatched, with no schedule or per-build
trigger. Publishing consumes GitHub Actions minutes (potentially billable beyond
the included allowance) and requires transferring archives out of Google Cloud,
even though retaining the images in GHCR is currently free. See
[Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions).

Publication uses the private
[`cozysoft-io/corpus-containers`](https://github.com/cozysoft-io/corpus-containers)
repository, deployed from `containers/publisher/`. All three organization packages
have been verified private. Previous `mgsloan` digest records remain in Git history.
Transfer small OCI archives through the trusted local machine into private release
assets. For large archives, use temporary private Cloud Storage and object-specific
signed PUT/GET URLs. The latest release used this path; its temporary bucket and
signer have been removed, while the archives remain on the GCE data disk.
A reviewed workflow
checks archive/chunk hashes and expected image configuration digests, then uses
`skopeo copy --preserve-digests` to upload without executing the images. It checks
repository/package visibility and refuses existing public packages. Its temporary
`GITHUB_TOKEN` has `contents: read` and `packages: write`; no GitHub credential is
sent to the build VM. See [GitHub Actions package authentication](https://docs.github.com/en/packages/managing-github-packages-using-github-actions-workflows/publishing-and-installing-a-package-with-github-actions).

Pull-only workers authenticate host-side using `read:packages` with access to the
private packages. A classic token with `write:packages` is an alternative for a
trusted manual publisher. Supply credentials through password-stdin and a
dedicated host-side auth file, and remove temporary credentials afterward. Never
put tokens in build arguments, image layers, workload environment variables, or
mounted directories. Runtime image pulls happen before starting offline
containers. GitHub documents these scopes in the
[registry authentication guide](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry#authenticating-to-the-container-registry).

Uploading from the Google build VM to GHCR can still incur Google Cloud Internet
egress; build compute and disks also cost money. The configured registry prefix
is `ghcr.io/cozysoft-io`. Do not provision Artifact Registry or
mirror images to a second registry as part of this plan.

Share unchanged layers, put stable toolchains before changing dependencies, and
never squash the server image's inherited grammar layers. Retain the current and
previous release plus digests referenced by saved benchmarks; prune unreferenced
failed builds and stale caches. Measure download/unpacked sizes and disk peaks as
part of each release. Large aggregate images trade simple distribution for large
initial pulls; grammar-only users need only the grammar image.

## Google Cloud runtime: start with Compute Engine

Use a dedicated project or narrowly scoped environment and a disposable Linux VM
with the same Podman wrapper. Bake a reviewed VM image with Podman and its rootless
user/cgroup configuration. Bootstrap via a startup script or cloud-init; the old
Compute Engine container startup agent is deprecated. See Google's
[deployment guidance](https://docs.cloud.google.com/compute/docs/containers/deploying-containers).

The simplest strong separation for initial benchmarks is a worker with **no
attached service account**. A trusted controller stages the OCI image and inputs
on disks or transfers them before execution, then retrieves results afterward.
The worker needs no registry or bucket credentials. Configure no external IP and
restricted VPC access; arrange administration through an approved private path
such as IAP. `gcloud compute instances create` supports `--no-service-account`,
`--no-scopes`, and `--no-address`; see its
[reference](https://docs.cloud.google.com/sdk/gcloud/reference/compute/instances/create).
Use explicit VM image versions, resource limits, and automatic expiry/cleanup.

Still run workload containers with `--network=none`. Removing an external IP does
not remove internal connectivity or metadata access. The metadata server can
expose instance/project information and attached service-account credentials;
never put secrets in metadata. Do not rely on VPC firewall rules alone to protect
metadata. See [VM metadata](https://docs.cloud.google.com/compute/docs/metadata/overview)
and [service-account access](https://docs.cloud.google.com/compute/docs/access/service-accounts).

Use the published images from private GHCR; keep inputs/results in separate
private Cloud Storage buckets if needed. Only a trusted host supervisor
fetches/uploads; the offline container gets staged files.
Use a dedicated minimal Google worker identity for reading required inputs,
creating new result objects, and reporting job status as needed; GHCR pulls use
the separate host-side GitHub credential described above. Avoid project-wide Editor,
service-account keys, credentials in mounts, and a bucket containing unrelated
private data. Choose result object paths in the supervisor, never from workload
output. A kernel escape could reach host identity, which is why the identity-free
worker is the preferred first version.

### Add Batch for larger matrices

Batch supports script or container tasks. Use a **trusted script task on a
compatible VM image** to invoke our rootless Podman wrapper; do not assume a
plain managed container task inherits the local isolation policy. Provision
Podman/user namespaces and the Batch agent in that image, and test them together.
This design runs Podman on the task VM, without privileged container nesting.
See [Batch job creation](https://docs.cloud.google.com/batch/docs/create-run-basic-job).

Batch workers require an appropriate service account, including agent reporting
permissions; keep it separate from submission/build identities. Preserve the
offline inner container and trusted transfer supervisor. See
[Batch agent troubleshooting](https://docs.cloud.google.com/batch/docs/troubleshooting).
Start with one task per VM, explicit CPU/memory sizing, concurrency limits, finite
retries, and unique attempt directories. Use Spot workers for resumable tests;
publish a completion manifest only after validated uploads finish. Bound job
duration and worker count, set storage lifecycle rules, and delete leftover disks.
Budget alerts are useful notifications, not spending caps.

Defer Kubernetes and Cloud Run Jobs: this workload first needs controllable
execution and comparable machines. A small Compute Engine runner, followed by
Batch scheduling if needed, keeps the moving parts manageable.

## Implementation order and acceptance checks

1. **Recipes and three-image skeleton.** Add `containers/run`,
   `Containerfile.build`, `Containerfile.grammars`, `Containerfile.servers`,
   a minimal job schema, executable/dependency locks, and coverage inventory.
   Integrate the actual consumer harnesses (`heuristic-jump` and `tree-squatter`)
   explicitly; their runners are not implemented in this repository. Move
   dependency preparation and execution-based verification into containers.
2. **Verify the boundary.** Use harmless fixture jobs to attempt reading a host
   sentinel, writing staged inputs, reaching Internet/host/metadata addresses,
   and accessing runtime sockets. Check limits with bounded allocation, output,
   and child-process probes; confirm cancellation removes descendants. Test
   malicious output links and that credentials/proxy variables are absent.
   Run these checks on each local/cloud host profile before real workloads.
3. **Compile the complete selection on the supplied VM.** Bootstrap with one
   grammar and one server, then expand the builder and recipes to every selected
   target. Resume from cached successes and investigate failures. Run repository
   unit tests in the builder and smoke-test every built grammar/server in its
   runtime image. Exercise external scanners, stdio LSP, generated project files,
   and offline cache misses. Missing dependencies must be visible failures.
4. **Publish and reproduce.** Upload all three images to private GHCR, record
   digests and coverage, and reproduce a representative matrix
   after pulling onto a clean local account and disposable cloud worker.
5. **Benchmark, then scale.** Compare correctness and inspect timing variance
   before adding Batch or parallel runtime workers. Retain image digests needed
   to reproduce results after the build VM has been deleted.

Delivery is complete when all selected targets have a recorded outcome, every
built artifact passes its runtime smoke test, the three images are stored in the
user's GitHub account or organization, and jobs run locally and in Google Cloud
without exposing host credentials or original writable checkouts to workloads.
Report unresolved targets explicitly alongside
the release rather than claiming unsupported targets were compiled.
