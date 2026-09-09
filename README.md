# Code corpora

This corpus collects code examples from a variety of languages. It was created
for two [Cozysoft](https://cozysoft.io) projects:

* [`heuristic-jump`](https://github.com/cozysoft-io/heuristic-jump) was the original reason for creating this. It provides language-specific heuristic logic for go-to-definition.

* [`tree-squatter`](https://github.com/cozysoft-io/tree-squatter), an experiment in a more compact representation for Tree-sitter. This corpus is used to check for behavioral equivalence and benchmarking.

# Organization

* `test/` and `train/` contain checkouts of selected open-source repositories. Each sub-folder is a repository.

* `grammars/` and `servers/` contain editable checkouts of the available Tree-sitter grammars and language-server sources referenced by Zed or an extension.

* The [`zed/`](https://github.com/zed-industries/zed) and [`zed-extensions/`](https://github.com/zed-industries/extensions) submodules are used to determine the repositories and versions to use.

  - `selected-grammars.toml` and `selected-servers.toml` are computed from these, and pin the URLs and SHAs for those.

  - Zed integration will use the registered extension versions and our selected grammar and server builds.

* [`lsp-data/`](https://github.com/cozysoft-io/code-corpora-lsp-data) is an optional submodule containing LSP data computed for the repositories based on the `servers`.

* [`containers/`](containers/README.md) contains build and runtime scripts for building the containers

* `.corpus/` is bind mounted in to the container(s) and holds build outputs.


# Language coverage

[`SELECTION.md`](SELECTION.md) describes how to choose new repositories for
heuristic-jump, preserve train/test assignments, and verify readiness for LSP
evaluation. Configuration and data languages are deferred during the current
programming-language expansion.

[`repo-selection.md`](repo-selection.md) lists the selected train/test pairs,
exceptions, deferrals, and unresolved gaps. Its
[`JSON audit`](repo-selection.json) records candidate evidence and source scopes.
New source selections remain unverified for evaluation until their language
support and dependencies have been checked.

[`DATA-PROPOSALS.md`](DATA-PROPOSALS.md) proposes sources for the remaining gaps,
including Rosetta Code, grammar tests, and repositories covering several languages.
[`data-proposals.json`](data-proposals.json) records the measurements and per-language routes.

[`language-coverage.md`](language-coverage.md) lists registered Zed language
suffixes and UTF-8 file/raw-line counts in `training/` and `test/`.
The census also accepts RosettaCodeData's `.arturo`, `.uiua`, and `.simula` aliases.
[`language-coverage.json`](language-coverage.json) retains registration pins,
per-suffix measurements, ambiguous suffixes, and unavailable extensions.

```sh
python3 corpus_coverage.py               # recount using the saved inventory
python3 corpus_coverage.py --refresh     # reread pinned extension configs
```

The census includes hidden and ignored files, skips Git metadata and symlinks,
and counts blanks and comments as ordinary lines. Shared suffixes can contribute
to several languages; split totals count each matching file once.

# Containers

`ghcr.io/cozysoft-io/code-corpora-build`: dependencies needed to build grammars and servers

`ghcr.io/cozysoft-io/code-corpora-grammars`: grammars compiled to both native and WASM. This has a local copy of the Zed extensions and grammars.

`ghcr.io/cozysoft-io/code-corpora-servers`: atop the grammars image, adds the language server and dependencies needed to load the corpus repos into the servers

These are setup such that modifications to the grammars or servers are accessible to both Zed and native builds.  This is done by:

* Symlinking the extensions into the directory Zed expects, and automatically structuring the extensions in the way that Zed expects.

* In the servers version, including a Zed configuration which overrides the binary path of every language server.

See the [local development workflow](containers/README.md#editing-grammars-and-servers-locally)
for building edited grammars and trying them in Zed. Bulk WASM/extension packaging is still pending.


# Fetching repositories

Only selection metadata and the fetch tool are downloaded by a normal clone.
All three submodules are optional and skipped even by `git clone --recurse-submodules`.
Corpus, grammar, and server checkouts are independent, ignored Git repositories.

```sh
./corpus clone                           # selected corpus repositories
./corpus clone --split train --language rust --repo ripgrep
./corpus clone /tmp/small-corpus --repo ripgrep
./corpus clone --set grammars            # all available grammar pins
./corpus clone --set grammars --repo csharp
./corpus clone --set servers --repo zls
./corpus status --set grammars
./corpus verify --split train --language rust

./corpus submodules --references         # opt in to Zed and its registry
./corpus submodules --data               # opt in to recorded LSP data
./corpus submodules --path zed            # or select a specific submodule
```

Python 3.11+ and Git are required. The default checkout root is this repository,
regardless of the working directory. An optional directory changes the checkout
root; selections still come from this repository. `--set` chooses `repos`
(the default), `grammars`, or `servers`. Repeated `--repo` filters select names;
`--split` and `--language` apply to corpus repositories. Cloning uses four workers
by default; `--jobs` changes that limit. No grammar or server is fetched implicitly.

[`selected-repos.toml`](selected-repos.toml) owns repository choices, full commit
SHAs, splits, language metadata, rationale, and dependency notes. Its 256 entries
span 17 languages: 171 training and 85 test, including one retired training entry.
Retired entries remain documented but are skipped by the tool.
[`corpus-lock.toml`](corpus-lock.toml) caches measurements of those selected commits.
Pins are used even without this cache; conflicting cached SHAs or URLs are errors.
Reserves and considered candidates also have explicit SHAs but are not cloned.

[`selected-grammars.toml`](selected-grammars.toml) pins 547 grammar checkouts.
[`selected-servers.toml`](selected-servers.toml) pins 432 server/source repositories,
shared across languages. A grammar's `directory` locates its parser inside the
checkout. Variants with different pins retain distinct names. These selections
are derived from the audited Zed snapshot in [`zed-sources.toml`](zed-sources.toml):

```sh
./corpus sources --check                 # validate generated selections offline
./corpus sources --write                 # regenerate them from the audit
./corpus submodules --check              # validate the three optional Git pins
```

Regeneration uses the existing audit; it does not refresh upstream HEADs. Updating
Zed references requires re-auditing their pinned extensions before generating new
selections. [SOURCES.md](SOURCES.md) documents the census and upstream limitations:
two grammar pins cannot currently be fetched, five server sources cannot be pinned,
and six extension manifests are unavailable. A full grammar clone reports the two
missing pins instead of substituting commits. Server source pins do not claim to
be the binary versions used by either Zed or the recorded LSP runs.

Missing checkouts use a shallow fetch of the selected SHA, no tags, and Git LFS
smudging disabled. Hosts that cannot serve a shallow SHA fetch fall back to history.
Existing checkouts are reused at their pin; a different HEAD is reported without
resetting it. Local modifications and untracked files are preserved. Failed clones
remove only their own staging directory. Source fetching does not build parsers,
install language servers, or initialize upstream repositories' nested submodules.

Paths are flat: `train/NAME`, `test/NAME`, `grammars/NAME`, and `servers/NAME`.
`training` remains a compatibility symlink to `train`; `--split training` is
also accepted. There are no per-language repository directories or generated manifests. `status`
checks pins; `verify` also checks working-tree cleanliness. For corpus repositories,
verification retains the existing dependency checks, using `.corpus/build/SPLIT/NAME`
for build artifacts. Migrated build products may need regeneration because they
can embed the old absolute paths.

Precompiled Tree-sitter grammars are available in the private
`ghcr.io/mgsloan/code-corpora-grammars` image. See the
[container usage instructions](containers/README.md#runtime-use) for running
them with Podman.

# Recorded data and history

[`lsp-data/`](https://github.com/cozysoft-io/code-corpora-lsp-data) stores the latest
position pools and their recorded observations under `training/NAME` and `test/NAME`.
Its inventory records original paths, repository pins, file hashes, collection
headers, and how each result set aligns with the current positions. Read its
`MIGRATION.md` before combining collection passes. Synthetic examples and analysis
exclusions are preserved there too. Local timing files remain ignored.

The dataset uses plain Git: individual files are under 25 MB, and the JSONL snapshot
compresses well. LFS is unnecessary for this snapshot; keeping data in an optional
repository is what makes the main repository quick to clone. Neither data nor
upstream checkout history is stored in the new initial commit on `main`.

The local `heuristic-jump-corpus` branch preserves the commit immediately before
the submodule migration (`ab10f8c`). It is intentionally not published: publishing
that historical branch would make ordinary clones fetch the old dataset history.
The local checkout is `~/cozy/code-corpora`; compatibility symlinks at
`~/cozy/code-analysis-corpus` and `~/cozy/tree-sitter-corpus` still point here,
but consumers must adopt the new paths. Heuristic-jump has not been updated for
this layout yet.

```sh
python3 -m unittest test_corpus
python3 lsp-data/verify.py                # after opting in to data
```
