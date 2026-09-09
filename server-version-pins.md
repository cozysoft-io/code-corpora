# Language-server version pins in Zed adapters

**30 selected repositories would change commits to reproduce the adapters' fixed
server versions.** Five have explicit version-matching or backwards-compatibility
reasons below; the other 25 have fixed installer defaults. A fixed download alone
is not evidence that a newer locally built server is incompatible.

This historical comparison uses the original HEAD snapshots. The subsequent
selection update is recorded in [server-releases.json](server-releases.json);
the “current” commits below refer to the original selection. Full SHAs,
requirements, and audit provenance are in [server-version-pins.json](server-version-pins.json).

## Scope and interpretation

Audited the 2026-09-08 selection: all **396 registered extensions declaring language
servers**, **18 built-in server mappings**, and **4 bundled extensions**, reading
adapters at their recorded Git commits. The registry has 1,467 entries; six
previously unavailable manifests remain a coverage gap. All 396 server-extension
source fetches succeeded. Fountain declares its command in the manifest and has
no Rust adapter source.

Reviewed version constants, tagged and direct downloads, package-install calls,
versions derived from Cargo/package metadata, compatibility checks, and relevant
documentation. Resolved upstream tags (peeling annotated tags to commits) and npm
`gitHead` values; where npm lacks `gitHead`, used the repository's package/release
tag. Remote resolution was checked on 2026-09-09 UTC. Links below point to pinned
adapter source and exact commits, not moving branches.

Here, “change” means replacing a source HEAD snapshot with the commit for the
adapter-selected release. Two different commits can report the same version;
version compatibility does not itself require identical Git commits. This audit
does not test protocol compatibility or recommend downgrading every listed
server. User-supplied executables and cached-download fallbacks can bypass managed
installation choices.

## Explicit compatibility or version-matching reasons

