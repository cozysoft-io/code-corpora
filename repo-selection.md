# Registered-language repository selection

Baseline: 425 language names below 50 UTF-8 files **or** 2,000 raw lines across training and test. 97 names have a train/test pair, using 186 new repositories (92 train, 94 test). 219 are deferred; 109 remain unresolved.

Selections and immutable pins are in [`selected-repos.toml`](selected-repos.toml). The [process](SELECTION.md) explains the criteria; [`repo-selection.json`](repo-selection.json) preserves the baseline, candidate snapshots, source paths, measurements, exceptions, and discovery queries. Existing repository pins and splits are preserved.

**Fetched, evaluation unverified:** all 186 new repositories have been fetched and checked against their selected commits. Original pins, splits, and 256 lock entries are unchanged. Builds and LSP oracles remain unverified; every addition has `evaluation_ready = false`. Counts in the selected-pairs table remain the scoped archive measurements used for selection. The updated [coverage census](language-coverage.md) counts all matching UTF-8 files in the fetched checkouts, including comments, blanks, and incidental formats.

The source scope excludes known fixtures, copied libraries and stubs. Exact Git-blob comparisons found no matching scoped files over 300 bytes between the GitHub candidates or with the existing corpus checkouts. This does not detect near copies. Apply the recorded source scopes and audit dependencies before evaluating; the fetch tool clones whole repositories.

The current census requires at least **21 files and 2,000 raw lines** combined.
After recounting, **302 language names** remain below threshold; all 97 language
names with selected pairs now meet it. File and line totals are unchanged.

## Coverage after fetching (original 50-file threshold)

Languages below 50 files or 2,000 raw lines combined decreased from **425 to 316**. 109 language names cleared both thresholds, including 13 deferred registrations.

| Split | Added UTF-8 files | Added raw lines | Total UTF-8 files | Total raw lines |
| --- | ---: | ---: | ---: | ---: |
| training | 125,947 | 46,999,201 | 997,484 | 243,903,498 |
| test | 66,596 | 15,567,571 | 681,830 | 115,611,466 |

Deferred registrations that cleared both thresholds: Build2, Docker Compose, Dune, EJS, Godot Resource, GPR, Meson, Move.toml, OMNeT++ MSG, PlatformIO, Quadlet, RPM Spec, TLA+ Cfg.

Four selected languages still have fewer than 50 matching files combined:
AppleScript (43), AWK (39), OCamllex (32), and ucode (44). Each exceeds 2,000 raw lines.

The language inventory is unchanged. The scan had no file-read errors; the same six extension inventories remain unavailable. Shared filename suffixes still indicate possible coverage rather than verified language identity. Historical selection decisions below remain frozen; current per-language counts are in the coverage report and JSON audit.

## Selected pairs

