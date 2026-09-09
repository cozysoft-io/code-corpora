# Corpus language coverage

Source snapshot: 2026-09-08. Regenerate with `python3 corpus_coverage.py`.

Files match registered Zed `path_suffixes`, including exact filenames and compound suffixes, plus aliases `.arturo` (Arturo), `.uiua` (Uiua), and `.simula` (Simula). Matching is case-sensitive. Only strictly valid UTF-8 files count. Lines include blanks and comments; a final unterminated line counts once. Empty files count as files with zero lines.

The scan includes hidden and ignored files, skips `.git` and symlinks, and scans `training/` (the `train/` alias) once. First-line patterns and user overrides are not applied. A file matching several registrations counts toward each language, once per language. Split totals count each file only once. Shared suffixes indicate possible coverage, not a verified language classification.

| Split | UTF-8 files | Raw lines | Rejected non-UTF-8 files | Unmatched files |
| --- | ---: | ---: | ---: | ---: |
| training | 1,072,632 | 246,584,529 | 975 | 320,491 |
| test | 681,830 | 115,611,466 | 631 | 144,952 |

596 registrations; 582 language names; 1022 unique suffixes/filenames; 298 languages below 21 files or 2,000 raw lines combined. 6 extension inventories unavailable.

Full registrations, pins, per-suffix counts, ambiguities, and failures are in [language-coverage.json](language-coverage.json).

## Below coverage threshold