| Repository | Extension / adapter | Server version or tag | Current commit → release commit |
| --- | --- | --- | --- |
| `awsum` | [awsum](https://github.com/awsum-lang/awsum-zed/blob/3310599f11aa56730e1c699543e742b045706987/src/lib.rs#L74) | `v0.0.7` | [`fd7abdf701be`](https://github.com/awsum-lang/awsum/commit/fd7abdf701be2ae08277563c58da94efdfa1bcf1) → [`264f4ab5631c`](https://github.com/awsum-lang/awsum/commit/264f4ab5631c3baf0b2d829732e1109ad2cb4f2e) |
| `luau-lsp-proxy` | [luau](https://github.com/4teapo/zed-luau/blob/4f803e32bfb4cd1dc6b7ae25c047f18956c1a53f/src/luau.rs#L327) | `v0.1.0` | [`7a3a5861c8f8`](https://github.com/4teapo/luau-lsp-proxy/commit/7a3a5861c8f8261a4118f08c4c3c25ffc3085339) → [`2d626e9080a2`](https://github.com/4teapo/luau-lsp-proxy/commit/2d626e9080a2502e72726024e3cfac648fc40d09) |
| `tabby` | [zabby](https://github.com/arne-fuchs/zabby/blob/2f91f8ee997d6475d17915644c70da3ed3bba79a/src/zabby.rs#L40) | `tabby-agent@1.7.0` | [`21b29048d7bc`](https://github.com/TabbyML/tabby/commit/21b29048d7bcf6b94f9f482f2d0fd05efadfd19f) → [`e5fc90af54e0`](https://github.com/TabbyML/tabby/commit/e5fc90af54e0886678d1f9b16350a3393522bd2a) |
| `vscode-gradle` | [java](https://github.com/zed-extensions/java/blob/825c0c679828897921d23f081125ba130ea6e2f9/src/gradle_ls.rs#L17) | `3.18.0` | [`627e9eae0582`](https://github.com/microsoft/vscode-gradle/commit/627e9eae0582a849dbf7029786d9f704b99ef3d4) → [`2864656bcb12`](https://github.com/microsoft/vscode-gradle/commit/2864656bcb12114b392174d2dc333f49c983b38d) |
| `zed-dependi` | [dependi](https://github.com/mpiton/zed-dependi/blob/24445b1f94ceaf5c27c85a4d14c0a0c0f5893fd4/dependi-zed/src/lib.rs#L12) | `v1.11.0` | [`57790d92105d`](https://github.com/mpiton/zed-dependi/commit/57790d92105dad183a1337d1cad957f955792643) → [`24445b1f94ce`](https://github.com/mpiton/zed-dependi/commit/24445b1f94ceaf5c27c85a4d14c0a0c0f5893fd4) |

- **Awsum:** the extension sends `expectedAwsumVersion = 0.0.7`; its README says
  mismatched compiler/server and extension versions are unsupported.
- **Gradle:** Java's bridge protocol is coupled to vscode-gradle 3.18. The adapter
  explicitly prevents its update cache from substituting another version.
- **Tabby:** Zabby installs `tabby-agent@1.7.0` with an explicit comment that newer
  versions are broken. The relevant component is the Node agent, not just Tabby's
  main server executable.
- **Dependi:** v1.11.0 preserves the last Dependi release's asset names; subsequent
  Depsy releases use different names.
- **Luau:** the v0.1.0 constraint applies to the **proxy**, explicitly for backwards
  compatibility. The separate `luau-lsp` server still follows latest releases.

## Other fixed installer versions that differ

These reproduce the registered adapter's choice; their source does not establish
that all newer server code must be rejected.

| Repository | Extension / adapter | Server version or tag | Current commit → release commit |
| --- | --- | --- | --- |
| `baml` | [baml](https://github.com/BoundaryML/zed-baml/blob/e0f3f0438c42000a7983886e4cfa6ff921d702d1/src/lib.rs#L40) | `0.226.2` | [`92c9d1e4c0e9`](https://github.com/BoundaryML/baml/commit/92c9d1e4c0e9135a5590b4a34839b40f0fb0ef14) → [`d9c0bc720d81`](https://github.com/BoundaryML/baml/commit/d9c0bc720d813821cdd00c90a774bf6f71e4e572) |
| `bloc` | [bloc](https://github.com/felangel/bloc/blob/28b92e57ff84b4d0e1e6e1d041d442e50d40bdb1/extensions/zed/src/lib.rs#L5) | `bloc_tools-v0.1.0-dev.22` | [`8fcf54dfea7b`](https://github.com/felangel/bloc/commit/8fcf54dfea7ba51ef04c091d1a27e0da498b29f0) → [`9d7163e2c114`](https://github.com/felangel/bloc/commit/9d7163e2c114afd70a9f440d2bd791e2c835098d) |
| `che-che4z-lsp-for-cobol` | [cobol](https://github.com/willswire/zed-cobol/blob/ebf82098c0ac90da7676863ee1249fe8bc4311f4/src/cobol.rs#L50) | `2.4.3` | [`96818ab80d8f`](https://github.com/eclipse-che4z/che-che4z-lsp-for-cobol/commit/96818ab80d8f3bbe47e61669d557220c3377b938) → [`664f3d9e4e7d`](https://github.com/eclipse-che4z/che-che4z-lsp-for-cobol/commit/664f3d9e4e7d346a0e7e4ef9443597d7ea60a01a) |
| `code-translate` | [code-translate-lsp](https://github.com/nazzeDe/code-translate/blob/e60d026bc3597ea2bd162f94307441eeead2f73e/extensions/code-translate/src/lib.rs#L9) | `v0.1.0` | [`b53b9e644e53`](https://github.com/nazzeDe/code-translate/commit/b53b9e644e5354996e8bf3499a8e03d8ac144922) → [`c754ece78473`](https://github.com/nazzeDe/code-translate/commit/c754ece78473026acf0c53d9e585011c9fa0c8e0) |
| `ctags-lsp` | [ctags](https://github.com/mazurel/zed-ctags/blob/ee9d5a66bc78b0e78fc702c54b7aa5aa6c9445e9/src/ctags_lsp.rs#L40) | `v0.8.1` | [`fe3d1f8490c5`](https://github.com/netmute/ctags-lsp/commit/fe3d1f8490c5e7db38725b6e847472b9a63bacfc) → [`81903ebfe20f`](https://github.com/netmute/ctags-lsp/commit/81903ebfe20fb723b04ea919e2f33633e9484bb5) |
| `devglobe-extension` | [devglobe-activity-ls](https://github.com/devglobe-xyz/zed-devglobe/blob/cf9724a3053f4c2a868c5bb525696d9ef1b35dbc/src/lib.rs#L5) | `core-v2.0.0` | [`5c5cbc04d53c`](https://github.com/Nako0/devglobe-extension/commit/5c5cbc04d53c34ff6b2051763eb6bfb0f6ec6bcb) → [`07ac5678dcf6`](https://github.com/Nako0/devglobe-extension/commit/07ac5678dcf62636fc3416198c5d01e7c0bb6a33) |
| `elsa-lsp` | [elsa-lang](https://github.com/MrPoloGit/elsa-lang/blob/349bdaf15d32dbc28bfebc4cb39e9e1d27564340/src/lib.rs#L6) | `v0.1.0` | [`797b1b7779ae`](https://github.com/MrPoloGit/elsa-lsp/commit/797b1b7779aef3a907b3ea21c6e05843fe1799d7) → [`047dc2113c57`](https://github.com/MrPoloGit/elsa-lsp/commit/047dc2113c57a8d823cd54060cf192d38ffdbfe8) |
| `emoji-completions-zed` | [emoji-completions](https://github.com/ahockersten/emoji-completions-zed/blob/ddcd74ca832ba30f3f4ebacb9abb31dd0fe1f9d2/src/lib.rs#L4) | `1.1.1` | [`78cb190b949d`](https://github.com/ahockersten/emoji-completions-zed/commit/78cb190b949df45514dfec105512970209cc08a9) → [`ddcd74ca832b`](https://github.com/ahockersten/emoji-completions-zed/commit/ddcd74ca832ba30f3f4ebacb9abb31dd0fe1f9d2) |
| `muon` | [meson](https://github.com/jobpaardekooper/zed-meson/blob/152d031699da3c9d2b2666faef11e8efae5e9c6f/src/muon.rs#L11) | `0.6.0` | [`3ee54382d463`](https://git.sr.ht/~lattis/muon/commit/3ee54382d463bec09647edc6bd834a8f50f34458) → [`1c825e41e226`](https://git.sr.ht/~lattis/muon/commit/1c825e41e2266be1bead999f7f65d9c763a7ca18) |
| `papyrus-language-server` | [papyrus](https://github.com/monster-cookie/zed-papyrus/blob/bf56e65433cc861d5725a0ed0c946a6f896087f6/src/lib.rs#L9) | `v0.1.0` | [`db79ab22f4e6`](https://github.com/monster-cookie/papyrus-language-server/commit/db79ab22f4e6e1935aa18d5f59ff162a29165bfa) → [`f4baf7da54ed`](https://github.com/monster-cookie/papyrus-language-server/commit/f4baf7da54ed6fca79ff81ae211b3364282630b6) |
| `pgfmt` | [pgfmt-lsp](https://github.com/middle-management/pgfmt/blob/76e468b3ee7c48779f35b19e4bdd0cce23b89c11/zed-pgfmt/src/lib.rs#L6) | `v0.4.0` | [`e38e211c4453`](https://github.com/middle-management/pgfmt/commit/e38e211c445372ec5d2eb2d2b69b9168a8f7f228) → [`76e468b3ee7c`](https://github.com/middle-management/pgfmt/commit/76e468b3ee7c48779f35b19e4bdd0cce23b89c11) |
| `rust-glancer` | [rust-glancer](https://github.com/rust-glancer/rust-glancer/blob/7737db379d16f0de8c6d917335f288780ad6d26d/editors/zed/src/server/mod.rs#L25) | `v0.2.0` | [`c81f62d04188`](https://github.com/rust-glancer/rust-glancer/commit/c81f62d04188e67b5c97976723208b1ad6dadb8c) → [`7737db379d16`](https://github.com/rust-glancer/rust-glancer/commit/7737db379d16f0de8c6d917335f288780ad6d26d) |
| `schemalock` | [schemalock-lsp](https://github.com/schemalock/zed/blob/3e54139321b1e355adb8a3ba20bafa85cddfc4cd/src/lib.rs#L11) | `v0.3.2` | [`07ef8b01fa7a`](https://github.com/schemalock/schemalock/commit/07ef8b01fa7af7a64ff1dcd030e03a9c0a4357cc) → [`3ae7f7945894`](https://github.com/schemalock/schemalock/commit/3ae7f7945894a02b188d40a62591b7d567f0f46f) |
| `slang-server` | [verilog](https://github.com/someone13574/zed-verilog-extension/blob/63c7b90809441a124593c147429936312e3416cb/src/language_server/slang.rs#L12) | `v0.2.9` | [`a4ab2a4d6669`](https://github.com/hudson-trading/slang-server/commit/a4ab2a4d66693dde153848f14116b6d909698a1a) → [`4f33c99d8d41`](https://github.com/hudson-trading/slang-server/commit/4f33c99d8d41f254450e7396260861d55e6243b6) |
| `slint` | [slint](https://github.com/slint-ui/slint/blob/cf62c975c311e7036d599ed8ed0b7e6a8386a934/editors/zed/src/slint.rs#L55) | `v1.17.1` | [`f9363d7bdf5e`](https://github.com/slint-ui/slint/commit/f9363d7bdf5e026074c7d3a2e7aef1912b691e5f) → [`cf62c975c311`](https://github.com/slint-ui/slint/commit/cf62c975c311e7036d599ed8ed0b7e6a8386a934) |
| `svls` | [verilog](https://github.com/someone13574/zed-verilog-extension/blob/63c7b90809441a124593c147429936312e3416cb/src/language_server/svls.rs#L12) | `v0.2.14` | [`d8ea9a8340f2`](https://github.com/dalance/svls/commit/d8ea9a8340f24688d8c4987eb5a0a7e0f4110104) → [`698aba81a43c`](https://github.com/dalance/svls/commit/698aba81a43c63ebcbfa9abe9d1d7a2b955f7ee8) |
| `tsrx` | [tsrx](https://github.com/tsrx-org/tsrx/blob/04c99ffbbeb4c0ce7f4b4309cc611a187ce8d163/packages/zed-plugin/src/lib.rs#L205) | `@tsrx/language-server@0.3.132` | [`c88c913c21f9`](https://github.com/tsrx-org/tsrx/commit/c88c913c21f9c61bf34c58724b7a00d95b423d85) → [`04c99ffbbeb4`](https://github.com/tsrx-org/tsrx/commit/04c99ffbbeb4c0ce7f4b4309cc611a187ce8d163) |
| `twiggy` | [twig](https://github.com/YussufSassi/zed-twig/blob/5e94550cd5326dd1af8703afae6dbda731f5dd40/src/lib.rs#L26) | `twiggy-language-server@0.17.0` | [`198f402052fa`](https://github.com/moetelo/twiggy/commit/198f402052fafdad81e563ee9b151712cf8f501c) → [`acb08b4ec353`](https://github.com/moetelo/twiggy/commit/acb08b4ec353dafb709e2b6ef5847990582ceb8c) |
| `verible` | [verilog](https://github.com/someone13574/zed-verilog-extension/blob/63c7b90809441a124593c147429936312e3416cb/src/language_server/verible.rs#L12) | `v0.0-4080-ga0a8d8eb` | [`b975d9d903f7`](https://github.com/chipsalliance/verible/commit/b975d9d903f7a60510393d438a086294ab086dea) → [`a0a8d8eb8cfa`](https://github.com/chipsalliance/verible/commit/a0a8d8eb8cfa9fd8969c9d646454d363b48aa449) |
| `vscode-antlers-language-server` | [statamic-antlers](https://github.com/mynetx/zed-statamic-antlers/blob/76f7ccb977c2fb54cb2dab737005c6026e2af6fb/src/lib.rs#L26) | `antlers-language-server@1.3.14` | [`d1c2a2d99d93`](https://github.com/Stillat/vscode-antlers-language-server/commit/d1c2a2d99d936cd4b54bdcfda41aaa552d9c16cd) → [`bb19f62ecee4`](https://github.com/Stillat/vscode-antlers-language-server/commit/bb19f62ecee45b55ea5cc580b4b9f92bdd3a643e) |
| `vscode-autohotkey` | [autohotkey](https://github.com/alfredomtx/tree-sitter-autohotkey/blob/f81633d58c9cda7da140148b4910687ec3cb7053/src/lib.rs#L12) | `lsp-v0.4.0` | [`bbd429675c5c`](https://github.com/alfredomtx/vscode-autohotkey/commit/bbd429675c5c5b73dbad306ef4693bcbe763f5d8) → [`16fa748fe73d`](https://github.com/alfredomtx/vscode-autohotkey/commit/16fa748fe73d9e9f736b197cc13ec9515b6183f6) |
| `zed-firrtl-source-locator` | [firrtl-source-locator](https://github.com/MrAMS/zed-firrtl-source-locator/blob/76e71c5344baac995863e7f134fda5290105a5ef/src/lib.rs#L10) | `v0.1.0` | [`afa0915caf42`](https://github.com/MrAMS/zed-firrtl-source-locator/commit/afa0915caf42d4cd2fc68e6ed9f03178bc991d57) → [`76e71c5344ba`](https://github.com/MrAMS/zed-firrtl-source-locator/commit/76e71c5344baac995863e7f134fda5290105a5ef) |
| `zed-laravel` | [laravel](https://github.com/mike-bronner/zed-laravel/blob/c164f7e834cf2cc1730878f9d0657539fd451fbc/src/lib.rs#L5) | `0.7.6` | [`83d79d5072a4`](https://github.com/mike-bronner/zed-laravel/commit/83d79d5072a4be87c0059688b5b09736db5c0ae4) → [`c164f7e834cf`](https://github.com/mike-bronner/zed-laravel/commit/c164f7e834cf2cc1730878f9d0657539fd451fbc) |
| `zed-phpmd-lsp` | [phpmd](https://github.com/mike-bronner/zed-phpmd-lsp/blob/c497da1cb99b706aea0de13ac0237d0a1e9fbf9c/src/lib.rs#L7) | `0.1.5` | [`9c090ae2443c`](https://github.com/GeneaLabs/zed-phpmd-lsp/commit/9c090ae2443cf4cb13d9c883a842e1f0992b4e29) → [`c497da1cb99b`](https://github.com/GeneaLabs/zed-phpmd-lsp/commit/c497da1cb99b706aea0de13ac0237d0a1e9fbf9c) |
| `zed-python-autodoc` | [python-autodoc-lsp](https://github.com/eallender/zed-python-autodoc/blob/2e280337d4bf603ebf65d3cdb6e59886d936df04/src/lib.rs#L61) | `v0.1.1` | [`8d97c0303738`](https://github.com/eallender/zed-python-autodoc/commit/8d97c03037382f86158f457aecccf61d4656da08) → [`2e280337d4bf`](https://github.com/eallender/zed-python-autodoc/commit/2e280337d4bf603ebf65d3cdb6e59886d936df04) |

BAML selects the release matching its extension version to stay on the engine
release stream; another release pipeline in the same repository has different
asset names. Laravel, PHPmd, Slint, and several other adapters also derive their
release version from the extension's Cargo version. TSRX embeds
`@tsrx/language-server@0.3.132` in its package configuration; the package tag and npm
published provenance name the same commit. Muon's download directory is
`v0.6.0`, but its Git tag is `0.6.0`.

## Fixed versions already at the selected commit

| Repository | Extension / adapter | Server version or tag | Current commit → release commit |
| --- | --- | --- | --- |
| `fswiki-lsp` | [fswiki](https://github.com/blank71/zed-fswiki/blob/00cebd342aa66744a895e1fdd1c95cf638450f81/src/lib.rs#L8) | `v1.0.1` | [`dd8f2fa3f458`](https://github.com/blank71/fswiki-lsp/commit/dd8f2fa3f45885d468d01e03160f196b11414813) → [`dd8f2fa3f458`](https://github.com/blank71/fswiki-lsp/commit/dd8f2fa3f45885d468d01e03160f196b11414813) |
| `hl7_v2_lsp` | [hl7v2](https://github.com/Yes25/zed-hl7v2-extension/blob/38c232ce29fd86440a2c57be33a969fba5281d8d/src/lib.rs#L50) | `v0.1.0` | [`5bb0319204eb`](https://github.com/Yes25/hl7_v2_lsp/commit/5bb0319204eb45e6af79f97e837a8558d7a8d122) → [`5bb0319204eb`](https://github.com/Yes25/hl7_v2_lsp/commit/5bb0319204eb45e6af79f97e837a8558d7a8d122) |
| `odoo-ls` | [odoo](https://github.com/odoo/odoo-zed/blob/376c8ffa99a692a9c37dd09748f20c1f71e841f3/src/odoo.rs#L5) | `1.4.0` | [`1b54aeb358e9`](https://github.com/odoo/odoo-ls/commit/1b54aeb358e96825389192d334f230a2430e96a7) → [`1b54aeb358e9`](https://github.com/odoo/odoo-ls/commit/1b54aeb358e96825389192d334f230a2430e96a7) |
| `vscode-eslint` | [Zed core](https://github.com/zed-industries/zed/blob/20d3cd1d7981ed2076be5b72c817a1febbba3cb9/crates/languages/src/eslint.rs#L41) | `release/3.0.24` | [`395c7bd36f2a`](https://github.com/microsoft/vscode-eslint/commit/395c7bd36f2a81f3271bf2e303949d4358c231a1) → [`395c7bd36f2a`](https://github.com/microsoft/vscode-eslint/commit/395c7bd36f2a81f3271bf2e303949d4358c231a1) |
| `zed-phpcs-lsp` | [phpcs](https://github.com/mike-bronner/zed-phpcs-lsp/blob/10c40a7861b388cafc8fc5e2908ac7e4734b3ea3/src/lib.rs#L12) | `0.4.5` | [`10c40a7861b3`](https://github.com/mike-bronner/zed-phpcs-lsp/commit/10c40a7861b388cafc8fc5e2908ac7e4734b3ea3) → [`10c40a7861b3`](https://github.com/mike-bronner/zed-phpcs-lsp/commit/10c40a7861b388cafc8fc5e2908ac7e4734b3ea3) |
| `zed-todo-highlight` | [todo-highlight-language-server](https://github.com/shionit/zed-todo-highlight/blob/a5885f34f322479d8f3559d11eec260a8b642f95/extension/src/lib.rs#L6) | `v0.3.0` | [`a5885f34f322`](https://github.com/shionit/zed-todo-highlight/commit/a5885f34f322479d8f3559d11eec260a8b642f95) → [`a5885f34f322`](https://github.com/shionit/zed-todo-highlight/commit/a5885f34f322479d8f3559d11eec260a8b642f95) |
| `zed-urdf` | [urdf](https://github.com/MorningFrog/zed-urdf/blob/3b5e645201bf4fb2545afba8cacdfd6742955f81/src/lib.rs#L12) | `v0.1.0` | [`3b5e645201bf`](https://github.com/MorningFrog/zed-urdf/commit/3b5e645201bf4fb2545afba8cacdfd6742955f81) → [`3b5e645201bf`](https://github.com/MorningFrog/zed-urdf/commit/3b5e645201bf4fb2545afba8cacdfd6742955f81) |

ESLint's `release/3.0.24` was already respected by the original source census.
The other six matching pins also require no change.

## Conditional choices and installation hints

| Repository | Extension / adapter | Server version or tag | Current commit → release commit |
| --- | --- | --- | --- |
| `gregorio-lsp` | [gregorio](https://github.com/AISCGre-BR/zed-gregorio/blob/65e90135e17772825aed9c89f4edbd1e0bcf2857/src/lib.rs#L40) | `v0.9.0` | [`5fe102992cb8`](https://github.com/aiscgre-br/gregorio-lsp/commit/5fe102992cb82ac6b0f29323ff57169f5a8bb890) → [`6a777ff62732`](https://github.com/aiscgre-br/gregorio-lsp/commit/6a777ff627328990fab16a9ad8d0f57485a24bc7) |
| `language-tools` | [prisma](https://github.com/zed-extensions/prisma/blob/153761b02be4eae40eb7fe8414f3e8421a41653f/src/prisma.rs#L14) | `@prisma/language-server@6.19.0-hotfix.1` | [`3c526c3ca6f6`](https://github.com/prisma/language-tools/commit/3c526c3ca6f6fbe869230130a21836f62776a774) → [`79d09e4b556e`](https://github.com/prisma/language-tools/commit/79d09e4b556ebc8db2c3e79fb38be788fc90a306) |
| `spec42` | [sysml-v2](https://github.com/elan8/spec42/blob/2183b21b63a8de619de4a4718847b6a5fb15c339/zed/src/lib.rs#L122) | `v0.30.0` | [`31a8b7bb4b64`](https://github.com/elan8/spec42/commit/31a8b7bb4b64c668df6c0b54d8e8a9044d9b9902) → [`2183b21b63a8`](https://github.com/elan8/spec42/commit/2183b21b63a8de619de4a4718847b6a5fb15c339) |

- **Prisma / `language-tools`:** `6.19.0-hotfix.1` applies only when
  `prisma.pinToPrisma6` is true. The default installs latest, so this is not a
  blanket downgrade.
- **SysML v2 / `spec42`:** prefers `v0.30.0`, matching the extension, but explicitly
  falls back to latest when that tag cannot be fetched. Reproducing its preferred
  release adds one commit change; it is not a strict holdback.
- **Gregorio:** `v0.9.0` appears only in the manual-install error message. The
  adapter accepts an executable on PATH without checking its version; this is
  not an enforced pin.

## Constraints that do not force an existing repository to change

- **path-server:** [major 0 or 1](https://github.com/kunlinglio/path-server/blob/0b0bd32468acb66a7f99bfd523953af88c1f2770/extensions/zed/src/config.rs#L5). The selected source reports [1.4.1](https://github.com/kunlinglio/path-server/blob/7b25d961c15b78d4d5e737cbba0ba1d1895a405a/Cargo.toml#L3), which satisfies the constraint. Latest release is checked for allowed major; existing source version satisfies it. No unique older commit is required.
- **arkts:** [zed-ets-language-server major 3; its 3.0.0 package depends on @arkts/language-server ^1.2.8](https://github.com/liuyanghejerry/zed-arkts/blob/ebab416c802e197d6e4ed60c754e303e4ba27158/src/lib.rs#L9). The selected source reports [1.3.10](https://github.com/ohosvscode/arkTS/blob/25fda87a6677c3e92f3b7ed41adbab82c3847929/packages/language-server/package.json), which satisfies the constraint. The major-3 limit applies to a separate npm wrapper, not major 3 of the selected arkTS source. Selected server version satisfies ^1.2.8.

Minimum-version checks (for example Stylelint >=1.0.0, Oso >=0.18.0, and the TSGo
adapter's >=7 requirement) do not establish an upper limit. Angular requires a
server major matching the project's Angular major; that depends on the project,
so it does not identify one replacement commit for this corpus. Dynamic latest
releases, rolling `nightly`/`latest` tags, and user-configurable version settings
were not turned into arbitrary fixed pins.

## Dependency pins and source-mapping gaps

- **TypeScript:** [Astro](https://github.com/zed-extensions/astro/blob/03b07a4451df6f9dee6897afc06d841131dc8c05/src/astro.rs#L11) and [Vue](https://github.com/zed-extensions/vue/blob/bbd770740d10fc38c72ccbd59f8898608cb70baf/src/vue.rs#L12) pin their bundled JavaScript TypeScript dependency to **6.0.3**; Vue explains that newer native releases lack the JavaScript API it needs. [Angular's documentation](https://github.com/nathansbradshaw/zed-angular/blob/b2e68e970f76e52d65698fdde2bcd5faca5b53ae/README.md#L29) also caps supported TypeScript at 6.0.3. Zed's built-in TypeScript adapter requests `^6`. The npm 6.0.3 package records commit `050880ce59e30b356b686bd3144efe24f875ebc8` in `microsoft/TypeScript`. That repository is absent from `selected-servers.toml`: this needs a dependency pin, not a change to `typescript-language-server` or `typescript-go`. TSRX's pinned package instead declares a TypeScript `^5.9.3` peer dependency; keep these dependencies separate.
- **Salesforce:** the [Apex adapter](https://github.com/Damecek/zed-salesforce-extension/blob/a88190149536525dee62a0a0f606754ec43689c9/src/lib.rs#L9) downloads its JAR from `forcedotcom/salesforcedx-vscode` at `67dc27932e0ce43b93abe00878a2f966d0eb16a3`. That distribution repository is missing from the server selection. The listed `aer-dist` repository is a separate optional backend, so repinning it would not reproduce the Apex JAR.
- **Veridian:** the [adapter](https://github.com/someone13574/zed-verilog-extension/blob/63c7b90809441a124593c147429936312e3416cb/src/language_server/veridian.rs#L11) downloads assets from `someone13574/zed-verilog-extension@v0.0.19`. That is **not a Veridian version**. Its [release workflow](https://github.com/someone13574/zed-verilog-extension/blob/63c7b90809441a124593c147429936312e3416cb/.github/workflows/build-veridian.yaml#L13) checks out `vivekmalneedi/veridian` without a `ref`. The pinned adapter/workflow cannot determine the compiled server commit; build logs or artifact provenance are needed before claiming a change from selected `0c5776a4a4e08fd00b90d91ad3cd2ec10315d2bd`.
- **PX-to-rem:** hardcodes `0.1.0` in its asset filename but asks for the latest release. This is an installer fragility, not a source-tag constraint. The corresponding v0.1.0 tag already equals its selected commit.

The six unreadable extension manifests are `bearded`, `irix-terminal-theme`,
`nanowise`, `spai-zero-theme`, `vanta-theme`, and `zedburn`. Their names alone do
not prove that they contain no additional server constraints.
