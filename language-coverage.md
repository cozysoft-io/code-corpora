# Corpus language coverage

Source snapshot: 2026-09-08. Regenerate with `python3 corpus_coverage.py`.

Files match registered Zed `path_suffixes`, including exact filenames and compound suffixes, plus aliases `.arturo` (Arturo), `.uiua` (Uiua), and `.simula` (Simula). Matching is case-sensitive. Only strictly valid UTF-8 files count. Lines include blanks and comments; a final unterminated line counts once. Empty files count as files with zero lines.

The scan includes hidden and ignored files, skips `.git` and symlinks, and scans `training/` (the `train/` alias) once. First-line patterns and user overrides are not applied. A file matching several registrations counts toward each language, once per language. Split totals count each file only once. Shared suffixes indicate possible coverage, not a verified language classification.

| Split | UTF-8 files | Raw lines | Rejected non-UTF-8 files | Unmatched files |
| --- | ---: | ---: | ---: | ---: |
| training | 997,484 | 243,903,498 | 975 | 246,648 |
| test | 681,830 | 115,611,466 | 631 | 144,952 |

596 registrations; 582 language names; 1022 unique suffixes/filenames; 302 languages below 21 files or 2,000 raw lines combined. 6 extension inventories unavailable.

Full registrations, pins, per-suffix counts, ambiguities, and failures are in [language-coverage.json](language-coverage.json).

