# Servers still selected from HEAD

After applying extension version pins and selecting numbered release tags on
2026-09-09 UTC, **27 of 432 repositories** still use an observed default-branch
HEAD. These remain frozen to the full SHAs in `selected-servers.toml`; fetching
does not follow a moving branch.

The other 405 selections comprise 38 extension-selected versions and 367 release
tags. Stable versions take precedence over prereleases; dated releases are used
where that is the upstream convention. Monorepo selections use the server's tag
family where available. [server-releases.json](server-releases.json) records every
old/new commit, selected ref, and the observation time. **315 commits changed.**

| Repository | Frozen HEAD | Reason |
| --- | --- | --- |
| [al](https://github.com/microsoft/AL) | [`179d3edf6605`](https://github.com/microsoft/AL/commit/179d3edf6605559cf146f514b7580b3c18212741) | No tags |
| [bqnlsp](https://git.sr.ht/~detegr/bqnlsp) | [`13dfae2687b4`](https://git.sr.ht/~detegr/bqnlsp/commit/13dfae2687b482d55ff679eb905951267c7b00b0) | No tags |
| [bruno-language-server](https://github.com/davitostes/bruno-language-server) | [`236cbe5092aa`](https://github.com/davitostes/bruno-language-server/commit/236cbe5092aa63d025049caf6b0aaad84d7bc06a) | No tags |
| [coffeesense](https://github.com/phil294/coffeesense) | [`793ea901b7ef`](https://github.com/phil294/coffeesense/commit/793ea901b7ef5c1528400ae9a589365589085cdc) | No tags |
| [dang](https://codeberg.org/vito/dang) | [`acc64672d754`](https://codeberg.org/vito/dang/commit/acc64672d7540cb2f6804ac2b1f68ab5efd46f99) | No tags |
| [edge-language-server](https://github.com/Hexacker/edge-language-server) | [`41a41c77eb5d`](https://github.com/Hexacker/edge-language-server/commit/41a41c77eb5d901b9ed8b01085bd9fe815942939) | No tags |
| [elle](https://github.com/acquitelol/elle) | [`0e218ec645a9`](https://github.com/acquitelol/elle/commit/0e218ec645a9307363ef5b85bf0122e10f9125a6) | No tags |
| [fuzzy_ruby_server](https://github.com/doompling/fuzzy_ruby_server) | [`9a439496ae06`](https://github.com/doompling/fuzzy_ruby_server/commit/9a439496ae0666b1cee0213031a6dcc3e74662cd) | No tags |
| [gh-actions-language-server](https://github.com/lttb/gh-actions-language-server) | [`dcbb17fc6c6a`](https://github.com/lttb/gh-actions-language-server/commit/dcbb17fc6c6af3484f59c75959c6b132760d9f5d) | No tags |
| [groovy-language-server](https://github.com/valentinegb/groovy-language-server) | [`d6ec7d7f12bc`](https://github.com/valentinegb/groovy-language-server/commit/d6ec7d7f12bce86c96ba2cde11cc5c964a07ad6d) | No numbered release tags (only 2884e64, 39aeba0, 6dd296e, 886f0ee, 8d57a04, aaebaeb, b8cc4e6, d6ec7d7) |
| [idris2-lsp](https://github.com/idris-community/idris2-lsp) | [`9a2f0ad6a958`](https://github.com/idris-community/idris2-lsp/commit/9a2f0ad6a95815fe3ed438ddba08c95574a4de54) | No tags |
| [intelephense-docs](https://github.com/bmewburn/intelephense-docs) | [`3e810bc28237`](https://github.com/bmewburn/intelephense-docs/commit/3e810bc2823754096710863d2d0c30382c0bee55) | No tags |
| [jsonl-tools](https://github.com/sarvagnan/jsonl-tools) | [`073cec243a57`](https://github.com/sarvagnan/jsonl-tools/commit/073cec243a57ffba6885d882e5ab8ccf3187326e) | No tags |
| [moon](https://github.com/moonbitlang/moon) | [`5257d96a6414`](https://github.com/moonbitlang/moon/commit/5257d96a6414eff4ee50bf19efcb55c700f40642) | No tags |
| [phptools-docs](https://github.com/DEVSENSE/phptools-docs) | [`cbd57d88aac2`](https://github.com/DEVSENSE/phptools-docs/commit/cbd57d88aac201e5fd821071106a625755da2c3b) | No tags |
| [plaintasks-zed](https://github.com/cseelus/plaintasks-zed) | [`a80c6e5a7027`](https://github.com/cseelus/plaintasks-zed/commit/a80c6e5a70276c6a8f1f372b3ae7861ad6859d37) | No tags |
| [racket-langserver](https://github.com/jeapostrophe/racket-langserver) | [`d84878a09914`](https://github.com/jeapostrophe/racket-langserver/commit/d84878a099140c5afaaf70c9593d09e82dd8655a) | No tags |
| [silverstripe-language-server](https://github.com/nicolas-cusan/silverstripe-language-server) | [`1e807d927e46`](https://github.com/nicolas-cusan/silverstripe-language-server/commit/1e807d927e46e781a6d4dcd27924679cb582d383) | No tags |
| [soma](https://github.com/SrGaabriel/soma) | [`b8be70dfbdb6`](https://github.com/SrGaabriel/soma/commit/b8be70dfbdb687f73b72f140dfa9fa75d1b221e5) | No tags |
| [stardog-language-servers](https://github.com/stardog-union/stardog-language-servers) | [`d3e39c4c876f`](https://github.com/stardog-union/stardog-language-servers/commit/d3e39c4c876ff276da9e36e73f9f6376b36da849) | No tags |
| [texpresso](https://github.com/lnay/texpresso) | [`47cd92e4619c`](https://github.com/lnay/texpresso/commit/47cd92e4619cc32f2499223e966dd09700836d6e) | No tags |
| [umple-lsp](https://github.com/umple/umple-lsp) | [`1771d55d7e00`](https://github.com/umple/umple-lsp/commit/1771d55d7e00a720b97c0f2422971efa26e110f6) | No tags |
| [valse](https://github.com/gavr123456789/vaLSe) | [`bcfbdd0995b8`](https://github.com/gavr123456789/vaLSe/commit/bcfbdd0995b81307a0c2a7e64eef2ed362a514c2) | No tags |
| [veridian](https://github.com/vivekmalneedi/veridian) | [`0c5776a4a4e0`](https://github.com/vivekmalneedi/veridian/commit/0c5776a4a4e08fd00b90d91ad3cd2ec10315d2bd) | No numbered release tags (only nightly) |
| [vls](https://github.com/lv37/vls) | [`244aca640711`](https://github.com/lv37/vls/commit/244aca64071177ab4d40cb28b2fa1f7bb5a223f4) | No numbered release tags (only nightly) |
| [zed-bookmark](https://github.com/A-23187/zed-bookmark) | [`a8effebb481b`](https://github.com/A-23187/zed-bookmark/commit/a8effebb481b9c7b96af3c2fc1d4f73409dcf74d) | No tags |
| [zed-hexpeek](https://github.com/A-23187/zed-hexpeek) | [`fedc038fae5c`](https://github.com/A-23187/zed-hexpeek/commit/fedc038fae5ce56586a1cc3c6e0a995b42b239b1) | No tags |

`veridian` has an additional provenance gap: the extension's v0.0.19 release
builds upstream without a source ref. Its extension release tag cannot safely be
used as a Veridian source tag. The selected HEAD is therefore explicit rather
than presented as the source of that downloaded binary.

Prisma's optional `pinToPrisma6` setting is not enabled by this selection. SysML's
preferred extension-version tag is selected even though its installer permits a
latest-release fallback. Manual installation hints are not treated as pins.

Builds made before this selection keep their original source provenance. New
versions need new builds; selecting a commit does not validate its buildability
or compatibility.