| Language | Suffixes / filenames | Training files | Training lines | Test files | Test lines |
| --- | --- | ---: | ---: | ---: | ---: |
| Aleo | `aleo` | 0 | 0 | 0 | 0 |
| Alex | `x` | 10 | 919 | 2 | 70 |
| Amber | `ab` | 1 | 10 | 0 | 0 |
| Angular | `component.html`, `ng.html` | 11 | 1,197 | 3 | 78 |
| Animation.txt | `animation.txt` | 0 | 0 | 0 | 0 |
| Ansible | `ansible` | 0 | 0 | 0 | 0 |
| Answer Set Programming | `asp`, `lp` | 1 | 103 | 1 | 1 |
| Apache Avro (IDL) | `avdl` | 0 | 0 | 0 | 0 |
| ASN.1 | `mib` | 0 | 0 | 0 | 0 |
| ASP Classic | `asa`, `asp` | 1 | 103 | 1 | 1 |
| ass | `ass`, `ssa` | 0 | 0 | 0 | 0 |
| Awsum | `aww` | 0 | 0 | 0 | 0 |
| Ayla | `ayl`, `ayla` | 0 | 0 | 0 | 0 |
| Baml | `baml` | 0 | 0 | 0 | 0 |
| bazelrc | `bazelrc` | 7 | 472 | 3 | 27 |
| Beancount | `bean`, `beancount` | 0 | 0 | 0 | 0 |
| Beast | `btsx` | 0 | 0 | 0 | 0 |
| Bend | `bend` | 0 | 0 | 0 | 0 |
| Bicep | `bicep` | 1 | 4 | 0 | 0 |
| Bicep Parameters | `bicepparam` | 0 | 0 | 0 | 0 |
| Blueprint | `blp` | 1 | 11 | 0 | 0 |
| Bruno | `bru` | 0 | 0 | 0 | 0 |
| Build2 manifest | `manifest` | 35 | 717 | 7 | 153 |
| C# Solution File | `slnx` | 12 | 369 | 31 | 369 |
| Caddyfile | `Caddyfile`, `caddyfile` | 5 | 347 | 0 | 0 |
| Candid | `did` | 0 | 0 | 0 | 0 |
| CAP CDS | `cds` | 0 | 0 | 0 | 0 |
| Cap'n Proto | `capnp` | 15 | 2,418 | 1 | 952 |
| Cartan | `cart` | 0 | 0 | 0 | 0 |
| Carve | `crv` | 0 | 0 | 0 | 0 |
| Cedar | `cedar` | 0 | 0 | 0 | 0 |
| CFEngine | `cf`, `cf.sub`, `cf3`, `cfengine`, `cfengine3` | 12 | 283 | 0 | 0 |
| CFML (Script) | `cfs` | 0 | 0 | 0 | 0 |
| Cherri | `cherri` | 0 | 0 | 0 | 0 |
| Civet | `civet` | 0 | 0 | 0 | 0 |
| CODEOWNERS | `CODEOWNERS`, `CODEOWNERS.txt` | 35 | 392 | 38 | 149 |
| Coi | `coi`, `d.coi` | 0 | 0 | 0 | 0 |
| CONL | `conl` | 0 | 0 | 0 | 0 |
| Cooklang | `cook` | 0 | 0 | 0 | 0 |
| Corn | `corn` | 0 | 0 | 0 | 0 |
| Cpp2 | `cpp2`, `h2` | 0 | 0 | 0 | 0 |
| CQL | `cql` | 6 | 356 | 0 | 0 |
| CSS + HubL | `hubl.css` | 0 | 0 | 0 | 0 |
| CUE | `cue` | 3 | 14 | 0 | 0 |
| Cylc | `cylc` | 5 | 835 | 0 | 0 |
| Cypher | `cql`, `cyp`, `cypher` | 6 | 356 | 0 | 0 |
| D2 | `d2` | 1 | 116 | 0 | 0 |
| Dang | `dang` | 0 | 0 | 0 | 0 |
| DataZinc | `dzn` | 0 | 0 | 0 | 0 |
| DBML | `dbml` | 1 | 19 | 0 | 0 |
| Demo Tape | `tape` | 1 | 99 | 0 | 0 |
| Desktop Entry | `desktop`, `directory` | 20 | 375 | 5 | 86 |
| devicetree | `dts`, `dtsi`, `dtso`, `its` | 0 | 0 | 1 | 8 |
| Dhall | `dhall` | 20 | 167 | 4 | 10 |
| Django | `dj.html`, `dj.md`, `dj.txt` | 0 | 0 | 0 | 0 |
| Djot | `dj`, `djot` | 9 | 1,953 | 1 | 149 |
| DOT | `DOT`, `dot`, `gv` | 9 | 161 | 10 | 619 |
| Duper | `duper` | 0 | 0 | 0 | 0 |
| Duso | `du` | 0 | 0 | 0 | 0 |
| Ebuild | `ebuild` | 0 | 0 | 0 | 0 |
| ECR | `ecr` | 6 | 31 | 4 | 21 |
| Edge | `edge` | 1 | 7 | 0 | 0 |
| EDI X12 | `x12` | 1 | 1,489 | 0 | 0 |
| Elle | `le` | 0 | 0 | 0 | 0 |
| Elsa | `lc` | 0 | 0 | 0 | 0 |
| Exograph | `exo` | 0 | 0 | 0 | 0 |
| Ferret | `fer` | 0 | 0 | 0 | 0 |
| Ferret Lockfile | `ferret.lock` | 0 | 0 | 0 | 0 |
| Ferret Manifest | `fer.ret` | 0 | 0 | 0 | 0 |
| Firebase Rules | `firebase.rules`, `rules`, `storage.rules` | 9 | 395 | 11 | 196 |
| FlatBuffers | `fbs` | 6 | 364 | 0 | 0 |
| FlatZinc | `fzn` | 0 | 0 | 0 | 0 |
| Fluent | `ftl` | 14 | 43 | 8 | 64 |
| Fountain | `fountain`, `spmd` | 0 | 0 | 0 | 0 |
| Freemarker | `ftl` | 14 | 43 | 8 | 64 |
| FreeStyleWiki | `fsw`, `fswiki` | 0 | 0 | 0 | 0 |
| FSH | `fsh` | 0 | 0 | 0 | 0 |
| FSM | `fsm` | 0 | 0 | 0 | 0 |
| GABC | `gabc` | 0 | 0 | 0 | 0 |
| Genexpr | `genexpr` | 0 | 0 | 0 | 0 |
| Geno | `geno` | 0 | 0 | 0 | 0 |
| Ghostty | `com.mitchellh.ghostty/config`, `config/ghostty/config`, `ghostty`, `ghostty/config` | 0 | 0 | 0 | 0 |
| Git Commit | `COMMIT_EDITMSG`, `EDIT_DESCRIPTION`, `MERGE_MSG`, `NOTES_EDITMSG`, `TAG_EDITMSG` | 2 | 2 | 1 | 1 |
| Git Config | `.gitconfig`, `.gitmodules`, `.lfsconfig`, `config.worktree` | 67 | 559 | 26 | 204 |
| Git Rebase | `git-rebase-todo` | 3 | 180 | 0 | 0 |
| Glimmer (JavaScript) | `gjs` | 5 | 429 | 32 | 557 |
| Glimmer (TypeScript) | `gts` | 5 | 531 | 22 | 373 |
| GN | `.gn`, `BUILD.gn`, `gn`, `gni` | 1 | 10 | 0 | 0 |
| Go HTML Template | `gohtml`, `html.gotmpl`, `html.gotpl` | 0 | 0 | 0 | 0 |
| Go Text Template | `go.tpl`, `go.txt`, `gotmpl`, `gtpl`, `txt.gotmpl`, `txt.gotpl` | 8 | 12,812 | 0 | 0 |
| Go Work | `work` | 0 | 0 | 0 | 0 |
| Grafana Alloy | `alloy` | 0 | 0 | 0 | 0 |
| GreyCat | `gcl` | 0 | 0 | 0 | 0 |
| GritQL | `grit` | 0 | 0 | 0 | 0 |
| GritQL Snippet | `gritqlsnippet` | 0 | 0 | 0 | 0 |
| GROQ | `groq` | 0 | 0 | 0 | 0 |
| GXL | `gxl` | 0 | 0 | 0 | 0 |
| Haml | `haml`, `html.haml` | 25 | 140 | 0 | 0 |
| Helm | `.helmignore` | 7 | 96 | 48 | 415 |
| Hera | `hera` | 0 | 0 | 0 | 0 |
| hl7_v2 | `hl7` | 1 | 1,584 | 0 | 0 |
| hledger | `hledger`, `journal`, `ledger` | 33 | 1,577 | 0 | 0 |
| hledger-rules | `rules` | 9 | 395 | 11 | 196 |
| Hosts | `hosts` | 1 | 3 | 2 | 4 |
| HP-42S | `42s`, `hp42s` | 0 | 0 | 0 | 0 |
| HTML + HubL | `hubl.html` | 0 | 0 | 0 | 0 |
| http | `http` | 3 | 219 | 0 | 0 |
| HubL | `hubl` | 0 | 0 | 0 | 0 |
| Huff | `huff` | 0 | 0 | 0 | 0 |
| HuJSON | `hujson`, `jwcc` | 0 | 0 | 0 | 0 |
| Hurl | `hurl` | 20 | 203 | 0 | 0 |
| HXML | `hxml` | 6 | 20 | 8 | 81 |
| Hyprland Config | `hyprland.conf`, `hyprland.hl`, `hyprlandd.conf`, `hyprlandd.hl` | 0 | 0 | 0 | 0 |
| iCal | `ics` | 0 | 0 | 0 | 0 |
| IFC | `ifc` | 0 | 0 | 0 | 0 |
| Immigrant | `schema` | 0 | 0 | 0 | 0 |
| Ink | `ink` | 4 | 2,214 | 0 | 0 |
| Inko | `inko` | 1 | 3 | 0 | 0 |
| ion | `ion` | 1 | 20 | 0 | 0 |
| ion_schema | `isl` | 2 | 764 | 0 | 0 |
| ISLE | `isle` | 0 | 0 | 2 | 3,203 |
| Jdl | `jdl` | 0 | 0 | 0 | 0 |
| Jerry | `jer` | 0 | 0 | 0 | 0 |
| JS+ERB | `js.erb` | 3 | 42 | 12 | 112 |
| JSON Lines | `jsonl`, `ndjson` | 2 | 7 | 15 | 678 |
| Jsonnet | `jsonnet`, `libsonnet` | 3 | 139 | 0 | 0 |
| JSP | `jsp`, `jspf`, `tag` | 0 | 0 | 7 | 7 |
| Just | `JUSTFILE`, `Justfile`, `just`, `justfile` | 29 | 1,361 | 11 | 262 |
| KCL | `k` | 308 | 1,934 | 0 | 0 |
| Kconfig | `Kconfig` | 0 | 0 | 1 | 258 |
| Kdl | `kdl` | 20 | 729 | 0 | 0 |
| Koto | `koto` | 1 | 4 | 0 | 0 |
| kulala-http | `http` | 3 | 219 | 0 | 0 |
| Latte | `latte` | 0 | 0 | 0 | 0 |
| Ledger | `journal`, `ldg`, `ldgr`, `ledger` | 33 | 1,577 | 0 | 0 |
| Leo | `leo` | 0 | 0 | 0 | 0 |
| LikeC4 | `c4`, `likec4` | 0 | 0 | 0 | 0 |
| LilyPond | `ily`, `ly` | 0 | 0 | 0 | 0 |
| Lini | `lini` | 0 | 0 | 0 | 0 |
| Liquid | `liquid` | 3 | 9 | 0 | 0 |
| Lisette | `lis` | 0 | 0 | 0 | 0 |
| Literate Haskell | `lhs` | 3 | 69 | 0 | 0 |
| Lox | `lox` | 0 | 0 | 0 | 0 |
| Mach | `mach` | 0 | 0 | 0 | 0 |
| Mako | `mako` | 0 | 0 | 0 | 0 |
| Marko | `marko` | 0 | 0 | 0 | 0 |
| mcfunction | `mcfunction` | 0 | 0 | 0 | 0 |
| MetaScript | `cms`, `ems`, `jms`, `ms`, `rms`, `wms` | 5 | 1,636 | 1 | 123 |
| microScript | `ms` | 5 | 1,636 | 1 | 123 |
| Minecraft Function | `mcfunction` | 0 | 0 | 0 | 0 |
| Minecraft Lang | `lang` | 99 | 1,469 | 0 | 0 |
| MiniZinc | `mzn` | 0 | 0 | 0 | 0 |
| MJML | `mjml` | 9 | 114 | 0 | 0 |
| MLIR | `mlir` | 0 | 0 | 0 | 0 |
| Modelfile | `Modelfile` | 0 | 0 | 0 | 0 |
| MoJu | `mju` | 0 | 0 | 0 | 0 |
| Nautilus | `nautilus` | 0 | 0 | 0 | 0 |
| Navi | `navi`, `nv` | 0 | 0 | 0 | 0 |
| Navi Stream | `nvs` | 0 | 0 | 0 | 0 |
| Nginx | `nginx.conf` | 7 | 565 | 0 | 0 |
| Nickel | `ncl` | 2 | 8 | 0 | 0 |
| Nim Format String | `nim_format_string` | 0 | 0 | 0 | 0 |
| niva | `niva` | 0 | 0 | 0 | 0 |
| Nomad Job | `nomad`, `nomad.hcl` | 0 | 0 | 0 | 0 |
| NSIS | `nsh`, `nsi` | 4 | 624 | 0 | 0 |
| Numscript | `num`, `numscript` | 10 | 229 | 0 | 0 |
| Nunjucks | `njk` | 4 | 28 | 0 | 0 |
| Oat | `oat` | 0 | 0 | 0 | 0 |
| OCaml MLX | `mlx` | 3 | 0 | 0 | 0 |
| Odoc | `mld` | 42 | 187 | 0 | 0 |
| OML | `oml` | 0 | 0 | 0 | 0 |
| OMNeT++ NED | `ned` | 0 | 0 | 0 | 0 |
| OpenFGA | `fga` | 0 | 0 | 0 | 0 |
| OpenTofu Vars | `tfvars` | 20 | 578 | 0 | 0 |
| OpenType Feature | `fea` | 0 | 0 | 0 | 0 |
| Path of Exile Filter | `filter` | 1 | 1 | 1 | 285 |
| PDLL | `pdll` | 0 | 0 | 0 | 0 |
| Pdxinfo | `pdxinfo` | 0 | 0 | 0 | 0 |
| Perm | `perm` | 0 | 0 | 0 | 0 |
| Pest | `pest` | 3 | 304 | 1 | 215 |
| pica200 | `pica` | 0 | 0 | 0 | 0 |
| Pine Script | `pine`, `ps` | 133 | 1,946 | 0 | 0 |
| PIO Assembly | `pio` | 27 | 1,766 | 0 | 0 |
| Pkl | `pcf`, `pkl` | 3 | 123 | 0 | 0 |
| PlantUML | `iuml`, `plantuml`, `pu`, `puml`, `wsd` | 6 | 450 | 3 | 203 |
| POD | `pod` | 3 | 5,772 | 0 | 0 |
| Polar | `polar` | 0 | 0 | 0 | 0 |
| Poryscript | `pory` | 0 | 0 | 0 | 0 |
| Praia | `praia` | 0 | 0 | 0 | 0 |
| Prisma | `prisma` | 1 | 18 | 10 | 252 |
| Pug | `jade`, `pug` | 13 | 807 | 14 | 122 |
| Puppet | `epp`, `pp` | 2 | 34 | 1 | 45 |
| Python constraints | `constraints.txt` | 2 | 194 | 0 | 0 |
| Python requirements | `requirements.txt` | 49 | 538 | 18 | 315 |
| Qlik | `qvs` | 0 | 0 | 0 | 0 |
| Quarkdown | `qd` | 0 | 0 | 0 | 0 |
| Quarto | `qmd` | 0 | 0 | 0 | 0 |
| Rainbow TSV (⭲) | `tsv` | 6 | 173 | 1 | 173 |
| RASI | `rasi`, `rasinc` | 0 | 0 | 0 | 0 |
| RBS | `rbs` | 0 | 0 | 0 | 0 |
| RCL | `rcl` | 0 | 0 | 0 | 0 |
| Regedit | `reg` | 0 | 0 | 0 | 0 |
| rego | `rego`, `rq` | 3 | 99 | 0 | 0 |
| Rhai | `rhai` | 0 | 0 | 0 | 0 |
| Risor | `risor` | 0 | 0 | 0 | 0 |
| Robot | `robot` | 1 | 143 | 0 | 0 |
| robots.txt | `robots.txt` | 33 | 231 | 21 | 184 |
| RON | `ron` | 6 | 135 | 0 | 0 |
| Roto | `roto` | 0 | 0 | 0 | 0 |
| RsHtml | `rs.html` | 16 | 350 | 0 | 0 |
| Rux | `rux` | 0 | 0 | 0 | 0 |
| SageMath | `sage` | 6 | 107 | 0 | 0 |
| SASS | `sass` | 24 | 424 | 18 | 46 |
| Sieve | `sieve`, `sieveinterface` | 0 | 0 | 0 | 0 |
| SilverStripe | `ss` | 4 | 10,056 | 1 | 2,184 |
| Skir | `skir` | 0 | 0 | 0 | 0 |
| Skript | `sk` | 0 | 0 | 0 | 0 |
| Slang | `slang` | 54 | 791 | 0 | 0 |
| Slim | `html.slim`, `slim` | 10 | 77 | 1 | 59 |
| Smithy | `smithy` | 7 | 340 | 0 | 0 |
| snakemake | `Snakefile`, `smk`, `snakefile` | 2 | 87 | 0 | 0 |
| Soma | `soma` | 0 | 0 | 0 | 0 |
| SOQL | `soql` | 0 | 0 | 0 | 0 |
| SOSL | `sosl` | 0 | 0 | 0 | 0 |
| Souffle | `dl` | 0 | 0 | 0 | 0 |
| SpiceDB | `zed` | 4 | 1,415 | 0 | 0 |
| spthy | `spthy` | 0 | 0 | 0 | 0 |
| Stan Functions | `stanfunctions` | 0 | 0 | 0 | 0 |
| Statamic Antlers | `antlers.html` | 0 | 0 | 0 | 0 |
| Strace | `strace` | 3 | 1,087 | 0 | 0 |
| Structurizr DSL | `dsl` | 0 | 0 | 1 | 66 |
| Surreal Query Language | `surql` | 0 | 0 | 0 | 0 |
| SysML v2 | `sysml` | 0 | 0 | 0 | 0 |
| SystemRDL | `rdl` | 0 | 0 | 0 | 0 |
| TableGen | `td` | 2 | 1,439 | 0 | 0 |
| Taskfile | `Taskfile.yaml`, `Taskfile.yml`, `taskfile.yaml`, `taskfile.yml` | 1 | 349 | 0 | 0 |
| Templ | `templ` | 0 | 0 | 0 | 0 |
| Tera | `tera` | 4 | 215 | 0 | 0 |
| Tera (CSS) | `css.tera` | 0 | 0 | 0 | 0 |
| Tera (HTML) | `html.tera` | 2 | 20 | 0 | 0 |
| Tera (JSON) | `json.tera` | 0 | 0 | 0 | 0 |
| Tera (TOML) | `toml.tera` | 0 | 0 | 0 | 0 |
| Tera (XML) | `xml.tera` | 0 | 0 | 0 | 0 |
| Tera (YAML) | `yaml.tera` | 0 | 0 | 0 | 0 |
| Terraform Vars | `tfvars` | 20 | 578 | 0 | 0 |
| Textproto | `pbtxt`, `textpb`, `textproto`, `txtpb` | 2 | 51 | 1 | 234 |
| TL-B | `tlb` | 0 | 0 | 0 | 0 |
| TLA+ | `tla` | 3 | 162 | 0 | 0 |
| tmux | `tmux`, `tmux.conf` | 0 | 0 | 0 | 0 |
| Todo | `task`, `taskpaper`, `tasks`, `todo`, `todos` | 3 | 148 | 0 | 0 |
| TOON | `toon` | 0 | 0 | 0 | 0 |
| TQL | `tql` | 12 | 46 | 0 | 0 |
| TSRX | `tsrx` | 0 | 0 | 0 | 0 |
| Turtle | `ttl`, `turtle` | 0 | 0 | 0 | 0 |
| Txtar | `txtar` | 0 | 0 | 0 | 0 |
| Typespec | `tsp`, `typespec` | 0 | 0 | 0 | 0 |
| TyranoScript | `ks` | 0 | 0 | 0 | 0 |
| Umka | `um` | 0 | 0 | 0 | 0 |
| Umple | `ump` | 0 | 0 | 0 | 0 |
| Ungrammar | `ungram` | 4 | 27 | 0 | 0 |
| Unison | `u` | 11 | 62 | 0 | 0 |
| URDF | `urdf` | 0 | 0 | 0 | 0 |
| USD | `usd`, `usda` | 0 | 0 | 0 | 0 |
| UTL | `utl` | 0 | 0 | 0 | 0 |
| vCard | `vcf` | 0 | 0 | 0 | 0 |
| Vento | `vento`, `vto` | 0 | 0 | 0 | 0 |
| Veryl | `veryl` | 0 | 0 | 0 | 0 |
| VEX | `vex`, `vfl` | 0 | 0 | 0 | 0 |
| VHS | `tape` | 1 | 99 | 0 | 0 |
| Vibescript | `vibe` | 0 | 0 | 0 | 0 |
| ViewTree ($mol) | `view.tree` | 0 | 0 | 0 | 0 |
| VRL | `vrl` | 0 | 0 | 0 | 0 |
| WDL | `wdl` | 0 | 0 | 0 | 0 |
| WebAssembly Text Format | `wat` | 8 | 183 | 2 | 103 |
| WeiXin Markup Language | `wxml` | 0 | 0 | 0 | 0 |
| WFG | `wfg` | 0 | 0 | 0 | 0 |
| WFL | `wfl` | 0 | 0 | 0 | 0 |
| WFS | `wfs` | 0 | 0 | 0 | 0 |
| Whim | `whim` | 0 | 0 | 0 | 0 |
| whkd | `whkdrc` | 0 | 0 | 0 | 0 |
| Wikitext | `mediawiki`, `wikimedia`, `wikitext` | 15 | 1,226 | 0 | 0 |
| WIT | `wit` | 1 | 40 | 0 | 0 |
| WoW TOC | `toc` | 0 | 0 | 1 | 36 |
| WPL | `wpl` | 0 | 0 | 0 | 0 |
| XDR Syntax Highlight | `xdr` | 0 | 0 | 0 | 0 |
| xmake | `xmake.lua` | 0 | 0 | 2 | 96 |
| XQuery | `xq`, `xql`, `xqm`, `xquery`, `xqy` | 25 | 360 | 0 | 0 |
| YAML+ERB | `yaml.erb`, `yml.erb` | 0 | 0 | 4 | 968 |
| YANG | `yang` | 0 | 0 | 0 | 0 |
| Yara | `yar`, `yara` | 1 | 28 | 0 | 0 |
| Yarn Spinner | `yarn` | 5 | 57 | 0 | 0 |
| Yuck | `yuck` | 0 | 0 | 0 | 0 |
| Yul | `yul` | 0 | 0 | 0 | 0 |
| Yulang | `yu` | 0 | 0 | 0 | 0 |
| ziggy | `zgy`, `ziggy` | 1 | 8 | 0 | 0 |
| ziggy-schema | `zgy-schema`, `ziggy-schema` | 2 | 230 | 0 | 0 |
| ZoKrates | `zok` | 0 | 0 | 0 | 0 |
| zwirn | `zwirn` | 0 | 0 | 0 | 0 |