| Language | Baseline files / lines | Train repository (scoped files / lines) | Test repository (scoped files / lines) |
| --- | ---: | --- | --- |
| ActionScript | 0 / 0 | [Gamua/Starling-Framework](https://github.com/Gamua/Starling-Framework) (120 / 32,962) | [away3d/away3d-core-fp11](https://github.com/away3d/away3d-core-fp11) (470 / 90,777) |
| Ada | 6 / 2,608 | [AdaCore/gnatcoll-core](https://github.com/AdaCore/gnatcoll-core) (247 / 84,467) | [alire-project/alire](https://github.com/alire-project/alire) (392 / 63,135) |
| Agda | 0 / 0 | [agda/agda-stdlib](https://github.com/agda/agda-stdlib) (1,171 / 139,546) | [agda/cubical](https://github.com/agda/cubical) (1,189 / 201,323) |
| Aiken | 0 / 0 | [aiken-lang/stdlib](https://github.com/aiken-lang/stdlib) (34 / 8,318) | [SundaeSwap-finance/sundae-contracts](https://github.com/SundaeSwap-finance/sundae-contracts) (19 / 3,949) |
| AL | 0 / 0 | [Drakonian/data-editor-for-bc](https://github.com/Drakonian/data-editor-for-bc) (27 / 12,871) | [Bertverbeek4PS/bc2adls](https://github.com/Bertverbeek4PS/bc2adls) (72 / 10,341) |
| AppleScript | 20 / 1,713 | [section83/MacYTDL](https://github.com/section83/MacYTDL) (9 / 14,075) | [franzheidl/alfred-workflows](https://github.com/franzheidl/alfred-workflows) (14 / 919) |
| Arduino | 0 / 0 | [letscontrolit/ESPEasy](https://github.com/letscontrolit/ESPEasy) (172 / 56,593) | [arendst/Tasmota](https://github.com/arendst/Tasmota) (434 / 289,078) |
| AutoHotkey | 0 / 0 | [Descolada/UIA-v2](https://github.com/Descolada/UIA-v2) (3 / 9,533) | [abgox/InputTip](https://github.com/abgox/InputTip) (27 / 8,354) |
| AWK | 3 / 797 | [soimort/translate-shell](https://github.com/soimort/translate-shell) (22 / 8,678) | [step-/JSON.awk](https://github.com/step-/JSON.awk) (3 / 740) |
| Bluespec SystemVerilog | 0 / 0 | [bluespec/Flute](https://github.com/bluespec/Flute) (184 / 68,073) | [cambridgehackers/connectal](https://github.com/cambridgehackers/connectal) (211 / 45,929) |
| BQN | 0 / 0 | [mlochbaum/BQN](https://github.com/mlochbaum/BQN) (25 / 3,880) | [mlochbaum/Singeli](https://github.com/mlochbaum/Singeli) (7 / 2,458) |
| Bsl | 0 / 0 | [cpr1c/tools_ui_1c](https://github.com/cpr1c/tools_ui_1c) (333 / 233,089) | [vbondarevsky/Connector](https://github.com/vbondarevsky/Connector) (4 / 8,121) |
| C3 | 4 / 235 | [c3lang/c3c](https://github.com/c3lang/c3c) (329 / 77,977) | [tonis2/lsp](https://github.com/tonis2/lsp) (27 / 12,786) |
| Cadence | 0 / 0 | [onflow/flow-core-contracts](https://github.com/onflow/flow-core-contracts) (351 / 18,033) | [dapperlabs/nba-smart-contracts](https://github.com/dapperlabs/nba-smart-contracts) (145 / 8,730) |
| Cairo | 2 / 14 | [OpenZeppelin/cairo-contracts](https://github.com/OpenZeppelin/cairo-contracts) (160 / 19,215) | [keep-starknet-strange/alexandria](https://github.com/keep-starknet-strange/alexandria) (113 / 23,236) |
| CFML (Tag) | 0 / 0 | [ColdBox/coldbox-platform](https://github.com/ColdBox/coldbox-platform) (187 / 58,829) | [framework-one/fw1](https://github.com/framework-one/fw1) (25 / 5,843) |
| Circom | 0 / 0 | [iden3/circomlib](https://github.com/iden3/circomlib) (54 / 5,768) | [privacy-ethereum/maci](https://github.com/privacy-ethereum/maci) (37 / 3,737) |
| Clarity | 0 / 0 | [stacks-sbtc/sbtc](https://github.com/stacks-sbtc/sbtc) (5 / 1,106) | [alexgo-io/alex-v1](https://github.com/alexgo-io/alex-v1) (362 / 98,412) |
| Clojure | 53 / 320 | [clojure/clojurescript](https://github.com/clojure/clojurescript) (71 / 31,179) | [ring-clojure/ring](https://github.com/ring-clojure/ring) (33 / 3,107) |
| COBOL | 0 / 0 | [meyfa/CobolCraft](https://github.com/meyfa/CobolCraft) (192 / 25,295) | [walmartlabs/zECS](https://github.com/walmartlabs/zECS) (5 / 4,056) |
| Crystal | 17 / 2,795 | [kemalcr/kemal](https://github.com/kemalcr/kemal) (33 / 4,370) | [luckyframework/lucky](https://github.com/luckyframework/lucky) (143 / 10,633) |
| Curry | 0 / 0 | [curry-language/curry2go](https://github.com/curry-language/curry2go) (32 / 7,177) | [curry-language/kics2](https://github.com/curry-language/kics2) (29 / 7,687) |
| Cython | 13 / 390 | [scikit-learn/scikit-learn](https://github.com/scikit-learn/scikit-learn) (77 / 21,728) | [lxml/lxml](https://github.com/lxml/lxml) (50 / 27,020) |
| Dafny | 0 / 0 | [dafny-lang/libraries](https://github.com/dafny-lang/libraries) (88 / 19,090) | [Consensys-Incorporated/evm-dafny](https://github.com/Consensys-Incorporated/evm-dafny) (20 / 6,902) |
| DAML | 0 / 0 | [digital-asset/daml](https://github.com/digital-asset/daml) (113 / 12,468) | [digital-asset/daml-finance](https://github.com/digital-asset/daml-finance) (202 / 15,912) |
| Dylan | 0 / 0 | [dylan-lang/http](https://github.com/dylan-lang/http) (36 / 10,169) | [dylan-lang/binary-data](https://github.com/dylan-lang/binary-data) (10 / 3,115) |
| Elisp | 23 / 1,895 | [magit/magit](https://github.com/magit/magit) (48 / 36,978) | [abo-abo/swiper](https://github.com/abo-abo/swiper) (12 / 15,937) |
| Elm | 32 / 1,852 | [mdgriffith/elm-ui](https://github.com/mdgriffith/elm-ui) (25 / 13,808) | [eikek/docspell](https://github.com/eikek/docspell) (452 / 85,701) |
| Erlang | 7 / 1,445 | [ninenines/cowboy](https://github.com/ninenines/cowboy) (31 / 12,893) | [processone/ejabberd](https://github.com/processone/ejabberd) (292 / 134,848) |
| Fish | 45 / 2,052 | [fish-shell/fish-shell](https://github.com/fish-shell/fish-shell) (1,339 / 70,745) | [IlanCosman/tide](https://github.com/IlanCosman/tide) (88 / 2,508) |
| Fortran | 6 / 1,027 | [fortran-lang/stdlib](https://github.com/fortran-lang/stdlib) (21 / 9,841) | [jacobwilliams/json-fortran](https://github.com/jacobwilliams/json-fortran) (6 / 17,068) |
| FSharp | 16 / 412 | [fsprojects/FAKE](https://github.com/fsprojects/FAKE) (340 / 79,422) | [fsprojects/FSharpPlus](https://github.com/fsprojects/FSharpPlus) (164 / 30,266) |
| Func | 1 / 142 | [ton-blockchain/token-contract](https://github.com/ton-blockchain/token-contract) (19 / 1,925) | [ton-blockchain/nominator-pool](https://github.com/ton-blockchain/nominator-pool) (2 / 955) |
| GDScript | 11 / 202 | [Orama-Interactive/Pixelorama](https://github.com/Orama-Interactive/Pixelorama) (211 / 54,170) | [HungryProton/scatter](https://github.com/HungryProton/scatter) (76 / 8,175) |
| GDShader | 0 / 0 | [Orama-Interactive/Pixelorama](https://github.com/Orama-Interactive/Pixelorama) (38 / 2,823) | [gdquest-demos/godot-shaders](https://github.com/gdquest-demos/godot-shaders) (49 / 2,043) |
| Gleam | 12 / 465 | [gleam-lang/stdlib](https://github.com/gleam-lang/stdlib) (19 / 9,699) | [lustre-labs/lustre](https://github.com/lustre-labs/lustre) (27 / 11,562) |
| Gren | 2 / 56 | [gren-lang/core](https://github.com/gren-lang/core) (29 / 15,230) | [gren-lang/node](https://github.com/gren-lang/node) (16 / 5,127) |
| Hare | 0 / 0 | [https://git.sr.ht/~sircmpwn/hare](https://git.sr.ht/~sircmpwn/hare) (756 / 120,957) | [https://git.sr.ht/~sircmpwn/himitsu](https://git.sr.ht/~sircmpwn/himitsu) (34 / 5,389) |
| Haskell | 4 / 47 | [jgm/pandoc](https://github.com/jgm/pandoc) (288 / 106,815) | [koalaman/shellcheck](https://github.com/koalaman/shellcheck) (28 / 19,600) |
| Haxe | 22 / 593 | [HaxeFlixel/flixel](https://github.com/HaxeFlixel/flixel) (223 / 72,661) | [HeapsIO/heaps](https://github.com/HeapsIO/heaps) (545 / 126,917) |
| HLSL | 7 / 522 | [Blinue/Magpie](https://github.com/Blinue/Magpie) (80 / 52,289) | [microsoft/DirectX-Graphics-Samples](https://github.com/microsoft/DirectX-Graphics-Samples) (228 / 10,016) |
| Hoon | 0 / 0 | [urbit/urbit](https://github.com/urbit/urbit) (726 / 145,513) | [yosoyubik/canvas](https://github.com/yosoyubik/canvas) (6 / 19,643) |
| Idris 2 | 0 / 0 | [idris-lang/Idris2](https://github.com/idris-lang/Idris2) (587 / 134,341) | [stefan-hoeck/idris2-pack](https://github.com/stefan-hoeck/idris2-pack) (43 / 10,443) |
| Jai | 1 / 16 | [focus-editor/focus](https://github.com/focus-editor/focus) (161 / 98,443) | [valignatev/hitboxer](https://github.com/valignatev/hitboxer) (31 / 12,655) |
| jq | 0 / 0 | [wader/fq](https://github.com/wader/fq) (47 / 3,910) | [wader/jqjq](https://github.com/wader/jqjq) (1 / 3,172) |
| Julia | 2 / 39 | [JuliaStats/Distributions.jl](https://github.com/JuliaStats/Distributions.jl) (151 / 21,206) | [FluxML/Flux.jl](https://github.com/FluxML/Flux.jl) (42 / 9,716) |
| Koka | 0 / 0 | [koka-lang/koka](https://github.com/koka-lang/koka) (88 / 20,611) | [koka-community/std](https://github.com/koka-community/std) (55 / 6,810) |
| Lean 4 | 0 / 0 | [leanprover-community/batteries](https://github.com/leanprover-community/batteries) (255 / 33,686) | [leanprover-community/aesop](https://github.com/leanprover-community/aesop) (248 / 23,953) |
| Liquidsoap | 0 / 0 | [savonet/liquidsoap](https://github.com/savonet/liquidsoap) (66 / 21,687) | [radiofrance/rf-liquidsoap](https://github.com/radiofrance/rf-liquidsoap) (18 / 1,287) |
| Luau | 3 / 22 | [littensy/charm](https://github.com/littensy/charm) (22 / 2,389) | [Sleitnick/RbxUtil](https://github.com/Sleitnick/RbxUtil) (54 / 13,127) |
| Metal | 1 / 1,079 | [ml-explore/mlx](https://github.com/ml-explore/mlx) (42 / 4,670) | [BradLarson/GPUImage3](https://github.com/BradLarson/GPUImage3) (86 / 3,183) |
| MoonBit | 21 / 1,849 | [moonbitlang/core](https://github.com/moonbitlang/core) (485 / 116,389) | [mizchi/actrun](https://github.com/mizchi/actrun) (75 / 46,431) |
| Motoko | 0 / 0 | [caffeinelabs/motoko-base](https://github.com/caffeinelabs/motoko-base) (48 / 21,704) | [canscale/StableBuffer](https://github.com/canscale/StableBuffer) (1 / 2,628) |
| Move | 49 / 7,409 | [aptos-labs/aptos-core](https://github.com/aptos-labs/aptos-core) (137 / 65,108) | [MystenLabs/sui](https://github.com/MystenLabs/sui) (84 / 18,946) |
| move | 49 / 7,409 | [aptos-labs/aptos-core](https://github.com/aptos-labs/aptos-core) (137 / 65,108) | [MystenLabs/sui](https://github.com/MystenLabs/sui) (84 / 18,946) |
| NetLinx | 0 / 0 | [DavidVine/amx-util-library](https://github.com/DavidVine/amx-util-library) (23 / 7,778) | [rverstappen/AMX](https://github.com/rverstappen/AMX) (82 / 18,042) |
| Nim | 11 / 12,277 | [nim-lang/nimble](https://github.com/nim-lang/nimble) (61 / 20,917) | [zedeus/nitter](https://github.com/zedeus/nitter) (70 / 8,894) |
| Noir | 0 / 0 | [noir-lang/noir-bignum](https://github.com/noir-lang/noir-bignum) (39 / 6,405) | [AztecProtocol/aztec-nr](https://github.com/AztecProtocol/aztec-nr) (194 / 25,767) |
| ObjectscriptUdl | 2 / 230 | [intersystems/ipm](https://github.com/intersystems/ipm) (168 / 37,198) | [intersystems-community/webterminal](https://github.com/intersystems-community/webterminal) (22 / 3,736) |
| OCaml | 29 / 714 | [ocaml/dune](https://github.com/ocaml/dune) (823 / 162,255) | [mirage/mirage](https://github.com/mirage/mirage) (60 / 8,349) |
| OCaml Interface | 5 / 464 | [ocaml/dune](https://github.com/ocaml/dune) (702 / 28,242) | [mirage/mirage](https://github.com/mirage/mirage) (57 / 4,236) |
| Odin | 3 / 132 | [DanielGavin/ols](https://github.com/DanielGavin/ols) (67 / 33,512) | [laytan/odin-http](https://github.com/laytan/odin-http) (30 / 10,652) |
| OpenSCAD | 10 / 77 | [BelfrySCAD/BOSL2](https://github.com/BelfrySCAD/BOSL2) (56 / 86,722) | [nophead/NopSCADlib](https://github.com/nophead/NopSCADlib) (228 / 31,574) |
| P4 Language | 0 / 0 | [p4lang/open-p4studio](https://github.com/p4lang/open-p4studio) (37 / 25,355) | [sonic-net/sonic-pins](https://github.com/sonic-net/sonic-pins) (26 / 4,675) |
| Pact | 0 / 0 | [kadena-io/chainweb-node](https://github.com/kadena-io/chainweb-node) (19 / 11,286) | [kadena-io/marmalade](https://github.com/kadena-io/marmalade) (39 / 9,049) |
| Papyrus | 0 / 0 | [MinLL/SkyrimNet-GamePlugin](https://github.com/MinLL/SkyrimNet-GamePlugin) (109 / 7,934) | [Starfield-Community-Patch/Starfield-Community-Patch](https://github.com/Starfield-Community-Patch/Starfield-Community-Patch) (14 / 5,732) |
| Pony | 3 / 105 | [ponylang/ponyc](https://github.com/ponylang/ponyc) (339 / 66,998) | [WallarooLabs/wally](https://github.com/WallarooLabs/wally) (215 / 55,816) |
| PureScript | 0 / 0 | [purescript-halogen/purescript-halogen](https://github.com/purescript-halogen/purescript-halogen) (24 / 4,141) | [purescript/spago](https://github.com/purescript/spago) (48 / 10,875) |
| QML | 4 / 123 | [KDE/kirigami](https://github.com/KDE/kirigami) (116 / 18,625) | [Swordfish90/cool-retro-term](https://github.com/Swordfish90/cool-retro-term) (26 / 3,723) |
| QuakeC | 0 / 0 | [xonotic/xonotic-data.pk3dir](https://github.com/xonotic/xonotic-data.pk3dir) (697 / 188,559) | [fte-team/fteqw](https://github.com/fte-team/fteqw) (195 / 75,922) |
| Racket | 0 / 0 | [racket/typed-racket](https://github.com/racket/typed-racket) (374 / 63,237) | [greghendershott/frog](https://github.com/greghendershott/frog) (37 / 3,892) |
| Reason | 1 / 3 | [grain-lang/grain](https://github.com/grain-lang/grain) (143 / 63,454) | [esy/esy](https://github.com/esy/esy) (154 / 33,863) |
| Reason Interface | 0 / 0 | [grain-lang/grain](https://github.com/grain-lang/grain) (85 / 5,492) | [esy/esy](https://github.com/esy/esy) (123 / 4,027) |
| Red | 0 / 0 | [red/red](https://github.com/red/red) (265 / 163,942) | [red/code](https://github.com/red/code) (133 / 81,933) |
| REDscript | 0 / 0 | [djkovrik/CP77Mods](https://github.com/djkovrik/CP77Mods) (383 / 55,986) | [psiberx/cp2077-codeware](https://github.com/psiberx/cp2077-codeware) (80 / 6,595) |
| Roc | 0 / 0 | [roc-lang/basic-webserver](https://github.com/roc-lang/basic-webserver) (30 / 8,739) | [smores56/weaver](https://github.com/smores56/weaver) (15 / 5,332) |
| Scala | 14 / 3,083 | [typelevel/cats](https://github.com/typelevel/cats) (678 / 73,014) | [http4s/http4s](https://github.com/http4s/http4s) (425 / 50,854) |
| Solidity | 4 / 787 | [OpenZeppelin/openzeppelin-contracts](https://github.com/OpenZeppelin/openzeppelin-contracts) (352 / 35,117) | [Uniswap/v4-core](https://github.com/Uniswap/v4-core) (44 / 4,494) |
| Sourcepawn | 1 / 2 | [alliedmodders/sourcemod](https://github.com/alliedmodders/sourcemod) (59 / 17,855) | [shavitush/bhoptimer](https://github.com/shavitush/bhoptimer) (22 / 37,736) |
| Squirrel | 0 / 0 | [KelvinShadewing/supertux-advance](https://github.com/KelvinShadewing/supertux-advance) (69 / 51,900) | [R2Northstar/NorthstarMods](https://github.com/R2Northstar/NorthstarMods) (145 / 67,232) |
| Stan | 0 / 0 | [stan-dev/rstanarm](https://github.com/stan-dev/rstanarm) (59 / 4,834) | [paul-buerkner/brms](https://github.com/paul-buerkner/brms) (69 / 2,933) |
| Standard ML | 14 / 195 | [melsman/mlkit](https://github.com/melsman/mlkit) (823 / 174,441) | [diku-dk/smlpkg](https://github.com/diku-dk/smlpkg) (23 / 1,870) |
| Svelte | 42 / 1,905 | [imputnet/cobalt](https://github.com/imputnet/cobalt) (95 / 9,513) | [VERT-sh/VERT](https://github.com/VERT-sh/VERT) (42 / 5,366) |
| Sway | 2 / 22 | [FuelLabs/sway](https://github.com/FuelLabs/sway) (91 / 31,354) | [FuelLabs/sway-libs](https://github.com/FuelLabs/sway-libs) (35 / 7,069) |
| Tact | 20 / 881 | [tact-lang/tact](https://github.com/tact-lang/tact) (14 / 5,128) | [tact-lang/jetton](https://github.com/tact-lang/jetton) (19 / 2,144) |
| TCL | 11 / 6,841 | [tcltk/tklib](https://github.com/tcltk/tklib) (269 / 149,415) | [macports/macports-base](https://github.com/macports/macports-base) (95 / 40,878) |
| Tonel Smalltalk | 0 / 0 | [svenvc/NeoJSON](https://github.com/svenvc/NeoJSON) (22 / 2,337) | [ObjectProfile/Roassal3](https://github.com/ObjectProfile/Roassal3) (731 / 66,058) |
| ucode | 0 / 0 | [openwrt/firewall4](https://github.com/openwrt/firewall4) (13 / 4,378) | [aredn/aredn](https://github.com/aredn/aredn) (27 / 5,980) |
| Vala | 1 / 4 | [GNOME/vala](https://github.com/GNOME/vala) (521 / 170,795) | [elementary/files](https://github.com/elementary/files) (118 / 36,406) |
| VHDL | 22 / 5,315 | [stnolting/neorv32](https://github.com/stnolting/neorv32) (61 / 26,082) | [VUnit/vunit](https://github.com/VUnit/vunit) (116 / 36,870) |
| Wren | 0 / 0 | [wren-lang/wren-cli](https://github.com/wren-lang/wren-cli) (8 / 1,932) | [UnicornsOfDeath/continuous-factory](https://github.com/UnicornsOfDeath/continuous-factory) (1 / 3,158) |
| Apex | 2 / 230 | [apex-enterprise-patterns/fflib-apex-common](https://github.com/apex-enterprise-patterns/fflib-apex-common) (21 / 6,667) | [jongpie/NebulaLogger](https://github.com/jongpie/NebulaLogger) (66 / 16,952) |
| ArkTS Language | 0 / 0 | [openharmony/applications_contacts](https://github.com/openharmony/applications_contacts) (175 / 22,716) | [openharmony/applications_mms](https://github.com/openharmony/applications_mms) (63 / 15,374) |
| OCamllex | 0 / 0 | [ocaml/dune](https://github.com/ocaml/dune) (11 / 1,446) | [reasonml/reason](https://github.com/reasonml/reason) (1 / 1,023) |
| Zeek | 0 / 0 | [zeek/zeek](https://github.com/zeek/zeek) (499 / 62,541) | [mitre-attack/bzar](https://github.com/mitre-attack/bzar) (11 / 4,546) |
| Mojo | 6 / 120 | [Mojo-Numerics-and-Algorithms-group/NuMojo](https://github.com/Mojo-Numerics-and-Algorithms-group/NuMojo) (82 / 42,504) | [Lightbug-HQ/lightbug_http](https://github.com/Lightbug-HQ/lightbug_http) (36 / 9,327) |
| Csound | 0 / 0 | [kunstmusik/csound-live-code](https://github.com/kunstmusik/csound-live-code) (4 / 2,596) | [csudo/csudo](https://github.com/csudo/csudo) (115 / 14,667) |

## Exceptions and companion syntaxes

Projects below 20,000 scoped lines are correctness workloads; larger sources carry an indexing-cost exception. Each exception and maintenance snapshot is recorded per repository in the JSON audit. These choices add one project to each split; they do not guarantee that either split reaches the coverage thresholds.

- **ActionScript:** Mature graphics frameworks; Away3D has little recent maintenance. Legacy-source exception.
- **Agda:** Independent algebra and cubical libraries under the same language organization; cubical is slightly above the preferred size band.
- **AppleScript:** macOS downloader and Alfred workflows. Small correctness workloads; Alfred workflows are legacy source (last push 2016), with application dependencies requiring review.
- **Arduino:** Production firmware. Restrict evaluation to src/ and tasmota/; bundled Arduino libraries and examples overlap. Tasmota exceeds the preferred band.
- **AWK:** Translation application and JSON parser. The parser is deliberately small; this pair exercises correctness rather than search latency.
- **Bluespec SystemVerilog:** Processor and hardware/software interface framework. Mature hardware sources with last pushes in 2023; legacy-source exception.
- **BQN:** Language tools and the Singeli compiler, both implemented partly in BQN. Small same-maintainer exception; separate implementations.
- **C3:** Compiler repository qualifies through lib/std C3 implementations; its C implementation and parser fixtures do not supply this language workload.
- **CFML (Tag):** The registered suffix group includes both tag and script syntax in .cfc/.cfm files. This does not establish coverage of the separately registered .cfs suffix.
- **Curry:** Two self-hosted compiler backends under one umbrella. Exclude the shared Docker example and debugger fixtures; dependencies may share runtime interfaces.
- **DAML:** SDK qualifies through Daml primitive/standard libraries and Daml Script, paired with the separate finance library. Same-organization exception.
- **GDShader:** Pixelorama effects and reusable GDQuest shaders. Small graphics workloads; exclude demonstrations and bundled addon shaders. Godot versions require separate readiness checks.
- **Gren:** Core and Node platform libraries from the language organization; separate modules, same-organization exception.
- **Hare:** Canonical SourceHut standard library and Himitsu secret-storage implementation; license evidence is in COPYING rather than GitHub metadata.
- **HLSL:** Magpie image effects and DirectX MiniEngine/library shaders. Only reusable engine/library code qualifies in the samples repository.
- **jq:** Binary inspection modules and an interpreter implemented in jq. Small same-maintainer exception; separate tools.
- **Koka:** Standard library and community library extensions. Exclude community std/async, which is derived from the language project; retain the separate data-structure and utility implementations.
- **Luau:** State-management and Roblox utility libraries; Roblox APIs must be available to the oracle.
- **Metal:** MLX compute kernels and GPUImage image-processing kernels. Small source subsets with host-language dependencies; GPUImage is mature legacy source.
- **Motoko:** Standard library and persistent buffer implementation. Base is archived; exclude StableBuffer reference/ and tests, which include upstream comparison code.
- **Move:** Aptos and Sui framework implementations use different Move dialects. Exclude their shared upstream compiler/tests and use dialect-appropriate handlers; do not pool oracle results without a dialect label.
- **move:** Alias of the Move suffix group; reuses its repository pair and dialect restrictions.
- **NetLinx:** Utility library and deployed automation source. AMX application is a legacy-source exception (last push 2017). Platform dependencies need a suitable oracle.
- **Noir:** Big-integer library and Aztec contract library; the latter is the official subtree mirror, not an independent second copy of aztec-packages in this corpus.
- **OCaml Interface:** Companion .mli files reuse the OCaml projects and their repository-level split.
- **Pact:** Coin contracts and NFT marketplace contracts are archived legacy production sources. Exclude shared root interface files in the test project.
- **Papyrus:** Separate Skyrim and Starfield mods. Small workloads; game-specific declarations and differing Papyrus dialects need separate readiness checks.
- **Reason Interface:** Companion .rei files reuse the Reason projects and their repository-level split.
- **Red:** Compiler/runtime and curated complete applications/libraries. Exclude showcase/demo scripts in red/code. Red/System .reds files must not be attributed to Cyberpunk REDscript.
- **REDscript:** Gameplay mods and Codeware UI/localization implementations. Exclude Codeware native import stubs; duplicate packaged mod releases are not evaluation source.
- **Stan:** Model and function implementations used by two statistical packages. Small correctness workloads with R-side model assembly and Stan includes to resolve.
- **Sway:** Compiler checkout qualifies through sway-lib-std; pair with separate sway-libs implementations, excluding compiler fixtures.
- **Tact:** Standard-library function implementations and jetton contracts. Deprecated/archived ecosystem accepted as legacy production source; exclude compiler fixtures and builtin stubs.
- **Tonel Smalltalk:** JSON and visualization libraries use Tonel .class.st/.extension.st. Seaside was rejected because its .st files use another serialization format.
- **Wren:** CLI modules and a released puzzle game. Legacy, small-project exception; the single-file game cannot exercise cross-file references or indexing latency.
- **ArkTS Language:** Separate OpenHarmony contacts and messaging applications under one umbrella. Device SDK and declaration resolution remain unverified.
- **OCamllex:** Dune and Reason contain real lexical analyzers with named rules. Small companion-source workloads; this is parser implementation, not parser test fixtures.
- **Csound:** Live-coding library and user-defined opcode library. Exclude live performance/practice snapshots, work-in-progress opcodes, and generated .udo aggregates. CSUDO intentionally keeps each handwritten opcode with a working example in .csd source.

## Unresolved source languages

These are not configuration deferrals. No complete suitable pair was established; discovery results are not an exhaustive survey of every upstream project.

| Language | Remaining gap |
| --- | --- |
| Alex | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| Amber | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| Answer Set Programming | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| Arturo | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| ASP Classic | aspJSON supplies a small real library; a second independent usable repository was not established. |
| Awsum | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| Ayla | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| Baml | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| Bend | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| Bison | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| Cartan | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| Cedar | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| CFML (Script) | The registered suffix is .cfs; inspected production CFML projects use .cfc/.cfm for script syntax. The CFML (Tag) pair is not evidence of .cfs coverage. |
| Cherri | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| Civet | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| Coi | Disambiguate the registered io-eric language from the unrelated coi/coi project. No matching production-source pair established. |
| Cpp2 | cppfront contains predominantly language tests rather than an application written in Cpp2. No independent application pair established. |
| Cypher | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| Dang | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| DataZinc | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| Duso | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| Elle | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| Elsa | The language is oriented toward lambda-calculus teaching; no production application pair established. |
| Ferret | The registered language is Ferret-Language/Ferret, not MontFerret. No second established application identified. |
| Fift | TON provides handwritten Fift tools; wallet repositories contain tiny fragments or generated output. A second handwritten project remains unverified. |
| Genexpr | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| Geno | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| GreyCat | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| GritQL | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| GritQL Snippet | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| GROQ | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| GXL | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| Hera | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| HP-42S | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| HQL | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| Huff | huffmate supplies a reusable contract library, while huff-examples is explicitly example material. A second production repository remains unverified. |
| Ink | Sky Caravan supplies a complete game script; ink-library is example material and ink is a C# compiler. A second production script repository remains unverified. |
| Inko | The language project contains substantial Inko source; the inspected standalone libraries are small exploratory projects. A second established project remains unverified. |
| ISLE | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| Jerry | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| Koto | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| Leo | Compiler .leo files are dominated by test programs. Two independent handwritten application repositories remain unverified. |
| Lisette | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| Literate Haskell | BSC supplies real .lhs implementation; other inspected Haskell applications do not supply a second substantial .lhs workload. |
| Lox | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| Mach | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| mcfunction | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| Menhir | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| MetaScript | Shared .ms suffix matches unrelated sources; no verified pair for the registered language. |
| microScript | Shared .ms suffix matches unrelated sources; the microStudio implementation alone does not establish handwritten microScript application coverage. |
| Minecraft Function | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| MiniZinc | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| MoJu | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| Navi | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| niva | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| NSIS | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| Oat | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| OCaml MLX | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| PDLL | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| pica200 | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| Pine Script | Indicator collections were found, but independent authorship of the second collection has not been established. Do not put potentially copied indicators in opposing splits. |
| PIO Assembly | PicoDVI supplies small handwritten programs; pico-examples is explicitly a collection of examples. No independent application pair established. |
| Poryscript | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| Praia | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| Processing | Compiler repository supplies examples; GenerateMe supplies artistic sketches. Two projects satisfying the application/library selection criteria remain unverified. |
| Qlik | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| rego | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| Rhai | Most compiler .rhai files are examples/tests; the large terrapkg match set is packaging configuration, deferred by the requested scope. |
| Risor | Inspected interpreter implementation is Go, with target-language examples/fixtures. No production-source pair established. |
| Robot | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| Roto | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| Rux | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| SageMath | Inspected Sage projects primarily implement in Python; registered .sage files do not provide a verified standalone pair. |
| Sieve | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| Simula | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| Skript | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| Slang | Compiler fixtures dominate the large match set; the inspected Gaussian rasterizer is small and the similarly named RetroArch shaders use a different shading language. |
| snakemake | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| Soma | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| SOQL | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| SOSL | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| Souffle | Doop supplies a substantial static-analysis implementation; the Souffle compiler contributes target-language fixtures. A second independent implementation remains unverified. |
| Spicy | Zeek supplies production protocol analyzers; the Spicy compiler contributes mostly tests, and a proposed separate analyzer repository was unavailable. |
| spthy | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| Stan Functions | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| Structured Text | OSCAT supplies IEC 61131-3 source. Other .st matches include Smalltalk, while many PLC projects serialize code in XML; a second matching application remains unverified. |
| Surreal Query Language | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| TableGen | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| TLA+ | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| TQL | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| TSRX | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| TyranoScript | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| Uiua | Both inspected math and plotting libraries explicitly label their source Experimental; the compiler contributes mostly fixtures. No pair meets the production-source criterion. |
| Umka | Compiler contains mostly target-language tests; the inspected OS is experimental. No qualifying independent pair established. |
| Umple | A large self-hosted implementation exists; no second independent production source repository established. |
| Unison | The inspected Git repositories do not establish two substantial handwritten .u source projects. Do not substitute compiler tests for application source. |
| Veryl | The compiler is implemented in Rust; its .veryl files and veryl-samples are primarily language test/example material. |
| VEX | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| Vibescript | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| WDL | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| WebAssembly Text Format | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| Whim | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| XQuery | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| Yara | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| Yarn Spinner | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| Yul | Solidity compiler provides Yul test cases, while Solady uses inline Solidity assembly rather than standalone registered .yul source. |
| Yulang | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| ZoKrates | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |
| zwirn | No pair of independent production-source repositories established in this pass. Language-tool sources and search results are leads, not qualified application selections. |

## Deferred registrations

Configuration, schema, document and template coverage can grow incidentally as application repositories are fetched. Other out-of-scope formats are identified explicitly below. No targeted repositories are selected for these entries.

| Language | Reason |
| --- | --- |
| Aleo | Compiled output format; prioritize handwritten Leo source rather than generated Aleo output. |
| Angular | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Animation.txt | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Ansible | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Apache Avro (IDL) | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| ASN.1 | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| ass | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| bazelrc | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Beancount | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Beast | Host-language template format; seek incidental coverage with application repositories. |
| BibTeX | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Bicep | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Bicep Parameters | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Blueprint | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Brainfuck | No named definitions or symbolic references suitable for the requested jump workload. |
| Bruno | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Build2 | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Build2 manifest | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| C# Solution File | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Cabal | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Caddyfile | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Candid | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| CAP CDS | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Cap'n Proto | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Carve | Markup format; seek incidental coverage. |
| CFEngine | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| CODEOWNERS | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| CONL | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Cooklang | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Corn | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| CQL | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| CSS + HubL | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| CUE | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Cylc | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| D2 | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| DBML | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Demo Tape | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Desktop Entry | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| devicetree | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Dhall | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Django | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Djot | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Docker Compose | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| DOT | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Dune | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Duper | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Ebuild | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| ECR | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Edge | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| EDI X12 | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| EJS | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Exograph | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Ferret Lockfile | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Ferret Manifest | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Firebase Rules | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| FlatBuffers | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| FlatZinc | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Fluent | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Fountain | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Freemarker | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| FreeStyleWiki | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| FSH | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| FSM | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| GABC | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Ghostty | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Git Commit | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Git Config | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Git Rebase | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Glimmer (JavaScript) | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Glimmer (TypeScript) | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| GN | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Go HTML Template | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Go Text Template | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Go Work | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Godot Resource | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| GPR | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Grafana Alloy | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Haml | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Helm | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| hl7_v2 | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| hledger | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| hledger-rules | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Hosts | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| HTML + HubL | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| http | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| HubL | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| HuJSON | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Hurl | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| HXML | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Hyprland Config | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| iCal | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| IFC | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Immigrant | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| ion | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| ion_schema | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Jdl | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| JS+ERB | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| JSON Lines | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Jsonnet | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| JSP | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Just | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| KCL | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Kconfig | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Kdl | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| kulala-http | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Latte | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Ledger | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| LikeC4 | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| LilyPond | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Lini | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Linker Script | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Liquid | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| LLVM IR | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Mako | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Marko | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Meson | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Minecraft Lang | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| MJML | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| MLIR | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Modelfile | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Move.toml | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Mustache | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Nautilus | Schema language; defer targeted repository selection. |
| Navi Stream | Data-stream format; defer targeted repository selection. |
| Nginx | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Nickel | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Nim Format String | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Nomad Job | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Numscript | Ledger transaction DSL; defer alongside configuration rather than selecting accounting scenario fixtures. |
| Nunjucks | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Odoc | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| OML | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| OMNeT++ MSG | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| OMNeT++ NED | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| OpenFGA | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| OpenTofu Vars | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| OpenType Feature | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Path of Exile Filter | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Pdxinfo | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Perm | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Pest | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Pkl | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| PlantUML | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| PlatformIO | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| POD | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Polar | Authorization policy DSL; seek incidental coverage in host applications. |
| Prisma | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Pug | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Puppet | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Python constraints | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Python requirements | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Quadlet | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Quarkdown | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Quarto | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Rainbow TSV (⭲) | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| RASI | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| RBS | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| RCL | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Regedit | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| robots.txt | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| RON | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| RPM Spec | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| RsHtml | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| SASS | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| SilverStripe | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Skir | Schema language; defer targeted repository selection. |
| Slim | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Smithy | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| SpiceDB | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Statamic Antlers | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Strace | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Structurizr DSL | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| SysML v2 | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| SystemRDL | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Taskfile | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Templ | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Tera | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Tera (CSS) | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Tera (HTML) | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Tera (JSON) | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Tera (TOML) | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Tera (XML) | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Tera (YAML) | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Terraform Vars | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Textproto | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Thrift | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| TL-B | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| TLA+ Cfg | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| tmux | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Todo | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| TOON | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Turtle | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Txtar | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Typespec | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Ungrammar | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| URDF | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| USD | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| UTL | CMS template format; seek incidental coverage with application repositories. |
| vCard | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Vento | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| VHS | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| ViewTree ($mol) | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| VRL | Transformation scripts embedded in Vector configurations; seek incidental coverage in host applications. |
| WeiXin Markup Language | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| WFG | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| WFL | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| WFS | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| whkd | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Wikitext | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| WIT | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| WoW TOC | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| WPL | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| XDR Syntax Highlight | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| xmake | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| YAML+ERB | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| YANG | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| Yuck | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| ziggy | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
| ziggy-schema | Configuration, schema, document, template, or tool format: defer targeted selection and seek incidental coverage from application repositories. |