| Language | Suffixes / filenames | Training files | Training lines | Test files | Test lines | Below threshold |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| ActionScript | `as` | 192 | 43,100 | 478 | 92,563 | no |
| Ada | `adb`, `ads` | 499 | 105,185 | 479 | 67,254 | no |
| Agda | `agda` | 1,263 | 149,161 | 1,205 | 203,603 | no |
| Aiken | `ak` | 56 | 15,962 | 34 | 7,326 | no |
| AL | `al`, `dal` | 36 | 15,943 | 111 | 17,515 | no |
| Aleo | `aleo` | 0 | 0 | 0 | 0 | yes |
| Alex | `x` | 9 | 804 | 2 | 70 | yes |
| Amber | `ab` | 1 | 10 | 0 | 0 | yes |
| Angular | `component.html`, `ng.html` | 11 | 1,197 | 3 | 78 | yes |
| Animation.txt | `animation.txt` | 0 | 0 | 0 | 0 | yes |
| Ansible | `ansible` | 0 | 0 | 0 | 0 | yes |
| Answer Set Programming | `asp`, `lp` | 0 | 0 | 1 | 1 | yes |
| Apache Avro (IDL) | `avdl` | 0 | 0 | 0 | 0 | yes |
| Apex | `apex`, `apex-anon`, `cls`, `trigger` | 428 | 67,810 | 278 | 60,911 | no |
| AppleScript | `applescript`, `scpt` | 13 | 14,455 | 30 | 2,252 | no |
| Arduino | `ino` | 690 | 110,620 | 869 | 355,455 | no |
| ArkTS Language | `ets` | 175 | 22,716 | 63 | 15,374 | no |
| Arturo | `art`, `arturo` | 2 | 4 | 0 | 0 | yes |
| AsciiDoc | `ad`, `adoc`, `asc`, `asciidoc` | 582 | 71,108 | 8 | 2,365 | no |
| AsciiDoc Inline | — | 0 | 0 | 0 | 0 | no filename registration |
| ASN.1 | `mib` | 0 | 0 | 0 | 0 | yes |
| ASP Classic | `asa`, `asp` | 0 | 0 | 1 | 1 | yes |
| ass | `ass`, `ssa` | 0 | 0 | 0 | 0 | yes |
| Assembly | `S`, `asm`, `s` | 461 | 101,236 | 199 | 25,127 | no |
| Astro | `astro` | 230 | 5,034 | 0 | 0 | no |
| AutoHotkey | `ahk` | 33 | 11,134 | 27 | 8,354 | no |
| AWK | `awk` | 36 | 10,651 | 3 | 740 | no |
| Awsum | `aww` | 0 | 0 | 0 | 0 | yes |
| Ayla | `ayl`, `ayla` | 0 | 0 | 0 | 0 | yes |
| Baml | `baml` | 0 | 0 | 0 | 0 | yes |
| Batch | `bat`, `cmd` | 206 | 12,316 | 104 | 5,252 | no |
| bazelrc | `bazelrc` | 7 | 472 | 3 | 27 | yes |
| Beancount | `bean`, `beancount` | 0 | 0 | 0 | 0 | yes |
| Beast | `btsx` | 0 | 0 | 0 | 0 | yes |
| Bend | `bend` | 0 | 0 | 0 | 0 | yes |
| BibTeX | `bib`, `biblatex`, `bibtex` | 19 | 10,858 | 12 | 3,214 | no |
| Bicep | `bicep` | 1 | 4 | 0 | 0 | yes |
| Bicep Parameters | `bicepparam` | 0 | 0 | 0 | 0 | yes |
| Bison | `y`, `yy` | 20 | 16,633 | 11 | 4,198 | no |
| bitbake | `bb`, `bbappend`, `bbclass`, `conf`, `inc` | 780 | 116,053 | 495 | 36,824 | no |
| Blade | `blade.php` | 198 | 2,425 | 1 | 196 | no |
| Blueprint | `blp` | 1 | 11 | 0 | 0 | yes |
| Bluespec SystemVerilog | `bsv` | 210 | 75,584 | 421 | 75,930 | no |
| BQN | `bqn` | 52 | 7,056 | 8 | 2,461 | no |
| Brainfuck | `bf` | 0 | 0 | 0 | 0 | yes |
| Bruno | `bru` | 0 | 0 | 0 | 0 | yes |
| Bsl | `bsl` | 333 | 233,089 | 6 | 9,578 | no |
| Build2 | `build`, `buildfile` | 56 | 4,438 | 34 | 1,654 | no |
| Build2 manifest | `manifest` | 35 | 717 | 7 | 153 | yes |
| C | `c` | 5,572 | 50,927,094 | 3,061 | 2,871,933 | no |
| C# Project File | `csproj` | 166 | 29,177 | 68 | 2,004 | no |
| C# Solution File | `slnx` | 12 | 369 | 31 | 369 | yes |
| C++ | `C`, `H`, `c++`, `c++m`, `cc`, `ccm`, `cpp`, `cppm`, `cu`, `cuh`, `cxx`, `cxxm`, `h`, `h++`, `hh`, `hip`, `hpp`, `hxx`, `inl`, `ino`, `ipp`, `ixx` | 43,372 | 19,671,556 | 10,971 | 3,369,858 | no |
| C3 | `c3`, `c3i` | 1,440 | 143,579 | 52 | 19,282 | no |
| Cabal | `cabal` | 24 | 4,994 | 2 | 206 | no |
| Caddyfile | `Caddyfile`, `caddyfile` | 5 | 347 | 0 | 0 | yes |
| Cadence | `cdc` | 385 | 24,957 | 146 | 8,783 | no |
| Cairo | `cairo` | 321 | 63,387 | 229 | 49,234 | no |
| Candid | `did` | 0 | 0 | 0 | 0 | yes |
| CAP CDS | `cds` | 0 | 0 | 0 | 0 | yes |
| Cap'n Proto | `capnp` | 15 | 2,418 | 1 | 952 | yes |
| Cartan | `cart` | 0 | 0 | 0 | 0 | yes |
| Carve | `crv` | 0 | 0 | 0 | 0 | yes |
| Cedar | `cedar` | 0 | 0 | 0 | 0 | yes |
| CFEngine | `cf`, `cf.sub`, `cf3`, `cfengine`, `cfengine3` | 2 | 8 | 0 | 0 | yes |
| CFML (Query) | — | 0 | 0 | 0 | 0 | no filename registration |
| CFML (Script) | `cfs` | 0 | 0 | 0 | 0 | yes |
| CFML (Tag) | `cfc`, `cfm`, `cfml` | 657 | 93,465 | 305 | 13,273 | no |
| Cherri | `cherri` | 0 | 0 | 0 | 0 | yes |
| Circom | `circom` | 104 | 31,779 | 37 | 3,737 | no |
| Civet | `civet` | 0 | 0 | 0 | 0 | yes |
| Clarity | `clar` | 6 | 1,150 | 364 | 98,558 | no |
| Clojure | `bb`, `clj`, `cljc`, `cljd`, `cljs`, `edn` | 356 | 77,992 | 83 | 8,026 | no |
| CMake | `CMakeLists.txt`, `cmake` | 1,158 | 99,858 | 289 | 24,411 | no |
| COBOL | `cbl`, `cob` | 206 | 29,442 | 5 | 4,056 | no |
| CODEOWNERS | `CODEOWNERS`, `CODEOWNERS.txt` | 35 | 392 | 38 | 149 | yes |
| CoffeeScript | `coffee` | 170 | 7,348 | 142 | 14,964 | no |
| Coi | `coi`, `d.coi` | 0 | 0 | 0 | 0 | yes |
| comment | — | 0 | 0 | 0 | 0 | no filename registration |
| CONL | `conl` | 0 | 0 | 0 | 0 | yes |
| Cooklang | `cook` | 0 | 0 | 0 | 0 | yes |
| Corn | `corn` | 0 | 0 | 0 | 0 | yes |
| Cpp2 | `cpp2`, `h2` | 0 | 0 | 0 | 0 | yes |
| CQL | `cql` | 6 | 356 | 0 | 0 | yes |
| Crystal | `cr` | 96 | 15,879 | 251 | 21,219 | no |
| CSharp | `cs` | 6,158 | 838,886 | 2,181 | 274,579 | no |
| Csound | `csd`, `orc`, `sco`, `udo` | 170 | 12,793 | 155 | 29,276 | no |
| CSS | `css`, `pcss`, `postcss` | 3,988 | 1,253,316 | 2,786 | 293,950 | no |
| CSS + HubL | `hubl.css` | 0 | 0 | 0 | 0 | yes |
| CSV | `csv` | 93 | 70,328 | 116 | 35,881 | no |
| CUE | `cue` | 3 | 14 | 0 | 0 | yes |
| Curry | `curry` | 83 | 9,088 | 151 | 13,906 | no |
| Cylc | `cylc` | 5 | 835 | 0 | 0 | yes |
| Cypher | `cql`, `cyp`, `cypher` | 6 | 356 | 0 | 0 | yes |
| Cython | `pxd`, `pxi`, `pyx` | 87 | 22,076 | 56 | 28,077 | no |
| D | `d`, `dd`, `di` | 3,582 | 57,112 | 2,868 | 50,612 | no |
| D2 | `d2` | 1 | 116 | 0 | 0 | yes |
| Dafny | `dfy` | 109 | 20,978 | 37 | 9,725 | no |
| DAML | `daml` | 1,125 | 64,630 | 634 | 75,502 | no |
| Dang | `dang` | 0 | 0 | 0 | 0 | yes |
| Dart | `dart` | 5,288 | 951,816 | 984 | 286,691 | no |
| DataZinc | `dzn` | 0 | 0 | 0 | 0 | yes |
| DBML | `dbml` | 1 | 19 | 0 | 0 | yes |
| Defold | `gui_script`, `lua`, `render_script`, `script` | 3,345 | 714,614 | 4,054 | 323,146 | no |
| Demo Tape | `tape` | 1 | 99 | 0 | 0 | yes |
| Desktop Entry | `desktop`, `directory` | 20 | 375 | 5 | 86 | yes |
| devicetree | `dts`, `dtsi`, `dtso`, `its` | 0 | 0 | 1 | 8 | yes |
| Dhall | `dhall` | 20 | 167 | 4 | 10 | yes |
| Diff | `diff`, `patch` | 175 | 38,704 | 125 | 17,384 | no |
| Django | `dj.html`, `dj.md`, `dj.txt` | 0 | 0 | 0 | 0 | yes |
| Djot | `dj`, `djot` | 9 | 1,953 | 1 | 149 | yes |
| Docker Compose | `compose.yaml`, `compose.yml`, `docker-compose.yaml`, `docker-compose.yml` | 33 | 2,137 | 33 | 1,894 | no |
| Dockerfile | `Containerfile`, `Dockerfile`, `dockerfile` | 178 | 7,143 | 121 | 4,341 | no |
| DOT | `DOT`, `dot`, `gv` | 9 | 161 | 10 | 619 | yes |
| Doxygen | — | 0 | 0 | 0 | 0 | no filename registration |
| DuckyScript | `txt` | 11,953 | 4,224,492 | 4,308 | 746,804 | no |
| Dune | `dune`, `dune-project`, `dune-workspace` | 2,169 | 20,306 | 64 | 1,074 | no |
| Duper | `duper` | 0 | 0 | 0 | 0 | yes |
| Duso | `du` | 0 | 0 | 0 | 0 | yes |
| Dylan | `dylan`, `lid` | 78 | 12,481 | 14 | 4,185 | no |
| Earthfile | `Earthfile` | 187 | 10,790 | 0 | 0 | no |
| EBNF | `bnf`, `ebnf` | 118 | 2,045 | 100 | 3,757 | no |
| Ebuild | `ebuild` | 0 | 0 | 0 | 0 | yes |
| ECR | `ecr` | 6 | 31 | 4 | 21 | yes |
| Edge | `edge` | 1 | 7 | 0 | 0 | yes |
| EDI X12 | `x12` | 1 | 1,489 | 0 | 0 | yes |
| Editorconfig | `editorconfig` | 1,241 | 27,221 | 653 | 12,531 | no |
| EEx | `eex` | 175 | 9,812 | 79 | 1,142 | no |
| EJS | `ejs`, `eta` | 53 | 3,142 | 42 | 888 | no |
| EL | — | 0 | 0 | 0 | 0 | no filename registration |
| Elisp | `el` | 81 | 45,189 | 32 | 24,354 | no |
| Elixir | `ex`, `exs`, `mix.lock` | 2,980 | 688,103 | 2,754 | 334,529 | no |
| Elle | `le` | 0 | 0 | 0 | 0 | yes |
| Elm | `elm` | 119 | 25,787 | 481 | 87,416 | no |
| Elsa | `lc` | 0 | 0 | 0 | 0 | yes |
| EmmyLua | `lua`, `lua.txt` | 3,341 | 710,309 | 4,050 | 322,497 | no |
| EmmyLuadoc | — | 0 | 0 | 0 | 0 | no filename registration |
| env | `conf`, `env`, `envrc`, `example`, `local`, `test` | 2,729 | 4,363,101 | 927 | 377,811 | no |
| ERB | `erb` | 504 | 12,378 | 650 | 20,288 | no |
| Erlang | `Emakefile`, `app.src`, `erl`, `erlang`, `escript`, `hrl`, `rebar.config`, `xrl`, `yrl` | 201 | 46,780 | 398 | 160,303 | no |
| Exograph | `exo` | 0 | 0 | 0 | 0 | yes |
| Ferret | `fer` | 0 | 0 | 0 | 0 | yes |
| Ferret Lockfile | `ferret.lock` | 0 | 0 | 0 | 0 | yes |
| Ferret Manifest | `fer.ret` | 0 | 0 | 0 | 0 | yes |
| Fift | `fif` | 16 | 3,128 | 12 | 1,666 | no |
| Firebase Rules | `firebase.rules`, `rules`, `storage.rules` | 9 | 395 | 11 | 196 | yes |
| Fish | `fish` | 1,634 | 95,248 | 124 | 4,146 | no |
| FlatBuffers | `fbs` | 6 | 364 | 0 | 0 | yes |
| FlatZinc | `fzn` | 0 | 0 | 0 | 0 | yes |
| Fluent | `ftl` | 14 | 43 | 8 | 64 | yes |
| Fortran | `F`, `F03`, `F08`, `F90`, `F95`, `f`, `f03`, `f08`, `f90`, `f95` | 421 | 38,136 | 64 | 26,431 | no |
| Fountain | `fountain`, `spmd` | 0 | 0 | 0 | 0 | yes |
| Freemarker | `ftl` | 14 | 43 | 8 | 64 | yes |
| FreeStyleWiki | `fsw`, `fswiki` | 0 | 0 | 0 | 0 | yes |
| FSH | `fsh` | 0 | 0 | 0 | 0 | yes |
| FSharp | `fs`, `fsi`, `fsscript`, `fsx` | 462 | 98,053 | 217 | 44,521 | no |
| FSM | `fsm` | 0 | 0 | 0 | 0 | yes |
| Func | `fc` | 53 | 7,123 | 3 | 1,265 | no |
| G-code | `001`, `S`, `anc`, `apt`, `aptcl`, `bfb`, `cls`, `cnc`, `din`, `dnc`, `ecs`, `eia`, `fan`, `fgc`, `fnc`, `g`, `g00`, `gc`, `gcd`, `gco`, `gcode`, `gp`, `hnc`, `knc`, `lib`, `m`, `min`, `mmg`, `mpf`, `mpt`, `nc`, `ncd`, `ncf`, `ncg`, `nci`, `ncp`, `ngc`, `out`, `pim`, `pit`, `plt`, `ply`, `prg`, `pu1`, `rol`, `sbp`, `spf`, `ssb`, `sub`, `tap`, `tcn`, `xpi` | 3,088 | 257,260 | 421 | 102,203 | no |
| GABC | `gabc` | 0 | 0 | 0 | 0 | yes |
| GDScript | `gd` | 261 | 59,576 | 146 | 11,563 | no |
| GDShader | `gdshader`, `gdshaderinc` | 40 | 2,864 | 63 | 2,700 | no |
| Genexpr | `genexpr` | 0 | 0 | 0 | 0 | yes |
| Geno | `geno` | 0 | 0 | 0 | 0 | yes |
| Gherkin | `feature`, `gherkin` | 237 | 40,343 | 0 | 0 | no |
| Ghostty | `com.mitchellh.ghostty/config`, `config/ghostty/config`, `ghostty`, `ghostty/config` | 0 | 0 | 0 | 0 | yes |
| Git Attributes | `.gitattributes`, `gitattributes` | 598 | 7,855 | 196 | 1,155 | no |
| Git Commit | `COMMIT_EDITMSG`, `EDIT_DESCRIPTION`, `MERGE_MSG`, `NOTES_EDITMSG`, `TAG_EDITMSG` | 2 | 2 | 1 | 1 | yes |
| Git Config | `.gitconfig`, `.gitmodules`, `.lfsconfig`, `config.worktree` | 67 | 559 | 26 | 204 | yes |
| Git Ignore | `.containerignore`, `.cursorignore`, `.dockerignore`, `.eslintignore`, `.fdignore`, `.git-blame-ignore-revs`, `.gitignore`, `.gitignore_global`, `.ignore`, `.npmignore`, `.prettierignore`, `.rgignore`, `.vscodeignore` | 2,536 | 41,902 | 1,526 | 18,218 | no |
| Git Rebase | `git-rebase-todo` | 3 | 180 | 0 | 0 | yes |
| GitHub Actions | — | 0 | 0 | 0 | 0 | no filename registration |
| Gleam | `gleam` | 54 | 19,758 | 80 | 22,537 | no |
| Glimmer (JavaScript) | `gjs` | 5 | 429 | 32 | 557 | yes |
| Glimmer (TypeScript) | `gts` | 5 | 531 | 22 | 373 | yes |
| GLSL | `comp`, `frag`, `geom`, `glsl`, `mesh`, `rahit`, `rcall`, `rchit`, `rgen`, `rint`, `rmiss`, `task`, `tesc`, `tese`, `vert` | 125 | 5,807 | 162 | 8,186 | no |
| GN | `.gn`, `BUILD.gn`, `gn`, `gni` | 1 | 10 | 0 | 0 | yes |
| Go | `go` | 4,686 | 1,110,805 | 1,030 | 236,736 | no |
| Go HTML Template | `gohtml`, `html.gotmpl`, `html.gotpl` | 0 | 0 | 0 | 0 | yes |
| Go Mod | `mod` | 217 | 3,050 | 22 | 1,044 | no |
| Go Sum | `go.sum` | 73 | 10,293 | 18 | 3,659 | no |
| Go Text Template | `go.tpl`, `go.txt`, `gotmpl`, `gtpl`, `txt.gotmpl`, `txt.gotpl` | 8 | 12,812 | 0 | 0 | yes |
| Go Work | `work` | 0 | 0 | 0 | 0 | yes |
| Godot Resource | `gdextension`, `godot`, `import`, `tres`, `tscn` | 354 | 28,671 | 436 | 23,774 | no |
| GPR | `gpr` | 82 | 1,333 | 40 | 1,047 | no |
| Gradle | `gradle` | 48 | 3,876 | 302 | 8,191 | no |
| Gradle KTS | `gradle.kts` | 440 | 22,180 | 105 | 7,700 | no |
| Grafana Alloy | `alloy` | 0 | 0 | 0 | 0 | yes |
| GraphQL | `gql`, `graphql`, `graphqls` | 111 | 6,957 | 12 | 70,575 | no |
| Gren | `gren` | 53 | 21,586 | 27 | 7,468 | no |
| GreyCat | `gcl` | 0 | 0 | 0 | 0 | yes |
| GritQL | `grit` | 0 | 0 | 0 | 0 | yes |
| GritQL Snippet | `gritqlsnippet` | 0 | 0 | 0 | 0 | yes |
| Groovy | `JenkinsFile`, `Jenkinsfile`, `gradle`, `groovy` | 72 | 6,221 | 306 | 8,493 | no |
| GROQ | `groq` | 0 | 0 | 0 | 0 | yes |
| GXL | `gxl` | 0 | 0 | 0 | 0 | yes |
| Haml | `haml`, `html.haml` | 25 | 140 | 0 | 0 | yes |
| Handlebars | `handlebars`, `hbs` | 284 | 6,313 | 116 | 5,458 | no |
| Hare | `ha` | 856 | 136,813 | 34 | 5,389 | no |
| Haskell | `hs` | 1,147 | 356,013 | 87 | 26,658 | no |
| Haxe | `hx` | 370 | 97,998 | 595 | 133,115 | no |
| HCL | `hcl` | 111 | 4,400 | 1 | 244 | no |
| HEEx | `heex`, `html.eex`, `leex`, `neex` | 30 | 3,127 | 182 | 10,760 | no |
| Helm | `.helmignore` | 7 | 96 | 48 | 415 | yes |
| Hera | `hera` | 0 | 0 | 0 | 0 | yes |
| hl7_v2 | `hl7` | 1 | 1,584 | 0 | 0 | yes |
| hledger | `hledger`, `journal`, `ledger` | 33 | 1,577 | 0 | 0 | yes |
| hledger-rules | `rules` | 9 | 395 | 11 | 196 | yes |
| HLSL | `hlsl` | 130 | 100,382 | 382 | 23,095 | no |
| HOCON | `conf`, `hocon` | 307 | 17,885 | 81 | 3,560 | no |
| Hoon | `hoon` | 828 | 173,495 | 6 | 19,643 | no |
| Hosts | `hosts` | 1 | 3 | 2 | 4 | yes |
| HP-42S | `42s`, `hp42s` | 0 | 0 | 0 | 0 | yes |
| HQL | `hx` | 370 | 97,998 | 595 | 133,115 | no |
| HTML | `htm`, `html`, `shtml` | 10,018 | 2,295,992 | 2,198 | 486,738 | no |
| HTML + HubL | `hubl.html` | 0 | 0 | 0 | 0 | yes |
| HTML+ERB | `html.erb` | 316 | 7,032 | 615 | 18,952 | no |
| HTML-Jinja | `j2`, `jinja`, `jinja2` | 6 | 266 | 52 | 7,933 | no |
| http | `http` | 3 | 219 | 0 | 0 | yes |
| HubL | `hubl` | 0 | 0 | 0 | 0 | yes |
| Huff | `huff` | 0 | 0 | 0 | 0 | yes |
| HuJSON | `hujson`, `jwcc` | 0 | 0 | 0 | 0 | yes |
| Hurl | `hurl` | 20 | 203 | 0 | 0 | yes |
| HXML | `hxml` | 6 | 20 | 8 | 81 | yes |
| Hyprland Config | `hyprland.conf`, `hyprland.hl`, `hyprlandd.conf`, `hyprlandd.hl` | 0 | 0 | 0 | 0 | yes |
| Hyprlang | `conf`, `hl` | 307 | 17,885 | 81 | 3,560 | no |
| iCal | `ics` | 0 | 0 | 0 | 0 | yes |
| Idris 2 | `idr`, `idr2` | 1,935 | 181,145 | 45 | 10,506 | no |
| IFC | `ifc` | 0 | 0 | 0 | 0 | yes |
| Immigrant | `schema` | 0 | 0 | 0 | 0 | yes |
| Inform 6 | `h`, `inf` | 32,725 | 15,249,911 | 6,079 | 1,601,431 | no |
| ini | `automount`, `build`, `cfg`, `conf`, `container`, `image`, `inf`, `ini`, `kube`, `mount`, `network`, `path`, `pod`, `scope`, `service`, `slice`, `socket`, `swap`, `target`, `timer`, `volume` | 751 | 62,543 | 375 | 28,224 | no |
| Ink | `ink` | 4 | 2,214 | 0 | 0 | yes |
| Inko | `inko` | 0 | 0 | 0 | 0 | yes |
| ion | `ion` | 1 | 20 | 0 | 0 | yes |
| ion_schema | `isl` | 2 | 764 | 0 | 0 | yes |
| ISLE | `isle` | 0 | 0 | 2 | 3,203 | yes |
| Jai | `jai` | 210 | 128,032 | 47 | 49,905 | no |
| Janet | `janet` | 0 | 0 | 99 | 13,508 | no |
| Java | `java` | 7,907 | 1,105,018 | 4,759 | 598,616 | no |
| JavaScript | `cjs`, `js`, `jsx`, `mjs` | 439,210 | 80,777,485 | 336,966 | 60,106,002 | no |
| Jdl | `jdl` | 0 | 0 | 0 | 0 | yes |
| Jerry | `jer` | 0 | 0 | 0 | 0 | yes |
| Jinja-Inline | — | 0 | 0 | 0 | 0 | no filename registration |
| Jinja2 | `jinja`, `jinja2` | 5 | 226 | 49 | 7,872 | no |
| Jinja2 Inline | — | 0 | 0 | 0 | 0 | no filename registration |
| jq | `jq` | 56 | 4,779 | 2 | 3,206 | no |
| JS+ERB | `js.erb` | 3 | 42 | 12 | 112 | yes |
| JSDoc | — | 0 | 0 | 0 | 0 | no filename registration |
| JSON | `deno.lock`, `flake.lock`, `geojson`, `json`, `json.dist`, `prettierrc`, `topojson` | 63,328 | 19,373,499 | 42,301 | 8,753,602 | no |
| JSON Lines | `jsonl`, `ndjson` | 2 | 7 | 15 | 678 | yes |
| JSON5 | `json5` | 196 | 13,443 | 53 | 1,493 | no |
| JSONC | `babelrc`, `bun.lock`, `devcontainer.json`, `eslintrc`, `jshintrc`, `jsonc`, `luaurc`, `pyrightconfig.json`, `stylelintrc`, `swcrc`, `tsconfig.json` | 4,991 | 90,779 | 2,764 | 49,944 | no |
| Jsonnet | `jsonnet`, `libsonnet` | 3 | 139 | 0 | 0 | yes |
| JSP | `jsp`, `jspf`, `tag` | 0 | 0 | 7 | 7 | yes |
| Julia | `jl` | 258 | 32,765 | 96 | 17,138 | no |
| Just | `JUSTFILE`, `Justfile`, `just`, `justfile` | 29 | 1,361 | 11 | 262 | yes |
| KCL | `k` | 0 | 0 | 0 | 0 | yes |
| Kconfig | `Kconfig` | 0 | 0 | 1 | 258 | yes |
| Kdl | `kdl` | 20 | 729 | 0 | 0 | yes |
| Koka | `kk` | 1,104 | 115,196 | 89 | 9,597 | no |
| Kotlin | `kt`, `kts` | 6,494 | 817,034 | 4,407 | 482,719 | no |
| Koto | `koto` | 1 | 4 | 0 | 0 | yes |
| kulala-http | `http` | 3 | 219 | 0 | 0 | yes |
| LaTeX | `cls`, `latex`, `sty`, `tex` | 535 | 103,777 | 434 | 105,374 | no |
| Latte | `latte` | 0 | 0 | 0 | 0 | yes |
| Lean 4 | `lean` | 468 | 93,031 | 250 | 24,242 | no |
| Ledger | `journal`, `ldg`, `ldgr`, `ledger` | 33 | 1,577 | 0 | 0 | yes |
| Leo | `leo` | 0 | 0 | 0 | 0 | yes |
| LESS | `less` | 96 | 5,100 | 745 | 59,929 | no |
| LikeC4 | `c4`, `likec4` | 0 | 0 | 0 | 0 | yes |
| LilyPond | `ily`, `ly` | 0 | 0 | 0 | 0 | yes |
| LilyPond Scheme | — | 0 | 0 | 0 | 0 | no filename registration |
| Lini | `lini` | 0 | 0 | 0 | 0 | yes |
| Linker Script | `ld` | 22 | 5,594 | 1 | 9 | no |
| Liquid | `liquid` | 3 | 9 | 0 | 0 | yes |
| Liquidsoap | `liq` | 632 | 46,556 | 23 | 1,403 | no |
| Lisette | `lis` | 0 | 0 | 0 | 0 | yes |
| Literate Haskell | `lhs` | 3 | 69 | 0 | 0 | yes |
| LLVM IR | `ll` | 19 | 11,099 | 5 | 105 | no |
| LOG | `log` | 1,225 | 99,706 | 18 | 4,354 | no |
| Logcat | `log`, `logcat` | 1,225 | 99,706 | 18 | 4,354 | no |
| Logstash Config | `conf` | 307 | 17,885 | 81 | 3,560 | no |
| Lox | `lox` | 0 | 0 | 0 | 0 | yes |
| Lua | `lua` | 3,338 | 709,494 | 4,050 | 322,497 | no |
| Luau | `luau` | 61 | 6,808 | 69 | 16,363 | no |
| Mach | `mach` | 0 | 0 | 0 | 0 | yes |
| Make | `GNUmakefile`, `Makefile`, `OCamlMakefile`, `mak`, `makefile`, `mk` | 919 | 67,597 | 654 | 34,277 | no |
| Mako | `mako` | 0 | 0 | 0 | 0 | yes |
| Markdown | `MD`, `markdown`, `md`, `mdc`, `mdwn`, `mdx` | 54,870 | 8,871,008 | 36,438 | 5,736,831 | no |
| Markdown Inline | — | 0 | 0 | 0 | 0 | no filename registration |
| Markdown-Inline | — | 0 | 0 | 0 | 0 | no filename registration |
| Marko | `marko` | 0 | 0 | 0 | 0 | yes |
| MATLAB | `m` | 604 | 92,530 | 118 | 17,204 | no |
| mcfunction | `mcfunction` | 0 | 0 | 0 | 0 | yes |
| MDX | `mdx` | 618 | 145,760 | 1,048 | 182,432 | no |
| Menhir | `mly` | 21 | 2,201 | 3 | 5,568 | no |
| Mermaid | `mermaid`, `mmd` | 170 | 17,737 | 0 | 0 | no |
| Meson | `meson.build`, `meson.options`, `meson_options.txt` | 56 | 4,322 | 25 | 1,031 | no |
| Metal | `metal` | 44 | 5,796 | 86 | 3,183 | no |
| MetaScript | `cms`, `ems`, `jms`, `ms`, `rms`, `wms` | 5 | 1,636 | 1 | 123 | yes |
| microScript | `ms` | 5 | 1,636 | 1 | 123 | yes |
| Minecraft Function | `mcfunction` | 0 | 0 | 0 | 0 | yes |
| Minecraft Lang | `lang` | 2 | 216 | 0 | 0 | yes |
| MiniZinc | `mzn` | 0 | 0 | 0 | 0 | yes |
| MJML | `mjml` | 9 | 114 | 0 | 0 | yes |
| MLIR | `mlir` | 0 | 0 | 0 | 0 | yes |
| Modelfile | `Modelfile` | 0 | 0 | 0 | 0 | yes |
| Mojo | `mojo` | 129 | 50,571 | 62 | 13,453 | no |
| MoJu | `mju` | 0 | 0 | 0 | 0 | yes |
| MoonBit | `mbt` | 895 | 219,134 | 99 | 66,009 | no |
| Motoko | `mo` | 87 | 50,087 | 3 | 9,029 | no |
| Move | `move` | 4,886 | 459,616 | 4,558 | 231,542 | no |
| move | `move` | 4,886 | 459,616 | 4,558 | 231,542 | no |
| Move.toml | `Move.toml` | 480 | 4,462 | 1,046 | 8,093 | no |
| MSBuild File | `proj`, `props`, `targets` | 130 | 5,595 | 82 | 2,435 | no |
| Mustache | `mustache` | 14 | 396 | 31 | 3,590 | no |
| Nautilus | `nautilus` | 0 | 0 | 0 | 0 | yes |
| Navi | `navi`, `nv` | 0 | 0 | 0 | 0 | yes |
| Navi Stream | `nvs` | 0 | 0 | 0 | 0 | yes |
| NetLinx | `axb`, `axi`, `axs`, `lib` | 24 | 7,952 | 84 | 18,126 | no |
| Nginx | `nginx.conf` | 7 | 565 | 0 | 0 | yes |
| Nickel | `ncl` | 2 | 8 | 0 | 0 | yes |
| Nim | `nim`, `nims` | 303 | 49,718 | 73 | 9,081 | no |
| Nim Format String | `nim_format_string` | 0 | 0 | 0 | 0 | yes |
| niva | `niva` | 0 | 0 | 0 | 0 | yes |
| Nix | `nix` | 132 | 9,713 | 40 | 5,368 | no |
| Noir | `nr` | 50 | 9,481 | 248 | 36,180 | no |
| Nomad ACL | — | 0 | 0 | 0 | 0 | no filename registration |
| Nomad Agent | — | 0 | 0 | 0 | 0 | no filename registration |
| Nomad CSI Volume | — | 0 | 0 | 0 | 0 | no filename registration |
| Nomad Dynamic Host Volume | — | 0 | 0 | 0 | 0 | no filename registration |
| Nomad Job | `nomad`, `nomad.hcl` | 0 | 0 | 0 | 0 | yes |
| Nomad Namespace | — | 0 | 0 | 0 | 0 | no filename registration |
| Nomad Node Pool | — | 0 | 0 | 0 | 0 | no filename registration |
| Nomad Resource Quota | — | 0 | 0 | 0 | 0 | no filename registration |
| Nomad Variable | — | 0 | 0 | 0 | 0 | no filename registration |
| NSIS | `nsh`, `nsi` | 4 | 624 | 0 | 0 | yes |
| Nu | `nu`, `nuon` | 120 | 15,066 | 3 | 747 | no |
| Numscript | `num`, `numscript` | 0 | 0 | 0 | 0 | yes |
| Nunjucks | `njk` | 4 | 28 | 0 | 0 | yes |
| Oat | `oat` | 0 | 0 | 0 | 0 | yes |
| Oberon | `Mod`, `mod` | 217 | 3,050 | 22 | 1,044 | no |
| Objective-C | `h`, `hh`, `m`, `mm` | 33,417 | 15,358,780 | 6,501 | 1,685,137 | no |
| objectscript | — | 0 | 0 | 0 | 0 | no filename registration |
| ObjectScript XML | `xml` | 2,479 | 290,990 | 3,764 | 565,728 | no |
| objectscript_routine | `inc`, `int`, `mac`, `rtn` | 429 | 97,917 | 414 | 33,313 | no |
| ObjectscriptUdl | `cls` | 428 | 67,810 | 262 | 60,598 | no |
| OCaml | `ml` | 2,729 | 358,069 | 234 | 43,336 | no |
| OCaml Interface | `mli` | 1,124 | 61,749 | 111 | 6,178 | no |
| OCaml MLX | `mlx` | 3 | 0 | 0 | 0 | yes |
| OCamllex | `mll` | 26 | 1,886 | 6 | 1,300 | no |
| Odin | `odin` | 148 | 65,298 | 41 | 11,742 | no |
| Odoc | `mld` | 42 | 187 | 0 | 0 | yes |
| OML | `oml` | 0 | 0 | 0 | 0 | yes |
| OMNeT++ MSG | `msg` | 13 | 1,157 | 173 | 26,397 | no |
| OMNeT++ NED | `ned` | 0 | 0 | 0 | 0 | yes |
| OpenFGA | `fga` | 0 | 0 | 0 | 0 | yes |
| OpenSCAD | `scad` | 77 | 87,488 | 389 | 39,948 | no |
| OpenTofu | `tf`, `tofu` | 1,817 | 104,921 | 9 | 637 | no |
| OpenTofu Vars | `tfvars` | 20 | 578 | 0 | 0 | yes |
| OpenType Feature | `fea` | 0 | 0 | 0 | 0 | yes |
| Org | `org` | 25 | 13,134 | 59 | 11,525 | no |
| P4 Language | `p4` | 153 | 51,114 | 71 | 9,810 | no |
| Pact | `pact`, `repl` | 214 | 27,900 | 58 | 12,955 | no |
| Papyrus | `psc` | 110 | 7,967 | 25 | 16,899 | no |
| Pascal | `dpr`, `inc`, `lpr`, `p`, `pas`, `pp` | 434 | 105,865 | 414 | 33,239 | no |
| Path of Exile Filter | `filter` | 1 | 1 | 1 | 285 | yes |
| PDLL | `pdll` | 0 | 0 | 0 | 0 | yes |
| Pdxinfo | `pdxinfo` | 0 | 0 | 0 | 0 | yes |
| Perl | `pl`, `pm`, `t` | 3,119 | 451,273 | 140 | 30,112 | no |
| Perm | `perm` | 0 | 0 | 0 | 0 | yes |
| Pest | `pest` | 3 | 304 | 1 | 215 | yes |
| PHP | `php`, `phpt`, `phtml` | 6,058 | 933,334 | 2,841 | 310,714 | no |
| php_only | — | 0 | 0 | 0 | 0 | no filename registration |
| PHPDoc | — | 0 | 0 | 0 | 0 | no filename registration |
| pica200 | `pica` | 0 | 0 | 0 | 0 | yes |
| Pine Script | `pine`, `ps` | 1 | 41 | 0 | 0 | yes |
| PIO Assembly | `pio` | 27 | 1,766 | 0 | 0 | yes |
| Pkl | `pcf`, `pkl` | 3 | 123 | 0 | 0 | yes |
| Plain Text | `txt` | 11,953 | 4,224,492 | 4,308 | 746,804 | no |
| PlantUML | `iuml`, `plantuml`, `pu`, `puml`, `wsd` | 6 | 450 | 3 | 203 | yes |
| PlatformIO | `platformio.ini` | 37 | 1,014 | 34 | 1,197 | no |
| PO | `po`, `pot` | 301 | 1,951,174 | 511 | 918,280 | no |
| POD | `pod` | 3 | 5,772 | 0 | 0 | yes |
| Polar | `polar` | 0 | 0 | 0 | 0 | yes |
| Pony | `pony` | 1,040 | 155,304 | 299 | 70,876 | no |
| Poryscript | `pory` | 0 | 0 | 0 | 0 | yes |
| PowerShell | `ps1`, `psm1` | 251 | 14,886 | 93 | 6,642 | no |
| Praia | `praia` | 0 | 0 | 0 | 0 | yes |
| Prisma | `prisma` | 1 | 18 | 10 | 252 | yes |
| Processing | `pde` | 10 | 466 | 25 | 3,625 | no |
| Prolog | `P`, `pl`, `pro` | 140 | 23,878 | 36 | 5,852 | no |
| Properties | `properties` | 459 | 118,853 | 208 | 1,745 | no |
| Proto | `proto` | 354 | 55,767 | 47 | 10,576 | no |
| Pug | `jade`, `pug` | 13 | 807 | 14 | 122 | yes |
| Puppet | `epp`, `pp` | 2 | 34 | 1 | 45 | yes |
| PureScript | `purs` | 67 | 6,300 | 215 | 21,372 | no |
| Python | `mpy`, `py`, `pyi` | 9,031 | 2,808,888 | 4,018 | 981,977 | no |
| Python constraints | `constraints.txt` | 2 | 194 | 0 | 0 | yes |
| Python requirements | `requirements.txt` | 49 | 538 | 18 | 315 | yes |
| Qlik | `qvs` | 0 | 0 | 0 | 0 | yes |
| QML | `qml` | 229 | 29,866 | 26 | 3,723 | no |
| Quadlet | `artifact`, `build`, `container`, `image`, `kube`, `network`, `pod`, `volume` | 60 | 10,220 | 36 | 2,448 | no |
| QuakeC | `qc` | 704 | 188,902 | 198 | 83,251 | no |
| Quarkdown | `qd` | 0 | 0 | 0 | 0 | yes |
| Quarkdown-Inline | — | 0 | 0 | 0 | 0 | no filename registration |
| Quarto | `qmd` | 0 | 0 | 0 | 0 | yes |
| Quint | `qnt` | 60 | 10,996 | 0 | 0 | no |
| R | `R`, `r` | 384 | 108,634 | 138 | 61,872 | no |
| Racket | `rkt` | 1,876 | 128,924 | 43 | 6,293 | no |
| Rainbow CSV (,) | `csv` | 93 | 70,328 | 116 | 35,881 | no |
| Rainbow CSV (;) | — | 0 | 0 | 0 | 0 | no filename registration |
| Rainbow CSV (&#124;) | — | 0 | 0 | 0 | 0 | no filename registration |
| Rainbow TSV (⭲) | `tsv` | 6 | 173 | 1 | 173 | yes |
| RASI | `rasi`, `rasinc` | 0 | 0 | 0 | 0 | yes |
| RBS | `rbs` | 0 | 0 | 0 | 0 | yes |
| RCL | `rcl` | 0 | 0 | 0 | 0 | yes |
| Reason | `re` | 205 | 74,472 | 246 | 52,598 | no |
| Reason Interface | `rei` | 92 | 5,723 | 129 | 4,567 | no |
| Red | `red`, `reds` | 909 | 338,683 | 7,518 | 141,767 | no |
| REDscript | `reds` | 706 | 263,352 | 7,461 | 132,796 | no |
| Regedit | `reg` | 0 | 0 | 0 | 0 | yes |
| Regex | — | 0 | 0 | 0 | 0 | no filename registration |
| rego | `rego`, `rq` | 3 | 99 | 0 | 0 | yes |
| ReScript | `res`, `resi` | 52 | 13,456 | 6 | 1,213 | no |
| reST | `rst` | 3,574 | 660,419 | 1,412 | 164,648 | no |
| Rhai | `rhai` | 0 | 0 | 0 | 0 | yes |
| Risor | `risor` | 0 | 0 | 0 | 0 | yes |
| Robot | `robot` | 1 | 143 | 0 | 0 | yes |
| robots.txt | `robots.txt` | 33 | 231 | 21 | 184 | yes |
| Roc | `roc` | 75 | 15,415 | 19 | 5,525 | no |
| RON | `ron` | 6 | 135 | 0 | 0 | yes |
| Roto | `roto` | 0 | 0 | 0 | 0 | yes |
| RPM Spec | `spec` | 42 | 7,041 | 8 | 735 | no |
| RsHtml | `rs.html` | 16 | 350 | 0 | 0 | yes |
| RSTML | — | 0 | 0 | 0 | 0 | no filename registration |
| Ruby | `Appfile`, `Appraisals`, `Berksfile`, `Berksfile.lock`, `Brewfile`, `Capfile`, `Cheffile`, `Dangerfile`, `Deliverfile`, `Fastfile`, `Gemfile`, `Guardfile`, `Gymfile`, `Hobofile`, `Matchfile`, `Podfile`, `Puppetfile`, `Rakefile`, `Rantfile`, `Scanfile`, `Snapfile`, `Steepfile`, `Thorfile`, `Vagrantfile`, `builder`, `cap`, `capfile`, `gemspec`, `irbrc`, `jbuilder`, `pryrc`, `rabl`, `rake`, `rb`, `rdoc`, `ru`, `rxml`, `simplecov`, `thor` | 5,945 | 738,284 | 4,138 | 508,312 | no |
| Rust | `rs` | 9,775 | 3,015,860 | 4,822 | 1,884,966 | no |
| Rux | `rux` | 0 | 0 | 0 | 0 | yes |
| SageMath | `sage` | 0 | 0 | 0 | 0 | yes |
| Salesforce Log | `log`, `sflog` | 1,225 | 99,706 | 18 | 4,354 | no |
| SASS | `sass` | 19 | 343 | 18 | 46 | yes |
| SassDoc | — | 0 | 0 | 0 | 0 | no filename registration |
| Scala | `mill`, `sbt`, `sc`, `scala` | 1,030 | 131,391 | 1,553 | 170,847 | no |
| Scheme | `scm`, `ss` | 2,079 | 127,290 | 23 | 4,641 | no |
| SCSS | `scss` | 2,039 | 200,286 | 862 | 97,330 | no |
| Shell Script | `.env`, `APKBUILD`, `PKGBUILD`, `bash`, `bash_aliases`, `bash_login`, `bash_logout`, `bash_profile`, `bashrc`, `bats`, `brushrc`, `ebuild`, `envrc`, `profile`, `sh`, `zlogin`, `zprofile`, `zsh`, `zsh_aliases`, `zsh_histfile`, `zsh_profile`, `zshenv`, `zshrc` | 2,168 | 180,734 | 1,132 | 57,873 | no |
| Sieve | `sieve`, `sieveinterface` | 0 | 0 | 0 | 0 | yes |
| SilverStripe | `ss` | 4 | 10,056 | 1 | 2,184 | yes |
| Simula | `SIM`, `SIm`, `SiM`, `Sim`, `sIM`, `sIm`, `siM`, `sim`, `simula` | 0 | 0 | 0 | 0 | yes |
| Skir | `skir` | 0 | 0 | 0 | 0 | yes |
| Skript | `sk` | 0 | 0 | 0 | 0 | yes |
| Slang | `slang` | 2 | 157 | 0 | 0 | yes |
| Slim | `html.slim`, `slim` | 10 | 77 | 1 | 59 | yes |
| Slint | `Cargo.lock`, `slint` | 134 | 125,935 | 16 | 93,178 | no |
| Smali | `smali` | 221 | 14,909 | 0 | 0 | no |
| Smithy | `smithy` | 7 | 340 | 0 | 0 | yes |
| snakemake | `Snakefile`, `smk`, `snakefile` | 2 | 87 | 0 | 0 | yes |
| Solidity | `sol` | 424 | 51,075 | 219 | 30,641 | no |
| Soma | `soma` | 0 | 0 | 0 | 0 | yes |
| SOQL | `soql` | 0 | 0 | 0 | 0 | yes |
| SOSL | `sosl` | 0 | 0 | 0 | 0 | yes |
| Souffle | `dl` | 0 | 0 | 0 | 0 | yes |
| Sourcepawn | `sp` | 94 | 25,115 | 22 | 37,736 | no |
| SpiceDB | `zed` | 0 | 0 | 0 | 0 | yes |
| Spicy | `evt`, `hlt`, `spicy` | 59 | 8,979 | 0 | 0 | no |
| spthy | `spthy` | 0 | 0 | 0 | 0 | yes |
| SQL | `sql` | 272 | 14,692 | 461 | 16,396 | no |
| Squirrel | `nut` | 71 | 52,309 | 146 | 67,535 | no |
| SSH Config | `config`, `ssh_config` | 231 | 9,942 | 96 | 2,574 | no |
| Stan | `stan` | 59 | 4,834 | 69 | 2,933 | no |
| Stan Functions | `stanfunctions` | 0 | 0 | 0 | 0 | yes |
| Standard ML | `fun`, `sig`, `sml` | 1,509 | 305,082 | 32 | 2,227 | no |
| Starlark | `.tilt`, `.tiltfile`, `BUCK`, `BUILD`, `BUILD.bazel`, `MODULE.bazel`, `PACKAGE`, `REPO.bazel`, `Tiltfile`, `WORKSPACE`, `WORKSPACE.bzlmod`, `bxl`, `bzl`, `star` | 429 | 45,885 | 99 | 14,722 | no |
| Statamic Antlers | `antlers.html` | 0 | 0 | 0 | 0 | yes |
| Strace | `strace` | 3 | 1,087 | 0 | 0 | yes |
| Strings | `strings` | 1,884 | 201,155 | 54 | 203 | no |
| Structured Text | `st`, `stx` | 53 | 5,367 | 944 | 93,718 | no |
| Structurizr DSL | `dsl` | 0 | 0 | 1 | 66 | yes |
| Styx | `styx` | 121 | 2,405 | 0 | 0 | no |
| Surreal Query Language | `surql` | 0 | 0 | 0 | 0 | yes |
| Svelte | `svelte` | 138 | 11,518 | 85 | 11,058 | no |
| Sway | `sw` | 2,052 | 168,474 | 92 | 16,825 | no |
| Swift | `swift`, `swiftinterface` | 4,506 | 573,604 | 1,906 | 270,536 | no |
| SysML v2 | `sysml` | 0 | 0 | 0 | 0 | yes |
| SystemRDL | `rdl` | 0 | 0 | 0 | 0 | yes |
| SystemVerilog | `sv`, `svh`, `v`, `vh` | 943 | 1,914,465 | 57 | 14,940 | no |
| TableGen | `td` | 2 | 1,439 | 0 | 0 | yes |
| Tact | `tact` | 1,016 | 35,376 | 19 | 2,144 | no |
| Taskfile | `Taskfile.yaml`, `Taskfile.yml`, `taskfile.yaml`, `taskfile.yml` | 1 | 349 | 0 | 0 | yes |
| TCL | `tcl`, `tm` | 457 | 175,570 | 1,267 | 585,323 | no |
| Templ | `templ` | 0 | 0 | 0 | 0 | yes |
| Tera | `tera` | 4 | 215 | 0 | 0 | yes |
| Tera (CSS) | `css.tera` | 0 | 0 | 0 | 0 | yes |
| Tera (HTML) | `html.tera` | 2 | 20 | 0 | 0 | yes |
| Tera (JSON) | `json.tera` | 0 | 0 | 0 | 0 | yes |
| Tera (TOML) | `toml.tera` | 0 | 0 | 0 | 0 | yes |
| Tera (XML) | `xml.tera` | 0 | 0 | 0 | 0 | yes |
| Tera (YAML) | `yaml.tera` | 0 | 0 | 0 | 0 | yes |
| Terraform | `tf`, `tofu` | 1,817 | 104,921 | 9 | 637 | no |
| Terraform Vars | `tfvars` | 20 | 578 | 0 | 0 | yes |
| Textproto | `pbtxt`, `textpb`, `textproto`, `txtpb` | 2 | 51 | 1 | 234 | yes |
| Thrift | `thrift` | 42 | 8,946 | 0 | 0 | no |
| TL-B | `tlb` | 0 | 0 | 0 | 0 | yes |
| TLA+ | `tla` | 3 | 162 | 0 | 0 | yes |
| TLA+ Cfg | `cfg` | 212 | 26,139 | 129 | 16,248 | no |
| tmux | `tmux`, `tmux.conf` | 0 | 0 | 0 | 0 | yes |
| Todo | `task`, `taskpaper`, `tasks`, `todo`, `todos` | 3 | 148 | 0 | 0 | yes |
| Todotxt | `todo.txt`, `txt` | 11,953 | 4,224,492 | 4,308 | 746,804 | no |
| Tolk | `tolk` | 101 | 24,660 | 0 | 0 | no |
| TOML | `Cargo.lock`, `Pipfile`, `toml`, `uv.lock` | 4,792 | 261,198 | 2,184 | 136,457 | no |
| Tonel Smalltalk | `st` | 53 | 5,367 | 944 | 93,718 | no |
| TOON | `toon` | 0 | 0 | 0 | 0 | yes |
| TQL | `tql` | 12 | 46 | 0 | 0 | yes |
| Tree-sitter Query | `scm` | 2,075 | 117,234 | 22 | 2,457 | no |
| TSRX | `tsrx` | 0 | 0 | 0 | 0 | yes |
| TSX | `tsx` | 2,064 | 227,317 | 3,167 | 218,564 | no |
| Turtle | `ttl`, `turtle` | 0 | 0 | 0 | 0 | yes |
| Twig | `html.twig`, `twig`, `twig.html` | 24 | 84 | 74 | 4,753 | no |
| Txtar | `txtar` | 0 | 0 | 0 | 0 | yes |
| TypeScript | `cts`, `mts`, `ts` | 170,951 | 19,986,414 | 137,774 | 17,803,284 | no |
| Typespec | `tsp`, `typespec` | 0 | 0 | 0 | 0 | yes |
| Typst | `typ`, `typst` | 314 | 48,230 | 0 | 0 | no |
| TyranoScript | `ks` | 0 | 0 | 0 | 0 | yes |
| ucode | `uc` | 17 | 5,077 | 27 | 5,980 | no |
| Uiua | `ua`, `uiua` | 0 | 0 | 0 | 0 | yes |
| Umka | `um` | 0 | 0 | 0 | 0 | yes |
| Umple | `ump` | 0 | 0 | 0 | 0 | yes |
| Ungrammar | `ungram` | 4 | 27 | 0 | 0 | yes |
| Unison | `u` | 6 | 18 | 0 | 0 | yes |
| URDF | `urdf` | 0 | 0 | 0 | 0 | yes |
| USD | `usd`, `usda` | 0 | 0 | 0 | 0 | yes |
| UTL | `utl` | 0 | 0 | 0 | 0 | yes |
| V | `mod`, `v`, `vsh`, `vv` | 1,202 | 1,926,765 | 47 | 13,217 | no |
| Vala | `vala`, `vapi` | 1,367 | 338,788 | 123 | 38,853 | no |
| vCard | `vcf` | 0 | 0 | 0 | 0 | yes |
| Vento | `vento`, `vto` | 0 | 0 | 0 | 0 | yes |
| Veryl | `veryl` | 0 | 0 | 0 | 0 | yes |
| VEX | `vex`, `vfl` | 0 | 0 | 0 | 0 | yes |
| VHDL | `vhd`, `vhdl` | 89 | 32,562 | 331 | 71,797 | no |
| VHS | `tape` | 1 | 99 | 0 | 0 | yes |
| Vibescript | `vibe` | 0 | 0 | 0 | 0 | yes |
| ViewTree ($mol) | `view.tree` | 0 | 0 | 0 | 0 | yes |
| VRL | `vrl` | 0 | 0 | 0 | 0 | yes |
| Vue.js | `vue` | 986 | 73,174 | 603 | 18,240 | no |
| WDL | `wdl` | 0 | 0 | 0 | 0 | yes |
| WebAssembly Text Format | `wat` | 8 | 183 | 2 | 103 | yes |
| WebIDL | `webidl` | 229 | 3,781 | 0 | 0 | no |
| WeiXin Markup Language | `wxml` | 0 | 0 | 0 | 0 | yes |
| WFG | `wfg` | 0 | 0 | 0 | 0 | yes |
| WFL | `wfl` | 0 | 0 | 0 | 0 | yes |
| WFS | `wfs` | 0 | 0 | 0 | 0 | yes |
| Wgsl | `wgsl` | 42 | 1,735 | 50 | 3,073 | no |
| WGSL/WESL | `wesl`, `wgsl` | 43 | 1,742 | 50 | 3,073 | no |
| Whim | `whim` | 0 | 0 | 0 | 0 | yes |
| whkd | `whkdrc` | 0 | 0 | 0 | 0 | yes |
| Wikitext | `mediawiki`, `wikimedia`, `wikitext` | 15 | 1,226 | 0 | 0 | yes |
| WIT | `wit` | 1 | 40 | 0 | 0 | yes |
| WoW TOC | `toc` | 0 | 0 | 1 | 36 | yes |
| WPL | `wpl` | 0 | 0 | 0 | 0 | yes |
| Wren | `wren` | 111 | 3,129 | 1 | 3,158 | no |
| Xcode Project | `pbxproj` | 188 | 96,960 | 34 | 32,611 | no |
| XDR Syntax Highlight | `xdr` | 0 | 0 | 0 | 0 | yes |
| xmake | `xmake.lua` | 0 | 0 | 2 | 96 | yes |
| XML | `xml` | 2,479 | 290,990 | 3,764 | 565,728 | no |
| XQuery | `xq`, `xql`, `xqm`, `xquery`, `xqy` | 0 | 0 | 0 | 0 | yes |
| YAML | `bst`, `clang-format`, `clangd`, `pixi.lock`, `yaml`, `yml` | 11,267 | 1,101,747 | 8,142 | 1,483,123 | no |
| YAML+ERB | `yaml.erb`, `yml.erb` | 0 | 0 | 4 | 968 | yes |
| YANG | `yang` | 0 | 0 | 0 | 0 | yes |
| Yara | `yar`, `yara` | 1 | 28 | 0 | 0 | yes |
| Yarn Spinner | `yarn` | 5 | 57 | 0 | 0 | yes |
| Yuck | `yuck` | 0 | 0 | 0 | 0 | yes |
| Yul | `yul` | 0 | 0 | 0 | 0 | yes |
| Yulang | `yu` | 0 | 0 | 0 | 0 | yes |
| Zed Keybind Context | — | 0 | 0 | 0 | 0 | no filename registration |
| Zeek | `zeek` | 2,593 | 148,354 | 11 | 4,546 | no |
| Zig | `zig`, `zon` | 3,285 | 813,064 | 473 | 178,418 | no |
| ziggy | `zgy`, `ziggy` | 1 | 8 | 0 | 0 | yes |
| ziggy-schema | `zgy-schema`, `ziggy-schema` | 2 | 230 | 0 | 0 | yes |
| ZoKrates | `zok` | 0 | 0 | 0 | 0 | yes |
| zwirn | `zwirn` | 0 | 0 | 0 | 0 | yes |

## Unavailable extension inventories

- `bearded`: HTTP Error 404: Not Found
- `irix-terminal-theme`: fatal: could not read Username for 'https://codeberg.org': No such device or address
- `nanowise`: HTTP Error 404: Not Found
- `spai-zero-theme`: HTTP Error 404: Not Found
- `vanta-theme`: fatal: mismatched algorithms: client sha1; server sha256
- `zedburn`: HTTP Error 404: Not Found