## Meets coverage threshold

| Language | Suffixes / filenames | Training files | Training lines | Test files | Test lines |
| --- | --- | ---: | ---: | ---: | ---: |
| ActionScript | `as` | 326 | 46,347 | 478 | 92,563 |
| Ada | `adb`, `ads` | 2,130 | 177,385 | 479 | 67,254 |
| Agda | `agda` | 1,291 | 149,854 | 1,205 | 203,603 |
| Aiken | `ak` | 56 | 15,962 | 34 | 7,326 |
| AL | `al`, `dal` | 36 | 15,943 | 111 | 17,515 |
| Apex | `apex`, `apex-anon`, `cls`, `trigger` | 480 | 68,307 | 278 | 60,911 |
| AppleScript | `applescript`, `scpt` | 1,129 | 73,991 | 30 | 2,252 |
| Arduino | `ino` | 690 | 110,620 | 869 | 355,455 |
| ArkTS Language | `ets` | 175 | 22,716 | 63 | 15,374 |
| Arturo | `art`, `arturo` | 829 | 13,554 | 0 | 0 |
| AsciiDoc | `ad`, `adoc`, `asc`, `asciidoc` | 582 | 71,108 | 8 | 2,365 |
| Assembly | `S`, `asm`, `s` | 523 | 111,414 | 199 | 25,127 |
| Astro | `astro` | 256 | 5,799 | 0 | 0 |
| AutoHotkey | `ahk` | 1,044 | 39,749 | 27 | 8,354 |
| AWK | `awk` | 919 | 34,450 | 3 | 740 |
| Batch | `bat`, `cmd` | 541 | 20,553 | 104 | 5,252 |
| BibTeX | `bib`, `biblatex`, `bibtex` | 19 | 10,858 | 12 | 3,214 |
| Bison | `y`, `yy` | 20 | 16,633 | 11 | 4,198 |
| bitbake | `bb`, `bbappend`, `bbclass`, `conf`, `inc` | 780 | 116,053 | 495 | 36,824 |
| Blade | `blade.php` | 198 | 2,425 | 1 | 196 |
| Bluespec SystemVerilog | `bsv` | 210 | 75,584 | 421 | 75,930 |
| BQN | `bqn` | 513 | 9,582 | 8 | 2,461 |
| Brainfuck | `bf` | 226 | 2,197 | 0 | 0 |
| Bsl | `bsl` | 333 | 233,089 | 6 | 9,578 |
| Build2 | `build`, `buildfile` | 56 | 4,438 | 34 | 1,654 |
| C | `c` | 7,832 | 51,047,619 | 3,061 | 2,871,933 |
| C# Project File | `csproj` | 166 | 29,177 | 68 | 2,004 |
| C++ | `C`, `H`, `c++`, `c++m`, `cc`, `ccm`, `cpp`, `cppm`, `cu`, `cuh`, `cxx`, `cxxm`, `h`, `h++`, `hh`, `hip`, `hpp`, `hxx`, `inl`, `ino`, `ipp`, `ixx` | 45,325 | 19,787,553 | 10,971 | 3,369,858 |
| C3 | `c3`, `c3i` | 1,490 | 144,533 | 52 | 19,282 |
| Cabal | `cabal` | 24 | 4,994 | 2 | 206 |
| Cadence | `cdc` | 385 | 24,957 | 146 | 8,783 |
| Cairo | `cairo` | 321 | 63,387 | 229 | 49,234 |
| CFML (Tag) | `cfc`, `cfm`, `cfml` | 743 | 94,551 | 305 | 13,273 |
| Circom | `circom` | 104 | 31,779 | 37 | 3,737 |
| Clarity | `clar` | 6 | 1,150 | 364 | 98,558 |
| Clojure | `bb`, `clj`, `cljc`, `cljd`, `cljs`, `edn` | 1,303 | 91,956 | 83 | 8,026 |
| CMake | `CMakeLists.txt`, `cmake` | 1,199 | 100,409 | 289 | 24,411 |
| COBOL | `cbl`, `cob` | 736 | 66,059 | 5 | 4,056 |
| CoffeeScript | `coffee` | 463 | 13,454 | 142 | 14,964 |
| Crystal | `cr` | 756 | 31,415 | 251 | 21,219 |
| CSharp | `cs` | 7,623 | 916,389 | 2,181 | 274,579 |
| Csound | `csd`, `orc`, `sco`, `udo` | 170 | 12,793 | 155 | 29,276 |
| CSS | `css`, `pcss`, `postcss` | 3,988 | 1,253,316 | 2,786 | 293,950 |
| CSV | `csv` | 93 | 70,328 | 116 | 35,881 |
| Curry | `curry` | 95 | 9,521 | 151 | 13,906 |
| Cython | `pxd`, `pxi`, `pyx` | 87 | 22,076 | 56 | 28,077 |
| D | `d`, `dd`, `di` | 4,944 | 115,732 | 2,868 | 50,612 |
| Dafny | `dfy` | 109 | 20,978 | 37 | 9,725 |
| DAML | `daml` | 1,125 | 64,630 | 634 | 75,502 |
| Dart | `dart` | 5,580 | 966,385 | 984 | 286,691 |
| Defold | `gui_script`, `lua`, `render_script`, `script` | 4,602 | 757,791 | 4,054 | 323,146 |
| Diff | `diff`, `patch` | 175 | 38,704 | 125 | 17,384 |
| Docker Compose | `compose.yaml`, `compose.yml`, `docker-compose.yaml`, `docker-compose.yml` | 33 | 2,137 | 33 | 1,894 |
| Dockerfile | `Containerfile`, `Dockerfile`, `dockerfile` | 178 | 7,143 | 121 | 4,341 |
| DuckyScript | `txt` | 14,712 | 4,303,917 | 4,308 | 746,804 |
| Dune | `dune`, `dune-project`, `dune-workspace` | 2,169 | 20,306 | 64 | 1,074 |
| Dylan | `dylan`, `lid` | 104 | 12,829 | 14 | 4,185 |
| Earthfile | `Earthfile` | 187 | 10,790 | 0 | 0 |
| EBNF | `bnf`, `ebnf` | 118 | 2,045 | 100 | 3,757 |
| Editorconfig | `editorconfig` | 1,241 | 27,221 | 653 | 12,531 |
| EEx | `eex` | 175 | 9,812 | 79 | 1,142 |
| EJS | `ejs`, `eta` | 53 | 3,142 | 42 | 888 |
| Elisp | `el` | 366 | 50,369 | 32 | 24,354 |
| Elixir | `ex`, `exs`, `mix.lock` | 3,628 | 703,507 | 2,754 | 334,529 |
| Elm | `elm` | 178 | 29,727 | 481 | 87,416 |
| EmmyLua | `lua`, `lua.txt` | 4,598 | 753,486 | 4,050 | 322,497 |
| env | `conf`, `env`, `envrc`, `example`, `local`, `test` | 2,729 | 4,363,101 | 927 | 377,811 |
| ERB | `erb` | 504 | 12,378 | 650 | 20,288 |
| Erlang | `Emakefile`, `app.src`, `erl`, `erlang`, `escript`, `hrl`, `rebar.config`, `xrl`, `yrl` | 823 | 62,765 | 398 | 160,303 |
| Fift | `fif` | 16 | 3,128 | 12 | 1,666 |
| Fish | `fish` | 1,679 | 95,537 | 124 | 4,146 |
| Fortran | `F`, `F03`, `F08`, `F90`, `F95`, `f`, `f03`, `f08`, `f90`, `f95` | 1,701 | 144,281 | 64 | 26,431 |
| FSharp | `fs`, `fsi`, `fsscript`, `fsx` | 1,719 | 114,599 | 217 | 44,521 |
| Func | `fc` | 53 | 7,123 | 3 | 1,265 |
| G-code | `001`, `S`, `anc`, `apt`, `aptcl`, `bfb`, `cls`, `cnc`, `din`, `dnc`, `ecs`, `eia`, `fan`, `fgc`, `fnc`, `g`, `g00`, `gc`, `gcd`, `gco`, `gcode`, `gp`, `hnc`, `knc`, `lib`, `m`, `min`, `mmg`, `mpf`, `mpt`, `nc`, `ncd`, `ncf`, `ncg`, `nci`, `ncp`, `ngc`, `out`, `pim`, `pit`, `plt`, `ply`, `prg`, `pu1`, `rol`, `sbp`, `spf`, `ssb`, `sub`, `tap`, `tcn`, `xpi` | 4,107 | 273,922 | 421 | 102,203 |
| GDScript | `gd` | 291 | 60,269 | 146 | 11,563 |
| GDShader | `gdshader`, `gdshaderinc` | 40 | 2,864 | 63 | 2,700 |
| Gherkin | `feature`, `gherkin` | 237 | 40,343 | 0 | 0 |
| Git Attributes | `.gitattributes`, `gitattributes` | 598 | 7,855 | 196 | 1,155 |
| Git Ignore | `.containerignore`, `.cursorignore`, `.dockerignore`, `.eslintignore`, `.fdignore`, `.git-blame-ignore-revs`, `.gitignore`, `.gitignore_global`, `.ignore`, `.npmignore`, `.prettierignore`, `.rgignore`, `.vscodeignore` | 2,537 | 41,912 | 1,526 | 18,218 |
| Gleam | `gleam` | 140 | 21,319 | 80 | 22,537 |
| GLSL | `comp`, `frag`, `geom`, `glsl`, `mesh`, `rahit`, `rcall`, `rchit`, `rgen`, `rint`, `rmiss`, `task`, `tesc`, `tese`, `vert` | 134 | 5,998 | 162 | 8,186 |
| Go | `go` | 6,777 | 1,241,026 | 1,030 | 236,736 |
| Go Mod | `mod` | 217 | 3,050 | 22 | 1,044 |
| Go Sum | `go.sum` | 73 | 10,293 | 18 | 3,659 |
| Godot Resource | `gdextension`, `godot`, `import`, `tres`, `tscn` | 354 | 28,671 | 436 | 23,774 |
| GPR | `gpr` | 82 | 1,333 | 40 | 1,047 |
| Gradle | `gradle` | 48 | 3,876 | 302 | 8,191 |
| Gradle KTS | `gradle.kts` | 440 | 22,180 | 105 | 7,700 |
| GraphQL | `gql`, `graphql`, `graphqls` | 111 | 6,957 | 12 | 70,575 |
| Gren | `gren` | 53 | 21,586 | 27 | 7,468 |
| Groovy | `JenkinsFile`, `Jenkinsfile`, `gradle`, `groovy` | 905 | 20,942 | 306 | 8,493 |
| Handlebars | `handlebars`, `hbs` | 284 | 6,313 | 116 | 5,458 |
| Hare | `ha` | 856 | 136,813 | 34 | 5,389 |
| Haskell | `hs` | 3,451 | 412,293 | 87 | 26,658 |
| Haxe | `hx` | 450 | 99,891 | 595 | 133,115 |
| HCL | `hcl` | 111 | 4,400 | 1 | 244 |
| HEEx | `heex`, `html.eex`, `leex`, `neex` | 30 | 3,127 | 182 | 10,760 |
| HLSL | `hlsl` | 130 | 100,382 | 382 | 23,095 |
| HOCON | `conf`, `hocon` | 307 | 17,885 | 81 | 3,560 |
| Hoon | `hoon` | 863 | 174,194 | 6 | 19,643 |
| HQL | `hx` | 450 | 99,891 | 595 | 133,115 |
| HTML | `htm`, `html`, `shtml` | 10,018 | 2,295,992 | 2,198 | 486,738 |
| HTML+ERB | `html.erb` | 316 | 7,032 | 615 | 18,952 |
| HTML-Jinja | `j2`, `jinja`, `jinja2` | 15 | 291 | 52 | 7,933 |
| Hyprlang | `conf`, `hl` | 307 | 17,885 | 81 | 3,560 |
| Idris 2 | `idr`, `idr2` | 1,935 | 181,145 | 45 | 10,506 |
| Inform 6 | `h`, `inf` | 32,800 | 15,250,974 | 6,079 | 1,601,431 |
| ini | `automount`, `build`, `cfg`, `conf`, `container`, `image`, `inf`, `ini`, `kube`, `mount`, `network`, `path`, `pod`, `scope`, `service`, `slice`, `socket`, `swap`, `target`, `timer`, `volume` | 826 | 63,606 | 375 | 28,224 |
| Jai | `jai` | 210 | 128,032 | 47 | 49,905 |
| Janet | `janet` | 34 | 425 | 99 | 13,508 |
| Java | `java` | 10,212 | 1,229,248 | 4,759 | 598,616 |
| JavaScript | `cjs`, `js`, `jsx`, `mjs` | 441,195 | 80,878,626 | 336,966 | 60,106,002 |
| Jinja2 | `jinja`, `jinja2` | 14 | 251 | 49 | 7,872 |
| jq | `jq` | 2,344 | 53,222 | 2 | 3,206 |
| JSON | `deno.lock`, `flake.lock`, `geojson`, `json`, `json.dist`, `prettierrc`, `topojson` | 63,328 | 19,373,499 | 42,301 | 8,753,602 |
| JSON5 | `json5` | 196 | 13,443 | 53 | 1,493 |
| JSONC | `babelrc`, `bun.lock`, `devcontainer.json`, `eslintrc`, `jshintrc`, `jsonc`, `luaurc`, `pyrightconfig.json`, `stylelintrc`, `swcrc`, `tsconfig.json` | 4,991 | 90,779 | 2,764 | 49,944 |
| Julia | `jl` | 2,322 | 102,555 | 96 | 17,138 |
| Koka | `kk` | 1,104 | 115,196 | 89 | 9,597 |
| Kotlin | `kt`, `kts` | 7,749 | 876,912 | 4,407 | 482,719 |
| LaTeX | `cls`, `latex`, `sty`, `tex` | 573 | 104,236 | 434 | 105,374 |
| Lean 4 | `lean` | 479 | 93,139 | 250 | 24,242 |
| LESS | `less` | 96 | 5,100 | 745 | 59,929 |
| Linker Script | `ld` | 22 | 5,594 | 1 | 9 |
| Liquidsoap | `liq` | 632 | 46,556 | 23 | 1,403 |
| LLVM IR | `ll` | 19 | 11,099 | 5 | 105 |
| LOG | `log` | 1,225 | 99,706 | 18 | 4,354 |
| Logcat | `log`, `logcat` | 1,225 | 99,706 | 18 | 4,354 |
| Logstash Config | `conf` | 307 | 17,885 | 81 | 3,560 |
| Lua | `lua` | 4,595 | 752,671 | 4,050 | 322,497 |
| Luau | `luau` | 61 | 6,808 | 69 | 16,363 |
| Make | `GNUmakefile`, `Makefile`, `OCamlMakefile`, `mak`, `makefile`, `mk` | 920 | 67,616 | 654 | 34,277 |
| Markdown | `MD`, `markdown`, `md`, `mdc`, `mdwn`, `mdx` | 54,871 | 8,871,097 | 36,438 | 5,736,831 |
| MATLAB | `m` | 1,496 | 108,343 | 118 | 17,204 |
| MDX | `mdx` | 618 | 145,760 | 1,048 | 182,432 |
| Menhir | `mly` | 21 | 2,201 | 3 | 5,568 |
| Mermaid | `mermaid`, `mmd` | 170 | 17,737 | 0 | 0 |
| Meson | `meson.build`, `meson.options`, `meson_options.txt` | 56 | 4,322 | 25 | 1,031 |
| Metal | `metal` | 44 | 5,796 | 86 | 3,183 |
| Mojo | `mojo` | 135 | 51,688 | 62 | 13,453 |
| MoonBit | `mbt` | 895 | 219,134 | 99 | 66,009 |
| Motoko | `mo` | 87 | 50,087 | 3 | 9,029 |
| Move | `move` | 4,886 | 459,616 | 4,558 | 231,542 |
| move | `move` | 4,886 | 459,616 | 4,558 | 231,542 |
| Move.toml | `Move.toml` | 480 | 4,462 | 1,046 | 8,093 |
| MSBuild File | `proj`, `props`, `targets` | 130 | 5,595 | 82 | 2,435 |
| Mustache | `mustache` | 14 | 396 | 31 | 3,590 |
| NetLinx | `axb`, `axi`, `axs`, `lib` | 24 | 7,952 | 84 | 18,126 |
| Nim | `nim`, `nims` | 2,174 | 130,490 | 73 | 9,081 |
| Nix | `nix` | 141 | 9,805 | 40 | 5,368 |
| Noir | `nr` | 50 | 9,481 | 248 | 36,180 |
| Nu | `nu`, `nuon` | 281 | 15,940 | 3 | 747 |
| Oberon | `Mod`, `mod` | 217 | 3,050 | 22 | 1,044 |
| Objective-C | `h`, `hh`, `m`, `mm` | 34,309 | 15,374,593 | 6,501 | 1,685,137 |
| ObjectScript XML | `xml` | 2,479 | 290,990 | 3,764 | 565,728 |
| objectscript_routine | `inc`, `int`, `mac`, `rtn` | 429 | 97,917 | 414 | 33,313 |
| ObjectscriptUdl | `cls` | 428 | 67,810 | 262 | 60,598 |
| OCaml | `ml` | 4,216 | 390,921 | 234 | 43,336 |
| OCaml Interface | `mli` | 1,151 | 62,352 | 111 | 6,178 |
| OCamllex | `mll` | 26 | 1,886 | 6 | 1,300 |
| Odin | `odin` | 233 | 67,978 | 41 | 11,742 |
| OMNeT++ MSG | `msg` | 13 | 1,157 | 173 | 26,397 |
| OpenSCAD | `scad` | 95 | 87,712 | 389 | 39,948 |
| OpenTofu | `tf`, `tofu` | 1,817 | 104,921 | 9 | 637 |
| Org | `org` | 25 | 13,134 | 59 | 11,525 |
| P4 Language | `p4` | 153 | 51,114 | 71 | 9,810 |
| Pact | `pact`, `repl` | 214 | 27,900 | 58 | 12,955 |
| Papyrus | `psc` | 110 | 7,967 | 25 | 16,899 |
| Pascal | `dpr`, `inc`, `lpr`, `p`, `pas`, `pp` | 3,055 | 254,786 | 414 | 33,239 |
| Perl | `pl`, `pm`, `t` | 5,358 | 510,419 | 140 | 30,112 |
| PHP | `php`, `phpt`, `phtml` | 6,703 | 948,825 | 2,841 | 310,714 |
| Plain Text | `txt` | 14,712 | 4,303,917 | 4,308 | 746,804 |
| PlatformIO | `platformio.ini` | 37 | 1,014 | 34 | 1,197 |
| PO | `po`, `pot` | 301 | 1,951,174 | 511 | 918,280 |
| Pony | `pony` | 1,062 | 156,283 | 299 | 70,876 |
| PowerShell | `ps1`, `psm1` | 1,200 | 32,814 | 93 | 6,642 |
| Processing | `pde` | 10 | 466 | 25 | 3,625 |
| Prolog | `P`, `pl`, `pro` | 3,174 | 107,456 | 36 | 5,852 |
| Properties | `properties` | 459 | 118,853 | 208 | 1,745 |
| Proto | `proto` | 354 | 55,767 | 47 | 10,576 |
| PureScript | `purs` | 67 | 6,300 | 215 | 21,372 |
| Python | `mpy`, `py`, `pyi` | 12,085 | 2,935,703 | 4,018 | 981,977 |
| QML | `qml` | 229 | 29,866 | 26 | 3,723 |
| Quadlet | `artifact`, `build`, `container`, `image`, `kube`, `network`, `pod`, `volume` | 60 | 10,220 | 36 | 2,448 |
| QuakeC | `qc` | 704 | 188,902 | 198 | 83,251 |
| Quint | `qnt` | 60 | 10,996 | 0 | 0 |
| R | `R`, `r` | 1,595 | 134,061 | 138 | 61,872 |
| Racket | `rkt` | 3,268 | 166,018 | 43 | 6,293 |
| Rainbow CSV (,) | `csv` | 93 | 70,328 | 116 | 35,881 |
| Reason | `re` | 205 | 74,472 | 246 | 52,598 |
| Reason Interface | `rei` | 92 | 5,723 | 129 | 4,567 |
| Red | `red`, `reds` | 1,217 | 350,152 | 7,518 | 141,767 |
| REDscript | `reds` | 706 | 263,352 | 7,461 | 132,796 |
| ReScript | `res`, `resi` | 90 | 13,921 | 6 | 1,213 |
| reST | `rst` | 3,574 | 660,419 | 1,412 | 164,648 |
| Roc | `roc` | 77 | 15,428 | 19 | 5,525 |
| RPM Spec | `spec` | 42 | 7,041 | 8 | 735 |
| Ruby | `Appfile`, `Appraisals`, `Berksfile`, `Berksfile.lock`, `Brewfile`, `Capfile`, `Cheffile`, `Dangerfile`, `Deliverfile`, `Fastfile`, `Gemfile`, `Guardfile`, `Gymfile`, `Hobofile`, `Matchfile`, `Podfile`, `Puppetfile`, `Rakefile`, `Rantfile`, `Scanfile`, `Snapfile`, `Steepfile`, `Thorfile`, `Vagrantfile`, `builder`, `cap`, `capfile`, `gemspec`, `irbrc`, `jbuilder`, `pryrc`, `rabl`, `rake`, `rb`, `rdoc`, `ru`, `rxml`, `simplecov`, `thor` | 7,709 | 775,866 | 4,138 | 508,312 |
| Rust | `rs` | 11,256 | 3,108,138 | 4,822 | 1,884,966 |
| Salesforce Log | `log`, `sflog` | 1,225 | 99,706 | 18 | 4,354 |
| Scala | `mill`, `sbt`, `sc`, `scala` | 2,380 | 169,107 | 1,553 | 170,847 |
| Scheme | `scm`, `ss` | 2,734 | 149,787 | 23 | 4,641 |
| SCSS | `scss` | 2,039 | 200,286 | 862 | 97,330 |
| Shell Script | `.env`, `APKBUILD`, `PKGBUILD`, `bash`, `bash_aliases`, `bash_login`, `bash_logout`, `bash_profile`, `bashrc`, `bats`, `brushrc`, `ebuild`, `envrc`, `profile`, `sh`, `zlogin`, `zprofile`, `zsh`, `zsh_aliases`, `zsh_histfile`, `zsh_profile`, `zshenv`, `zshrc` | 2,821 | 191,677 | 1,132 | 57,873 |
| Simula | `SIM`, `SIm`, `SiM`, `Sim`, `sIM`, `sIm`, `siM`, `sim`, `simula` | 107 | 6,990 | 0 | 0 |
| Slint | `Cargo.lock`, `slint` | 134 | 125,935 | 16 | 93,178 |
| Smali | `smali` | 221 | 14,909 | 0 | 0 |
| Solidity | `sol` | 424 | 51,075 | 219 | 30,641 |
| Sourcepawn | `sp` | 94 | 25,115 | 22 | 37,736 |
| Spicy | `evt`, `hlt`, `spicy` | 59 | 8,979 | 0 | 0 |
| SQL | `sql` | 541 | 21,540 | 461 | 16,396 |
| Squirrel | `nut` | 74 | 52,345 | 146 | 67,535 |
| SSH Config | `config`, `ssh_config` | 231 | 9,942 | 96 | 2,574 |
| Stan | `stan` | 59 | 4,834 | 69 | 2,933 |
| Standard ML | `fun`, `sig`, `sml` | 1,509 | 305,082 | 32 | 2,227 |
| Starlark | `.tilt`, `.tiltfile`, `BUCK`, `BUILD`, `BUILD.bazel`, `MODULE.bazel`, `PACKAGE`, `REPO.bazel`, `Tiltfile`, `WORKSPACE`, `WORKSPACE.bzlmod`, `bxl`, `bzl`, `star` | 429 | 45,885 | 99 | 14,722 |
| Strings | `strings` | 1,884 | 201,155 | 54 | 203 |
| Structured Text | `st`, `stx` | 678 | 12,726 | 944 | 93,718 |
| Styx | `styx` | 121 | 2,405 | 0 | 0 |
| Svelte | `svelte` | 138 | 11,518 | 85 | 11,058 |
| Sway | `sw` | 2,052 | 168,474 | 92 | 16,825 |
| Swift | `swift`, `swiftinterface` | 5,328 | 606,543 | 1,906 | 270,536 |
| SystemVerilog | `sv`, `svh`, `v`, `vh` | 1,795 | 1,941,974 | 57 | 14,940 |
| Tact | `tact` | 1,016 | 35,376 | 19 | 2,144 |
| TCL | `tcl`, `tm` | 2,000 | 217,552 | 1,267 | 585,323 |
| Terraform | `tf`, `tofu` | 1,817 | 104,921 | 9 | 637 |
| Thrift | `thrift` | 42 | 8,946 | 0 | 0 |
| TLA+ Cfg | `cfg` | 212 | 26,139 | 129 | 16,248 |
| Todotxt | `todo.txt`, `txt` | 14,712 | 4,303,917 | 4,308 | 746,804 |
| Tolk | `tolk` | 101 | 24,660 | 0 | 0 |
| TOML | `Cargo.lock`, `Pipfile`, `toml`, `uv.lock` | 4,792 | 261,198 | 2,184 | 136,457 |
| Tonel Smalltalk | `st` | 678 | 12,726 | 944 | 93,718 |
| Tree-sitter Query | `scm` | 2,730 | 139,731 | 22 | 2,457 |
| TSX | `tsx` | 2,064 | 227,317 | 3,167 | 218,564 |
| Twig | `html.twig`, `twig`, `twig.html` | 24 | 84 | 74 | 4,753 |
| TypeScript | `cts`, `mts`, `ts` | 171,017 | 19,989,203 | 137,774 | 17,803,284 |
| Typst | `typ`, `typst` | 314 | 48,230 | 0 | 0 |
| ucode | `uc` | 17 | 5,077 | 27 | 5,980 |
| Uiua | `ua`, `uiua` | 566 | 3,852 | 0 | 0 |
| V | `mod`, `v`, `vsh`, `vv` | 2,054 | 1,954,274 | 47 | 13,217 |
| Vala | `vala`, `vapi` | 1,492 | 341,154 | 123 | 38,853 |
| VHDL | `vhd`, `vhdl` | 103 | 33,107 | 331 | 71,797 |
| Vue.js | `vue` | 986 | 73,174 | 603 | 18,240 |
| WebIDL | `webidl` | 229 | 3,781 | 0 | 0 |
| Wgsl | `wgsl` | 42 | 1,735 | 50 | 3,073 |
| WGSL/WESL | `wesl`, `wgsl` | 43 | 1,742 | 50 | 3,073 |
| Wren | `wren` | 2,066 | 106,690 | 1 | 3,158 |
| Xcode Project | `pbxproj` | 188 | 96,960 | 34 | 32,611 |
| XML | `xml` | 2,479 | 290,990 | 3,764 | 565,728 |
| YAML | `bst`, `clang-format`, `clangd`, `pixi.lock`, `yaml`, `yml` | 14,028 | 1,108,691 | 8,142 | 1,483,123 |
| Zeek | `zeek` | 2,593 | 148,354 | 11 | 4,546 |
| Zig | `zig`, `zon` | 3,690 | 849,966 | 473 | 178,418 |

## No filename registration

These languages cannot be measured by the filename census: AsciiDoc Inline, CFML (Query), comment, Doxygen, EL, EmmyLuadoc, GitHub Actions, Jinja-Inline, Jinja2 Inline, JSDoc, LilyPond Scheme, Markdown Inline, Markdown-Inline, Nomad ACL, Nomad Agent, Nomad CSI Volume, Nomad Dynamic Host Volume, Nomad Namespace, Nomad Node Pool, Nomad Resource Quota, Nomad Variable, objectscript, php_only, PHPDoc, Quarkdown-Inline, Rainbow CSV (;), Rainbow CSV (|), Regex, RSTML, SassDoc, Zed Keybind Context.

## Unavailable extension inventories

- `bearded`: HTTP Error 404: Not Found
- `irix-terminal-theme`: fatal: could not read Username for 'https://codeberg.org': No such device or address
- `nanowise`: HTTP Error 404: Not Found
- `spai-zero-theme`: HTTP Error 404: Not Found
- `vanta-theme`: fatal: mismatched algorithms: client sha1; server sha256
- `zedburn`: HTTP Error 404: Not Found
