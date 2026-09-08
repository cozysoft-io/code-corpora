# Zed source snapshot

`zed-sources.toml` preserves the audited source inventory. The generated
`selected-grammars.toml` and `selected-servers.toml` supply URLs and SHAs to the
fetch tool; check them with `./corpus sources --check` and regenerate with
`./corpus sources --write`. Regeneration is offline and uses the existing audit,
not a fresh extension census. Only `zed`, `zed-extensions`, and `lsp-data` are
submodules; `./corpus submodules --check` checks their pins and inactive defaults.

The snapshot was collected on 2026-09-08 from:

- [Zed at 20d3cd1d7981ed2076be5b72c817a1febbba3cb9](https://github.com/zed-industries/zed/tree/20d3cd1d7981ed2076be5b72c817a1febbba3cb9)
- [Zed extensions at 755cff87501f53f916a72e2bc0b07dda724195a4](https://github.com/zed-industries/extensions/tree/755cff87501f53f916a72e2bc0b07dda724195a4)

The registry contains 1,467 extensions. Each `[[extension]]` records its registered
version, repository, exact registry Gitlink SHA, any subdirectory, grammar paths,
server IDs, and server repository paths. The audit read the extension at that
commit, including nested extension directories and legacy `extension.json` /
`grammars/*.toml` layouts. Bundled Zed extensions and built-in servers are recorded
separately. Themes and other extensions without grammars or servers remain in the
census with empty lists, making coverage and omissions visible.

## Grammars

There are 547 grammar checkouts covering 520 names (including the JavaScript
alias). An extension's grammar `commit` or `rev` supplies the SHA. A branch reference
is resolved once and retained as `upstream_ref`. Built-in Cargo dependencies use
Zed's `Cargo.lock`; registry crates supply their Git commit through the published
crate's `.cargo_vcs_info.json`. `crate_version` records that evidence. The
`directory` field identifies a grammar within a repository, such as `tsx` or
`tree-sitter-markdown-inline`.

The same grammar name at different forks or commits gets a separate checkout
with an extension suffix. Shared identical pins are deduplicated and retain every
consumer in `sources`. Each of the corpus's 17 language names has a corresponding
checkout path; upstream `c_sharp` is stored at `grammars/csharp`. Zed parses
JavaScript with TSX, so `grammars/javascript` intentionally has the same repository
and commit as `grammars/tsx`.

Two original URLs were unavailable but the exact commits were recovered elsewhere:
`diff` from `tree-sitter-grammars/tree-sitter-diff`, and `jai` from
`constantitus/tree-sitter-jai`. `upstream_url` retains the original reference.
The Rego extension itself was recovered at its original SHA from `StyraOSS/zed-rego`;
its registry entry retains both URLs.

Two grammar commits remain unavailable, and have **not** been substituted:

| Checkout | Original pin | Failure |
| --- | --- | --- |
| `grammars/rust` | `e2bee853694a1d3e0f6ef308fe3674542fec95d7` | The published `tree-sitter-rust` 0.24.2 crate records this commit, but the source remote rejects it; sampled forks did not contain it. |
| `grammars/duckyscript` | `790d09b0679d70930a5c7d73546a11bb371b69a8` | `traumweh/tree-sitter-duckyscript` is unavailable; the discovered alternative did not contain this commit. |

Their TOML pins and original URLs are still registered. They are absent
locally, and a full grammar fetch currently reports errors for them. The other
545 grammar checkouts were fetched at their recorded commits. This checkout has
local `info/attributes` exceptions for AWK's `test/corpus/crlf.txt` and D2's
`assets/screenshot_1.png` / `assets/screenshot_2.png`: their upstream blanket
`* text` rule otherwise makes byte-identical checkouts appear dirty. The exceptions
mark those files `-text`; no tracked upstream file was edited. No parser build or
language-server installation is part of source fetching.

## Language servers

The 432 server repository checkouts are deduplicated by repository, so a project
such as LLVM, VS Code's extracted language servers, or a language compiler appears
once even when multiple adapters use it. Extension records preserve all declared
server IDs and the corresponding set of repository paths. Built-in server records
map IDs directly to repositories. This includes optional alternatives and extensions
that implement editor features through an LSP server.

Repositories were traced from pinned adapter source, installation commands,
README references, and package registry repository metadata. Server selection SHAs freeze
source HEAD observed during this snapshot, except Zed's fixed ESLint
`release/3.0.24` tag. These source snapshots are **not** a binary version lock for
Zed: adapters commonly select latest releases, package versions, local toolchains,
or user-configured executables at runtime.

`role` distinguishes actual source repositories from documentation, release
repositories, public toolchain components, and launchers. Intelephense and PHP Tools
publish documentation repositories; Microsoft's AL server and several other
projects publish distributions or only parts of their toolchain. Those entries do
not imply that proprietary server implementations are present. The AL bridge is
included separately. A server implemented inside an extension repository uses that
repository as its source checkout.

Five known server sources cannot be represented by a verified Git SHA and are
listed under `[[unavailable_server]]` with the originating adapter IDs:

- **Cartan**: the adapter runs `cartan lsp` from the `counterplot` Python package;
  neither the extension nor package metadata identifies a public Git source.
- **CAP CDS**: `@sap/cds-lsp` is proprietary and does not publish a source repository
  in its package metadata.
- **GreyCat**: the public GreyCat group contains editor integrations and grammars,
  but does not publish the CLI/compiler source that implements `greycat lsp`.
- **Infracost**: the adapter's `infracost/infracost-ls` repository is unavailable.
- **MetaScript**: the documented `metascriptlang/metascript` source is unavailable.

No invented commits or unrelated replacement repositories stand in for these.

## Unavailable extension manifests

Six registered extensions could not be read at their pins: `bearded`,
`irix-terminal-theme`, `nanowise`, `spai-zero-theme`, `vanta-theme`, and `zedburn`.
Their `[[extension]]` entries record exact registry URLs, SHAs, versions, and
`audit_error` details. Their apparent theme names are not taken as proof that they
contain no grammars or servers. Complete coverage cannot be asserted until those
manifests and the missing server sources become available.

## Fetching and defaults

```sh
./corpus sources --check
./corpus clone --set grammars
./corpus clone --set grammars --repo csharp
./corpus clone --set servers --repo zls
./corpus submodules --references
./corpus submodules --data
```

Grammar and server repositories are ordinary ignored checkouts, fetched only by
an explicit `--set` selection. They have no Gitlinks or submodule configuration.
All initialized grammar checkouts from the migration were preserved, including
local Git configuration and attributes. `--jobs` controls concurrent cloning;
fetching does not initialize upstream nested submodules.

The three remaining submodules have `active = false`, `update = none`, and
`shallow = true` in `.gitmodules`. Git does not use its custom `active` field as a
portable activation setting; [Git's documented `update = none` behavior](https://git-scm.com/docs/gitmodules)
makes fresh recursive clones skip these repositories. Explicit fetching uses
invocation-local activation and `--checkout`, leaving their defaults intact.
It does not force-reset modified working trees.

Neither offline check certifies network availability, buildability, or completeness
of the unavailable entries above. Updating the reference pins requires a new audit.
