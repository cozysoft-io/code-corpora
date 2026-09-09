# Proposals for the remaining language data

The current census has **302 language names** below 21 files or 2,000 raw lines combined. This is a proposal, with archive measurements and a per-language route in [`data-proposals.json`](data-proposals.json). No new corpus entries or split assignments are made here.

## Recommended first batch

1. Import **Rosetta Code through a language-aware adapter**. It immediately supplies useful small programs for several previously difficult languages.
2. Extract the **Tree-sitter corpus tests already in `grammars/`**. This has the widest reach without fetching more repositories.
3. Add **Linguist samples** for broad language-labelled seeds and links back to source projects.
4. Add **Wasmtime, Alloy, Zephyr, and Bicep**, then targeted schema/compiler suites. These repositories contribute several related formats together.

## Rosetta Code

I inspected [`acmeism/RosettaCodeData`](https://github.com/acmeism/RosettaCodeData/tree/1d475861d7141ef2fafff293d9339f56e4b0f5db) at `1d475861d7141ef2fafff293d9339f56e4b0f5db`. Its [README](https://github.com/acmeism/RosettaCodeData#readme) describes the language/task organization and warns that some extensions were guessed. Count only the canonical `Task/` tree; the alternate language view must not duplicate the same programs.

| Remaining language | UTF-8 samples | Raw lines | Mirror suffix | Meets current target after import? |
| --- | ---: | ---: | --- | --- |
| Arturo | 827 | 13,550 | .arturo | yes |
| Uiua | 566 | 3,852 | .uiua | yes |
| MiniZinc | 33 | 345 | .minizinc | partial |
| Simula | 107 | 6,990 | .simula | yes |
| Brainfuck | 53 | 1,227 | .bf | partial |
| CFEngine | 7 | 153 | .cfengine | partial |
| LilyPond | 5 | 39 | .lily | partial |
| Inko | 1 | 3 | .inko | partial |
| NSIS | 7 | 113 | .nsis | partial |
| SageMath | 6 | 107 | .sage | partial |
| Unison | 5 | 44 | .u | partial |
| XQuery | 25 | 360 | .xquery | partial |

**Arturo, Uiua and Simula would clear both thresholds once imported.** The coverage tool accepts their longer export suffixes `.arturo`, `.uiua` and `.simula` alongside the registered suffixes `.art`, `.ua` and case variants of `.sim`. These files can keep their original names.

This needs content-aware curation: some samples contain shell transcripts or output, rather than only source. Directory labels also prevent misleading suffix matches: `.bf` includes Befunge, `.ps` is PostScript rather than Pine Script, `.k` is K rather than KCL, and S-lang is not the Slang shading language. The raw scanner incorrectly suggests that Brainfuck clears the line target; the reviewed Brainfuck subset has only 1,227 lines.

For a first import, keep this collection in training. If a held-out dataset is later needed, create an explicit dataset split by **task family**, grouping every language implementation and solution variant of a task together. Never randomly split individual files or treat another Rosetta mirror as independent held-out data. Small Rosetta programs provide syntax and local-reference examples; most do not provide whole-project import or indexing workloads.

## Reuse local grammars and broad sample collections

The local inventory found conventional corpus-test headers in grammars associated with **226 remaining language names**. This is an availability screen, not a promise of sufficient volume or correct coverage of every injected-language variant. The [Tree-sitter test format](https://tree-sitter.github.io/tree-sitter/creating-parsers/5-writing-tests.html) separates test name, source input and expected tree. An importer should emit just the input body and preserve the original case metadata.

Keep valid examples and expected-error cases distinguishable. Count distinct logical test cases rather than splitting large files to inflate the file count. Deduplicate grammar forks and copied suites before assigning splits. These fixtures can exercise parsing and recovery even when no build or LSP oracle exists.

Linguist contains samples under case-insensitively exact language labels for **72 remaining names** in the inspected snapshot. Many are only a few files. Use its labels and provenance, then follow representative samples to their original repositories. Its [contribution guide](https://github.com/github-linguist/linguist/blob/main/CONTRIBUTING.md#adding-an-extension-to-a-language) requests representative real-world samples and source/license information.

Also consider [Prism](https://github.com/PrismJS/prism/tree/master/tests/languages) and [Highlight.js](https://github.com/highlightjs/highlight.js/tree/main/test): their fixtures put language identity in paths and often store source in `.test` or `.txt` wrappers. They need adapters. A plain clone produced zero native-suffix hits for Prism among the remaining languages; that does not mean it lacks language examples.

## Measured repositories covering related languages

Counts below are UTF-8 files/raw lines from pinned archives. Tests, examples and generated files are allowed in this screen. Contributions are **not additive coverage guarantees**: deduplicate copied sources and inspect language identity before import.

| Repository | Relevant data found | Why use it |
| --- | --- | --- |
| [bytecodealliance/wasmtime](https://github.com/bytecodealliance/wasmtime/tree/ad985bc64f6567a065a1d94e29022346de1123f1) | ISLE: 108 / 65,731; WebAssembly Text Format: 2,667 / 193,174; WIT: 97 / 15,031 | Instruction-selection rules, component interfaces and WebAssembly tests in one project. |
| [grafana/alloy](https://github.com/grafana/alloy/tree/a38299a4e665bdf9c18f97e95a5d7f6c554cdfe9) | Grafana Alloy: 214 / 12,017; Jsonnet: 29 / 4,822; Txtar: 126 / 9,267 | Collector configurations, Jsonnet mixins and text-archive test fixtures. |
| [zephyrproject-rtos/zephyr](https://github.com/zephyrproject-rtos/zephyr/tree/042104ba7e2d2b2dace4d3ef7a7d5485e593f305) | devicetree: 5,883 / 687,041; Kconfig: 2,077 / 98,015; Python requirements: 6 / 1,663 | Many real hardware descriptions and build-configuration files; allow a larger checkout. |
| [Azure/bicep](https://github.com/Azure/bicep/tree/1758d3ad5401d1116efc049303d7ed841a1bae2e) | Bicep: 1,327 / 545,547; Bicep Parameters: 139 / 12,738 | Accept compiler fixtures and deployment examples; include both source and parameters. |
| [cue-lang/cue](https://github.com/cue-lang/cue/tree/eb886ed07a0864cc6bbc081bb8f1efa9fb834944) | CUE: 145 / 9,401; Txtar: 2,273 / 240,970 | Accept language tests; unpack txtar members for additional typed source. |
| [hashicorp/nomad](https://github.com/hashicorp/nomad/tree/9d52ef0f3ce672f01c30046a04a98a8b8b19c86a) | Nomad Job: 193 / 12,309; Glimmer (JavaScript): 2 / 316; Terraform Vars: 4 / 70; OpenTofu Vars: 4 / 70 | Job specifications plus UI and deployment configuration; secondary languages are partial contributions. |
| [microsoft/typespec](https://github.com/microsoft/typespec/tree/f16f4d44efe4f48d9dbfd82ffdb47609457e2659) | Typespec: 342 / 28,368 | Service-schema examples and compiler tests. |
| [google/flatbuffers](https://github.com/google/flatbuffers/tree/5761d6e67af841d15ee21bc1ce9a78ffa9cf939e) | FlatBuffers: 108 / 3,392 | Schema definitions and schema-parser tests. |
| [capnproto/capnproto](https://github.com/capnproto/capnproto/tree/851c45bb39c34c3f20f9d9ebe9f34a7e39109b6f) | Cap'n Proto: 22 / 5,218 | Schemas, examples and tests. |
| [apache/avro](https://github.com/apache/avro/tree/d02512a5d7cc75c552ec1a7fcd50ed01b960911c) | Apache Avro (IDL): 67 / 2,437 | IDL parser/compiler fixtures. |
| [cel-expr/cel-spec](https://github.com/cel-expr/cel-spec/tree/ba58ae5007845f3a1279b488cdeb79645ce958bb) | Textproto: 31 / 20,341 | Text-format protocol-buffer conformance data. |

LLVM is a strong additional candidate for **MLIR, PDLL and TableGen**. Its [PDLL documentation](https://mlir.llvm.org/docs/PDLL/) describes integration with TableGen definitions. Inspect or sparsely fetch the relevant LLVM/MLIR subtrees; the complete archive was not measured here. Gentoo, Nixpkgs and Gecko are broader follow-up candidates, but their size alone does not establish useful coverage, so they are not part of the measured first batch.

## Reconsider previously rejected language tools

Drop the requirement for two independent production repositories before admitting any data. One canonical compiler with a substantial test suite can give a small language useful initial coverage. Existing training projects keep their split; a single-source language can initially have training data only.

| Existing candidate snapshot | Target-language files / raw lines | Relaxed requirement |
| --- | --- | --- |
| [DanielXMoore/Civet](https://github.com/DanielXMoore/Civet/tree/10a55dd4b311303a827984fbe15962e991af0abb) | Civet: 322 / 86,845; Hera: 3 / 10,524 | Allow compiler fixtures, examples and small ecosystems; classify generated output separately. |
| [ProvableHQ/leo](https://github.com/ProvableHQ/leo/tree/f3578da035676364817aa7dffa9d21ecc3cd9dc4) | Leo: 2,639 / 124,443; Aleo: 31 / 1,761 | Allow compiler fixtures, examples and small ecosystems; classify generated output separately. |
| [vectordotdev/vrl](https://github.com/vectordotdev/vrl/tree/6cab87fa8112ae42135ac865b862ec1cf0f9915e) | VRL: 314 / 4,766 | Allow compiler fixtures, examples and small ecosystems; classify generated output separately. |
| [HigherOrderCO/Bend](https://github.com/HigherOrderCO/Bend/tree/814453670d0e0d6777c1313c972764dba0491b7f) | Bend: 525 / 6,374 | Allow compiler fixtures, examples and small ecosystems; classify generated output separately. |
| [inko-lang/inko](https://github.com/inko-lang/inko/tree/5a9a0cca46fb337cac11c8ec43ea1a59c0ebaf03) | Inko: 463 / 99,882 | Allow compiler fixtures, examples and small ecosystems; classify generated output separately. |
| [hsutter/cppfront](https://github.com/hsutter/cppfront/tree/66eb614ff7947ed2502227ae55bc686d98868abf) | Cpp2: 197 / 513,795 | Allow compiler fixtures, examples and small ecosystems; classify generated output separately. |
| [duso-org/duso](https://github.com/duso-org/duso/tree/2fc8b28bd3032ffad67ee2e9e519bb9521644d9f) | Duso: 184 / 13,768 | Allow compiler fixtures, examples and small ecosystems; classify generated output separately. |
| [rhaiscript/rhai](https://github.com/rhaiscript/rhai/tree/4d9e4d80809fc2234564717c909db412effeaf52) | Rhai: 45 / 23,095 | Allow compiler fixtures, examples and small ecosystems; classify generated output separately. |
| [Zokrates/ZoKrates](https://github.com/Zokrates/ZoKrates/tree/8699128ad0034f2f60d7de60d397ae7986bb23fe) | ZoKrates: 592 / 10,824 | Allow compiler fixtures, examples and small ecosystems; classify generated output separately. |

These are earlier screening measurements, not fresh checkout counts. In particular, the 3 Hera files and 1,761 Aleo lines are useful contributions but do not individually satisfy both current thresholds.

## Change what qualifies, without losing what the data means

- **Accept examples, tutorials, compiler tests, standard libraries, and mature archived projects.** Record source purpose and syntax validity. Keep generated cases explicitly labelled.
- **Separate syntax, local-reference, cross-file-reference and full-oracle capability.** A parser fixture is useful without a build, but does not establish import resolution. Continue to require an oracle before reporting reference accuracy.
- **Permit one source initially.** Prioritize marginal language coverage per repository; supplement an ecosystem later instead of blocking it on a train/test pair.
- **Treat short formats differently.** CODEOWNERS, Desktop Entry and Python requirements already have more than 20 filename matches but fewer than 2,000 lines. For such formats, propose a diversity/valid-example target instead of collecting thousands of redundant lines. This proposal does not change the current census thresholds.
- **Preserve immutable origins and split isolation.** Keep repository commit, original path, task/case ID, extraction method, language label and source/license metadata. Deduplicate before splitting. Aggregated copies and generated variants inherit their source group.

## Fix identification before collecting more

The registered-suffix census measures filename matches, not all available language data. Ansible normally uses YAML; Django normally uses HTML filenames; Helm templates are not measured by its `.helmignore` registration; CFML script is already present under `.cfc`/`.cfm`; injected strings such as Nim Format String have no natural standalone suffix. Add explicit dataset/path or extraction mappings, validated against actual contents. Keep the raw registration census available so this richer classification is auditable.

For the uncommon tail, start with the registered extension/grammar and the language author’s documentation. Extract labelled examples with provenance. If no public examples exist, hand-authored minimal fixtures are acceptable as explicitly synthetic syntax coverage; they must not be presented as independent production examples.

## Route for every remaining language

The first source below is a proposed starting point. The JSON includes alternatives, candidate measurements, grammar corpus paths and the current counts for all 302 names. Grammar corpus availability does not itself establish the 21-file/2,000-line target. Candidate links marked for inspection have not been measured under the relaxed rules.

| Language | Current files / lines | Proposed starting point |
| --- | ---: | --- |
| Aleo | 0 / 0 | Extract [aleo](https://github.com/MagicGordon/tree-sitter-aleo) corpus inputs (1 corpus files). |
| Alex | 11 / 874 | Extract [alex](https://github.com/brandonchinn178/tree-sitter-alex) corpus inputs (4 corpus files). |
| Amber | 1 / 10 | Extract [amber](https://github.com/amber-lang/tree-sitter-amber) corpus inputs (1 corpus files). |
| Angular | 14 / 1,275 | Extract [angular](https://github.com/dlvandenberg/tree-sitter-angular) corpus inputs (16 corpus files). |
| Animation.txt | 0 / 0 | Extract [animationtxt](https://github.com/notpeter/tree-sitter-animationtxt) corpus inputs (1 corpus files). |
| Ansible | 0 / 0 | Real playbooks are usually YAML; select by project path and playbook structure. The registered .ansible suffix misses them. Generic YAML grammar tests are only YAML syntax evidence. |
| Answer Set Programming | 1 / 1 | Extract [clingo](https://github.com/potassco/tree-sitter-clingo) corpus inputs (10 corpus files). |
| Apache Avro (IDL) | 0 / 0 | [Upstream source/examples/tests](https://github.com/apache/avro). |
| Arturo | 2 / 4 | [Rosetta Code labelled tasks](https://github.com/acmeism/RosettaCodeData). |
| ASN.1 | 0 / 0 | Extract [asn1](https://github.com/tdanner/tree-sitter-asn1) corpus inputs (5 corpus files). |
| ASP Classic | 1 / 1 | [Inspect upstream examples/tests](https://github.com/rcdmk/aspJSON). |
| ass | 0 / 0 | [Inspect upstream examples/tests](https://github.com/libass/libass). |
| Awsum | 0 / 0 | Extract [awsum](https://github.com/awsum-lang/tree-sitter-awsum) corpus inputs (1 corpus files). |
| Ayla | 0 / 0 | Inspect [registered extension](https://github.com/z-sk1/zed-ayla) examples/docs. |
| Baml | 0 / 0 | [Linguist labelled samples](https://github.com/github-linguist/linguist). |
| bazelrc | 10 / 499 | Extract [bazelrc](https://github.com/zaucy/tree-sitter-bazelrc) corpus inputs (1 corpus files). |
| Beancount | 0 / 0 | Extract [beancount](https://github.com/polarmutex/tree-sitter-beancount) corpus inputs (30 corpus files). |
| Beast | 0 / 0 | Extract [beast](https://github.com/phtn/beast-ext) corpus inputs (1 corpus files). |
| Bend | 0 / 0 | Extract [bend](https://github.com/LaBatata101/tree-sitter-bend) corpus inputs (6 corpus files). |
| Bicep | 1 / 4 | [Upstream source/examples/tests](https://github.com/Azure/bicep). |
| Bicep Parameters | 0 / 0 | [Upstream source/examples/tests](https://github.com/Azure/bicep). |
| Blueprint | 1 / 11 | Extract [blueprint](https://github.com/smrtrfszm/tree-sitter-blueprint) corpus inputs (11 corpus files). |
| Brainfuck | 0 / 0 | [Rosetta Code labelled tasks](https://github.com/acmeism/RosettaCodeData). |
| Bruno | 0 / 0 | Extract [bruno](https://github.com/Scalamando/tree-sitter-bruno) corpus inputs (7 corpus files). |
| Build2 manifest | 42 / 870 | [Inspect upstream examples/tests](https://github.com/build2/bpkg). |
| C# Solution File | 43 / 738 | Extract [xml](https://github.com/tree-sitter-grammars/tree-sitter-xml) corpus inputs (5 corpus files). |
| Caddyfile | 5 / 347 | Extract [caddyfile](https://github.com/nusnewob/tree-sitter-caddyfile) corpus inputs (14 corpus files). |
| Candid | 0 / 0 | [Inspect upstream examples/tests](https://github.com/dfinity/candid). |
| CAP CDS | 0 / 0 | Extract [cds](https://github.com/cap-js-community/tree-sitter-cds) corpus inputs (20 corpus files). |
| Cap'n Proto | 16 / 3,370 | [Upstream source/examples/tests](https://github.com/capnproto/capnproto). |
| Cartan | 0 / 0 | Extract [cartan](https://github.com/cartan-lang/tree-sitter-cartan) corpus inputs (1 corpus files). |
| Carve | 0 / 0 | Extract [carve](https://github.com/markup-carve/tree-sitter-carve) corpus inputs (1 corpus files). |
| Cedar | 0 / 0 | Extract [cedar](https://github.com/chrnorm/tree-sitter-cedar) corpus inputs (3 corpus files). |
| CFEngine | 2 / 8 | [Rosetta Code labelled tasks](https://github.com/acmeism/RosettaCodeData). |
| CFML (Script) | 0 / 0 | Existing selected CFML repositories contain script in .cfc/.cfm. Establish script syntax from file content; the .cfs registration alone misses it. |
| Cherri | 0 / 0 | [Inspect upstream examples/tests](https://github.com/electrikmilk/cherri). |
| Civet | 0 / 0 | Extract [civet](https://github.com/DanielXMoore/Civet) corpus inputs (3 corpus files). |
| CODEOWNERS | 73 / 541 | [Linguist labelled samples](https://github.com/github-linguist/linguist). |
| Coi | 0 / 0 | Extract [coi](https://github.com/jturner/tree-sitter-coi) corpus inputs (4 corpus files). |
| CONL | 0 / 0 | Extract [conl](https://github.com/ConradIrwin/tree-sitter-conl) corpus inputs (4 corpus files). |
| Cooklang | 0 / 0 | Extract [cooklang](https://github.com/addcninblue/tree-sitter-cooklang) corpus inputs (3 corpus files). |
| Corn | 0 / 0 | Inspect [registered extension](https://github.com/corn-config/corn-zed.git) examples/docs. |
| Cpp2 | 0 / 0 | Extract [cpp2](https://github.com/tsoj/tree-sitter-cpp2) corpus inputs (13 corpus files). |
| CQL | 6 / 356 | [Linguist labelled samples](https://github.com/github-linguist/linguist). |
| CSS + HubL | 0 / 0 | Use HubSpot CMS theme templates; separate embedded HubL from host HTML/CSS with source offsets. |
| CUE | 3 / 14 | [Upstream source/examples/tests](https://github.com/cue-lang/cue). |
| Cylc | 5 / 835 | Extract [cylc](https://github.com/elliotfontaine/tree-sitter-cylc) corpus inputs (15 corpus files). |
| Cypher | 6 / 356 | [Linguist labelled samples](https://github.com/github-linguist/linguist). |
| D2 | 1 / 116 | Extract [d2](https://git.pleshevski.ru/pleshevskiy/tree-sitter-d2) corpus inputs (5 corpus files). |
| Dang | 0 / 0 | Extract [dang](https://github.com/vito/dang) corpus inputs (4 corpus files). |
| DataZinc | 0 / 0 | Extract [datazinc](https://github.com/shackle-rs/shackle) corpus inputs (10 corpus files). |
| DBML | 1 / 19 | Extract [dbml](https://github.com/dynamotn/tree-sitter-dbml) corpus inputs (1 corpus files). |
| Demo Tape | 1 / 99 | Inspect [registered extension](https://github.com/fnando/zed-demotape.git) examples/docs. |
| Desktop Entry | 25 / 461 | Extract [desktop](https://github.com/ValdezFOmar/tree-sitter-desktop) corpus inputs (1 corpus files). |
| devicetree | 1 / 8 | [Upstream source/examples/tests](https://github.com/zephyrproject-rtos/zephyr). |
| Dhall | 24 / 177 | Extract [dhall](https://github.com/jbellerb/tree-sitter-dhall) corpus inputs (23 corpus files). |
| Django | 0 / 0 | Select known Django template directories; the registered dj.html/dj.md/dj.txt names miss normal .html templates. Do not label arbitrary HTML as Django. |
| Djot | 10 / 2,102 | Extract [djot](https://github.com/nzoschke/tree-sitter-djot) corpus inputs (2 corpus files). |
| DOT | 19 / 780 | Extract [dot](https://github.com/rydesun/tree-sitter-dot) corpus inputs (3 corpus files). |
| Duper | 0 / 0 | Extract [duper](https://github.com/EpicEric/duper) corpus inputs (11 corpus files). |
| Duso | 0 / 0 | [Compiler and language tests](https://github.com/duso-org/duso). |
| Ebuild | 0 / 0 | Extract [ebuild](https://gitlab.com/paveloom-g/forks/tree-sitter-ebuild) corpus inputs (5 corpus files). |
| ECR | 10 / 52 | Extract [ecr](https://github.com/crystal-lang-tools/tree-sitter-ecr) corpus inputs (1 corpus files). |
| Edge | 1 / 7 | Extract [edge](https://github.com/Hexacker/tree-sitter-edge) corpus inputs (2 corpus files). |
| EDI X12 | 1 / 1,489 | Extract [x12](https://github.com/hugginsio/tree-sitter-x12) corpus inputs (5 corpus files). |
| Elle | 0 / 0 | [Compiler and language tests](https://github.com/acquitelol/elle). |
| Elsa | 0 / 0 | Extract [elsa](https://github.com/MrPoloGit/tree-sitter-elsa) corpus inputs (1 corpus files). |
| Exograph | 0 / 0 | [Inspect upstream examples/tests](https://github.com/exograph/exograph). |
| Ferret | 0 / 0 | Extract [ferret](https://github.com/Ferret-Language/tree-sitter-ferret) corpus inputs (1 corpus files). |
| Ferret Lockfile | 0 / 0 | [Inspect upstream examples/tests](https://github.com/Ferret-Language/Ferret). |
| Ferret Manifest | 0 / 0 | [Inspect upstream examples/tests](https://github.com/Ferret-Language/Ferret). |
| Firebase Rules | 20 / 591 | [Inspect upstream examples/tests](https://github.com/firebase/quickstart-testing). |
| FlatBuffers | 6 / 364 | [Upstream source/examples/tests](https://github.com/google/flatbuffers). |
| FlatZinc | 0 / 0 | Extract [minizinc](https://github.com/shackle-rs/shackle) corpus inputs (10 corpus files). |
| Fluent | 22 / 107 | Extract [fluent](https://github.com/YouKnow-sys/tree-sitter-fluent) corpus inputs (15 corpus files). |
| Fountain | 0 / 0 | Extract [fountain](https://github.com/LaPingvino/tree-sitter-fountain) corpus inputs (4 corpus files). |
| Freemarker | 22 / 107 | Extract [freemarker](https://github.com/debba/tree-sitter-freemarker) corpus inputs (1 corpus files). |
| FreeStyleWiki | 0 / 0 | Extract [fswiki](https://github.com/blank71/tree-sitter-fswiki) corpus inputs (13 corpus files). |
| FSH | 0 / 0 | [Inspect upstream examples/tests](https://github.com/FHIR/sushi). |
| FSM | 0 / 0 | Inspect [registered extension](https://codeberg.org/reesericci/zed-extension-fsm.git) examples/docs. |
| GABC | 0 / 0 | Extract [gregorio](https://github.com/AISCGre-BR/tree-sitter-gregorio) corpus inputs (28 corpus files). |
| Genexpr | 0 / 0 | Extract [genexpr](https://github.com/isabelgk/tree-sitter-genexpr) corpus inputs (5 corpus files). |
| Geno | 0 / 0 | Extract [geno](https://github.com/jlyonsmith/tree-sitter-geno) corpus inputs (1 corpus files). |
| Ghostty | 0 / 0 | Use actual Ghostty config paths and preserve context; test path-bearing registrations before interpreting zero filename matches as absence. |
| Git Commit | 3 / 3 | Extract [gitcommit](https://github.com/zed-industries/tree-sitter-git-commit) corpus inputs (2 corpus files). |
| Git Config | 93 / 763 | Extract [git_config](https://github.com/the-mikedavis/tree-sitter-git-config) corpus inputs (1 corpus files). |
| Git Rebase | 3 / 180 | Extract [git_rebase](https://github.com/the-mikedavis/tree-sitter-git-rebase) corpus inputs (1 corpus files). |
| Glimmer (JavaScript) | 37 / 986 | [Upstream source/examples/tests](https://github.com/hashicorp/nomad). |
| Glimmer (TypeScript) | 27 / 904 | Extract [glimmer_typescript](https://github.com/NullVoxPopuli/tree-sitter-glimmer-typescript) corpus inputs (5 corpus files). |
| GN | 1 / 10 | [Linguist labelled samples](https://github.com/github-linguist/linguist). |
| Go HTML Template | 0 / 0 | Use known template directories in Hugo or other Go applications; filenames alone miss .html templates. |
| Go Text Template | 8 / 12,812 | Extract [gotmpl](https://github.com/ngalaiko/tree-sitter-go-template) corpus inputs (6 corpus files). |
| Go Work | 0 / 0 | Extract [gowork](https://github.com/zed-industries/tree-sitter-go-work) corpus inputs (5 corpus files). |
| Grafana Alloy | 0 / 0 | [Upstream source/examples/tests](https://github.com/grafana/alloy). |
| GreyCat | 0 / 0 | Extract [greycat](https://hub.datathings.com/greycat-oss/tree-sitter-greycat) corpus inputs (17 corpus files). |
| GritQL | 0 / 0 | Extract [gritql](https://github.com/honeycombio/tree-sitter-gritql) corpus inputs (2 corpus files). |
| GritQL Snippet | 0 / 0 | Extract labelled snippets from Grit rule files or documentation; keep the parent rule and byte offsets. |
| GROQ | 0 / 0 | Extract [groq](https://github.com/juice49/tree-sitter-groq) corpus inputs (11 corpus files). |
| GXL | 0 / 0 | Inspect [registered extension](https://github.com/wp-labs/zed-warplabs.git) examples/docs. |
| Haml | 25 / 140 | Extract [haml](https://github.com/vitallium/tree-sitter-haml) corpus inputs (10 corpus files). |
| Helm | 55 / 511 | The registration counts .helmignore, not normal YAML/Go-template charts. Use chart paths and embedded-template boundaries for Helm data. |
| Hera | 0 / 0 | Extract [hera](https://github.com/DanielXMoore/Civet) corpus inputs (3 corpus files). |
| hl7_v2 | 1 / 1,584 | [Inspect upstream examples/tests](https://github.com/hapifhir/hapi-hl7v2). |
| hledger | 33 / 1,577 | Extract [ledger](https://github.com/cbarrete/tree-sitter-ledger) corpus inputs (9 corpus files). |
| hledger-rules | 20 / 591 | [Inspect upstream examples/tests](https://github.com/simonmichael/hledger). |
| Hosts | 3 / 7 | Extract [hosts](https://github.com/vlasikhin/tree-sitter-hosts) corpus inputs (1 corpus files). |
| HP-42S | 0 / 0 | Extract [hp42s](https://codeberg.org/brechanbech/tree-sitter-hp42s) corpus inputs (8 corpus files). |
| HTML + HubL | 0 / 0 | Use HubSpot CMS theme templates; separate embedded HubL from host HTML/CSS with source offsets. |
| http | 3 / 219 | Extract [http](https://github.com/rest-nvim/tree-sitter-http) corpus inputs (4 corpus files). |
| HubL | 0 / 0 | Use HubSpot CMS theme templates; separate embedded HubL from host HTML/CSS with source offsets. |
| Huff | 0 / 0 | Extract [huff](https://github.com/Niraj-Kamdar/tree-sitter-huff) corpus inputs (5 corpus files). |
| HuJSON | 0 / 0 | Extract [hujson](https://github.com/ggfevans/tree-sitter-hujson) corpus inputs (8 corpus files). |
| Hurl | 20 / 203 | [Linguist labelled samples](https://github.com/github-linguist/linguist). |
| HXML | 14 / 101 | Extract [hxml](https://github.com/Frixuu/tree-sitter-hxml) corpus inputs (3 corpus files). |
| Hyprland Config | 0 / 0 | Extract [hyprlang](https://github.com/tree-sitter-grammars/tree-sitter-hyprlang) corpus inputs (1 corpus files). |
| iCal | 0 / 0 | [Inspect upstream examples/tests](https://github.com/icalendar/icalendar). |
| IFC | 0 / 0 | [Inspect upstream examples/tests](https://github.com/IfcOpenShell/IfcOpenShell). |
| Immigrant | 0 / 0 | Inspect [registered extension](https://github.com/deltarocks/zed-immigrant.git) examples/docs. |
| Ink | 4 / 2,214 | Extract [ink](https://github.com/rhizoome/tree-sitter-ink) corpus inputs (3 corpus files). |
| Inko | 0 / 0 | [Rosetta Code labelled tasks](https://github.com/acmeism/RosettaCodeData). |
| ion | 1 / 20 | Extract [ion](https://github.com/tartarughina/tree-sitter-ion) corpus inputs (1 corpus files). |
| ion_schema | 2 / 764 | Extract [ion_schema](https://github.com/tartarughina/tree-sitter-ion-schema) corpus inputs (1 corpus files). |
| ISLE | 2 / 3,203 | [Upstream source/examples/tests](https://github.com/bytecodealliance/wasmtime). |
| Jdl | 0 / 0 | [Inspect upstream examples/tests](https://github.com/jhipster/jdl-samples). |
| Jerry | 0 / 0 | [Compiler and language tests](https://github.com/jeffscottbrown/jerry-lang). |
| JS+ERB | 15 / 154 | Extract [embedded_template](https://github.com/dangh/tree-sitter-embedded-template) corpus inputs (1 corpus files). |
| JSON Lines | 17 / 685 | Extract [json](https://github.com/tree-sitter/tree-sitter-json) corpus inputs (1 corpus files). |
| Jsonnet | 3 / 139 | [Upstream source/examples/tests](https://github.com/grafana/alloy). |
| JSP | 7 / 7 | Extract [jsp](https://github.com/tartarughina/tree-sitter-jsp) corpus inputs (1 corpus files). |
| Just | 40 / 1,623 | Extract [just](https://github.com/IndianBoy42/tree-sitter-just) corpus inputs (5 corpus files). |
| KCL | 0 / 0 | Extract [kcl](https://github.com/kcl-lang/tree-sitter-kcl) corpus inputs (9 corpus files). |
| Kconfig | 1 / 258 | [Upstream source/examples/tests](https://github.com/zephyrproject-rtos/zephyr). |
| Kdl | 20 / 729 | Extract [kdl](https://github.com/tree-sitter-grammars/tree-sitter-kdl) corpus inputs (1 corpus files). |
| Koto | 1 / 4 | Extract [koto](https://github.com/koto-lang/tree-sitter-koto) corpus inputs (13 corpus files). |
| kulala-http | 3 / 219 | [Inspect upstream examples/tests](https://github.com/mistweaverco/kulala.nvim). |
| Latte | 0 / 0 | Extract [latte](https://github.com/josbeir/tree-sitter-latte) corpus inputs (13 corpus files). |
| Ledger | 33 / 1,577 | Extract [ledger](https://github.com/cbarrete/tree-sitter-ledger) corpus inputs (9 corpus files). |
| Leo | 0 / 0 | Extract [leo](https://github.com/MagicGordon/tree-sitter-leo) corpus inputs (2 corpus files). |
| LikeC4 | 0 / 0 | [Inspect upstream examples/tests](https://github.com/likec4/likec4). |
| LilyPond | 0 / 0 | [Rosetta Code labelled tasks](https://github.com/acmeism/RosettaCodeData). |
| Lini | 0 / 0 | Inspect [registered extension](https://github.com/monfa-red/lini) examples/docs. |
| Liquid | 3 / 9 | Extract [liquid](https://github.com/hankthetank27/tree-sitter-liquid) corpus inputs (5 corpus files). |
| Lisette | 0 / 0 | Extract [lisette](https://github.com/ivov/lisette) corpus inputs (6 corpus files). |
| Literate Haskell | 3 / 69 | Extract [haskell_literate](https://github.com/LaurentRDC/tree-sitter-haskell-literate) corpus inputs (1 corpus files). |
| Lox | 0 / 0 | [Inspect upstream examples/tests](https://github.com/munificent/craftinginterpreters). |
| Mach | 0 / 0 | Extract [mach](https://github.com/briar-systems/mach-tree-sitter) corpus inputs (5 corpus files). |
| Mako | 0 / 0 | Extract [mako](https://github.com/sbaldasty/tree-sitter-mako) corpus inputs (14 corpus files). |
| Marko | 0 / 0 | [Linguist labelled samples](https://github.com/github-linguist/linguist). |
| mcfunction | 0 / 0 | Extract [mcfunction--rockide-language-server](https://github.com/rockide/tree-sitter-mcfunction) corpus inputs (1 corpus files). |
| MetaScript | 6 / 1,759 | Extract [metascript](https://github.com/metascriptlang/tree-sitter-metascript) corpus inputs (4 corpus files). |
| microScript | 6 / 1,759 | Extract [microscript](https://github.com/Nascir/tree-sitter-microscript) corpus inputs (6 corpus files). |
| Minecraft Function | 0 / 0 | Extract [mcfunction--rockide-language-server](https://github.com/rockide/tree-sitter-mcfunction) corpus inputs (1 corpus files). |
| Minecraft Lang | 2 / 216 | Extract [lang](https://github.com/rockide/tree-sitter-lang) corpus inputs (4 corpus files). |
| MiniZinc | 0 / 0 | [Rosetta Code labelled tasks](https://github.com/acmeism/RosettaCodeData). |
| MJML | 9 / 114 | Extract [html--html-jinja](https://github.com/JaagupAverin/tree-sitter-html) corpus inputs (1 corpus files). |
| MLIR | 0 / 0 | Extract [mlir](https://github.com/felixtensor/tree-sitter-mlir) corpus inputs (14 corpus files). |
| Modelfile | 0 / 0 | Extract [modelfile](https://github.com/jackwsmth/tree-sitter-modelfile) corpus inputs (6 corpus files). |
| MoJu | 0 / 0 | Extract [moju](https://github.com/dayu-sec/tree-sitter-moju) corpus inputs (5 corpus files). |
| Nautilus | 0 / 0 | Extract [nautilus](https://github.com/ndr-lmnc/tree-sitter-nautilus) corpus inputs (7 corpus files). |
| Navi | 0 / 0 | Extract [navi](https://github.com/navi-language/tree-sitter-navi) corpus inputs (8 corpus files). |
| Navi Stream | 0 / 0 | Extract [navi_stream](https://github.com/navi-language/tree-sitter-navi-stream) corpus inputs (3 corpus files). |
| Nginx | 7 / 565 | Extract [nginx](https://gitlab.com/joncoole/tree-sitter-nginx) corpus inputs (5 corpus files). |
| Nickel | 2 / 8 | Extract [nickel](https://github.com/nickel-lang/tree-sitter-nickel) corpus inputs (22 corpus files). |
| Nim Format String | 0 / 0 | Injected syntax within Nim strings; extract string content with offsets from real Nim programs or grammar fixtures, rather than searching for standalone files. |
| niva | 0 / 0 | [Inspect upstream examples/tests](https://github.com/gavr123456789/Niva). |
| Nomad Job | 0 / 0 | [Upstream source/examples/tests](https://github.com/hashicorp/nomad). |
| NSIS | 4 / 624 | [Rosetta Code labelled tasks](https://github.com/acmeism/RosettaCodeData). |
| Numscript | 0 / 0 | [Inspect upstream examples/tests](https://github.com/formancehq/numscript). |
| Nunjucks | 4 / 28 | Extract [nunjucks](https://github.com/stormwarning/tree-sitter-nunjucks) corpus inputs (4 corpus files). |
| Oat | 0 / 0 | Inspect [registered extension](https://github.com/WhySoBad/zed-oat-extension.git) examples/docs. |
| OCaml MLX | 3 / 0 | Extract [ocaml_mlx](https://github.com/ocaml-mlx/tree-sitter-mlx) corpus inputs (12 corpus files). |
| Odoc | 42 / 187 | Extract [odoc_mld](https://github.com/manenko/tree-sitter-odoc-mld) corpus inputs (20 corpus files). |
| OML | 0 / 0 | Inspect [registered extension](https://github.com/wp-labs/zed-warplabs.git) examples/docs. |
| OMNeT++ NED | 0 / 0 | Extract [ned](https://github.com/omnetpp/tree-sitter-ned) corpus inputs (1 corpus files). |
| OpenFGA | 0 / 0 | Extract [fga](https://github.com/matoous/tree-sitter-fga) corpus inputs (7 corpus files). |
| OpenTofu Vars | 20 / 578 | [Upstream source/examples/tests](https://github.com/hashicorp/nomad). |
| OpenType Feature | 0 / 0 | Extract [fea](https://github.com/mishamyrt/tree-sitter-opentype-fea) corpus inputs (4 corpus files). |
| Path of Exile Filter | 2 / 286 | [Inspect upstream examples/tests](https://github.com/NeverSinkDev/NeverSink-Filter). |
| PDLL | 0 / 0 | Extract [pdll](https://github.com/felixtensor/tree-sitter-pdll) corpus inputs (7 corpus files). |
| Pdxinfo | 0 / 0 | Extract [pdxinfo](https://github.com/notpeter/tree-sitter-pdxinfo) corpus inputs (1 corpus files). |
| Perm | 0 / 0 | Extract [perm](https://github.com/theoriginalstove/tree-sitter-perm) corpus inputs (1 corpus files). |
| Pest | 4 / 519 | Extract [pest](https://github.com/pest-parser/tree-sitter-pest) corpus inputs (1 corpus files). |
| pica200 | 0 / 0 | Extract [pica200](https://github.com/Squareheron942/tree-sitter-pica200) corpus inputs (5 corpus files). |
| Pine Script | 1 / 41 | [Inspect upstream examples/tests](https://github.com/everget/tradingview-pinescript-indicators). |
| PIO Assembly | 27 / 1,766 | [Inspect upstream examples/tests](https://github.com/raspberrypi/pico-examples). |
| Pkl | 3 / 123 | Extract [pkl](https://github.com/apple/tree-sitter-pkl) corpus inputs (661 corpus files). |
| PlantUML | 9 / 653 | Extract [plantuml](https://github.com/Szeliga/tree-sitter-plantuml) corpus inputs (2 corpus files). |
| POD | 3 / 5,772 | [Linguist labelled samples](https://github.com/github-linguist/linguist). |
| Polar | 0 / 0 | Extract [polar](https://github.com/osohq/tree-sitter-polar) corpus inputs (6 corpus files). |
| Poryscript | 0 / 0 | [Inspect upstream examples/tests](https://github.com/huderlem/poryscript). |
| Praia | 0 / 0 | [Inspect upstream examples/tests](https://github.com/praia-lang/praia). |
| Prisma | 11 / 270 | Extract [prisma](https://github.com/victorhqc/tree-sitter-prisma) corpus inputs (8 corpus files). |
| Pug | 27 / 929 | Extract [pug](https://github.com/zealot128/tree-sitter-pug) corpus inputs (13 corpus files). |
| Puppet | 3 / 79 | Extract [puppet](https://github.com/tree-sitter-grammars/tree-sitter-puppet) corpus inputs (1 corpus files). |
| Python constraints | 2 / 194 | Extract [requirements](https://github.com/tree-sitter-grammars/tree-sitter-requirements) corpus inputs (2 corpus files). |
| Python requirements | 67 / 853 | [Upstream source/examples/tests](https://github.com/zephyrproject-rtos/zephyr). |
| Qlik | 0 / 0 | Extract [qlik](https://github.com/bintocher/zed-qlik-tree-sitter) corpus inputs (6 corpus files). |
| Quarkdown | 0 / 0 | Extract [quarkdown](https://github.com/kinten108101/tree-sitter-quarkdown) corpus inputs (14 corpus files). |
| Quarto | 0 / 0 | Extract [markdown](https://github.com/zed-industries/tree-sitter-markdown) corpus inputs (14 corpus files). |
| Rainbow TSV (⭲) | 7 / 346 | Extract [tsv](https://github.com/coroa/rainbow-csv-tree-sitter) corpus inputs (4 corpus files). |
| RASI | 0 / 0 | Extract [rasi](https://github.com/Fymyte/tree-sitter-rasi) corpus inputs (4 corpus files). |
| RBS | 0 / 0 | Extract [rbs](https://github.com/joker1007/tree-sitter-rbs) corpus inputs (7 corpus files). |
| RCL | 0 / 0 | Extract [rcl](https://github.com/rcl-lang/tree-sitter-rcl) corpus inputs (6 corpus files). |
| Regedit | 0 / 0 | [Inspect upstream examples/tests](https://github.com/wine-mirror/wine). |
| rego | 3 / 99 | Extract [rego](https://github.com/FallenAngel97/tree-sitter-rego) corpus inputs (7 corpus files). |
| Rhai | 0 / 0 | Extract [rhai](https://github.com/elkowar/tree-sitter-rhai) corpus inputs (1 corpus files). |
| Risor | 0 / 0 | Extract [risor](https://github.com/applejag/tree-sitter-risor) corpus inputs (16 corpus files). |
| Robot | 1 / 143 | Extract [robot](https://github.com/Hubro/tree-sitter-robot) corpus inputs (10 corpus files). |
| robots.txt | 54 / 415 | Extract [robots_txt](https://github.com/opa-oz/tree-sitter-robots-txt) corpus inputs (1 corpus files). |
| RON | 6 / 135 | Extract [ron](https://github.com/zee-editor/tree-sitter-ron) corpus inputs (3 corpus files). |
| Roto | 0 / 0 | Extract [roto](https://github.com/NLnetLabs/tree-sitter-roto) corpus inputs (3 corpus files). |
| RsHtml | 16 / 350 | Inspect [registered extension](https://github.com/rshtml/zed.git) examples/docs. |
| Rux | 0 / 0 | [Inspect upstream examples/tests](https://github.com/rux-lang/Rux). |
| SageMath | 0 / 0 | [Rosetta Code labelled tasks](https://github.com/acmeism/RosettaCodeData). |
| SASS | 37 / 389 | Extract [sass](https://github.com/bajrangCoder/tree-sitter-sass) corpus inputs (2 corpus files). |
| Sieve | 0 / 0 | Extract [sieve](https://github.com/aRustyDev/tree-sitter-sieve) corpus inputs (1 corpus files). |
| SilverStripe | 5 / 12,240 | Extract [silverstripe](https://github.com/nicolas-cusan/tree-sitter-silverstripe) corpus inputs (5 corpus files). |
| Simula | 0 / 0 | [Rosetta Code labelled tasks](https://github.com/acmeism/RosettaCodeData). |
| Skir | 0 / 0 | Extract [skir](https://github.com/sporto/tree-sitter-skir) corpus inputs (1 corpus files). |
| Skript | 0 / 0 | Extract [skript](https://github.com/DaisyCatTs/SkriptZed) corpus inputs (3 corpus files). |
| Slang | 2 / 157 | Extract [slang](https://github.com/tree-sitter-grammars/tree-sitter-slang) corpus inputs (2 corpus files). |
| Slim | 11 / 136 | Extract [slim](https://github.com/kolen/tree-sitter-slim) corpus inputs (8 corpus files). |
| Smithy | 7 / 340 | Extract [smithy](https://github.com/indoorvivants/tree-sitter-smithy) corpus inputs (1 corpus files). |
| snakemake | 2 / 87 | Extract [snakemake](https://github.com/osthomas/tree-sitter-snakemake) corpus inputs (9 corpus files). |
| Soma | 0 / 0 | [Compiler and language tests](https://github.com/SrGaabriel/soma). |
| SOQL | 0 / 0 | Extract [soql](https://github.com/aheber/tree-sitter-sfapex) corpus inputs (54 corpus files). |
| SOSL | 0 / 0 | Extract [sosl](https://github.com/aheber/tree-sitter-sfapex) corpus inputs (54 corpus files). |
| Souffle | 0 / 0 | Extract [souffle](https://github.com/langston-barrett/tree-sitter-souffle) corpus inputs (11 corpus files). |
| SpiceDB | 0 / 0 | Extract [authzed](https://github.com/mleonidas/tree-sitter-authzed) corpus inputs (4 corpus files). |
| spthy | 0 / 0 | [Inspect upstream examples/tests](https://github.com/tamarin-prover/tamarin-prover). |
| Stan Functions | 0 / 0 | Extract [stanfunctions](https://github.com/WardBrian/tree-sitter-stan) corpus inputs (7 corpus files). |
| Statamic Antlers | 0 / 0 | Extract [antlers](https://github.com/eugene-karuna/tree-sitter-antlers) corpus inputs (10 corpus files). |
| Strace | 3 / 1,087 | Extract [strace](https://github.com/sigmaSd/tree-sitter-strace) corpus inputs (1 corpus files). |
| Structurizr DSL | 1 / 66 | Extract [structurizr](https://github.com/sinon/tree-sitter-structurizr) corpus inputs (7 corpus files). |
| Surreal Query Language | 0 / 0 | Extract [surrealql](https://github.com/ce11an/tree-sitter-surrealql) corpus inputs (9 corpus files). |
| SysML v2 | 0 / 0 | Extract [sysml](https://gitlab.com/nomograph/tree-sitter-sysml) corpus inputs (15 corpus files). |
| SystemRDL | 0 / 0 | Extract [systemrdl](https://github.com/alex-torregrosa/tree-sitter-systemrdl) corpus inputs (2 corpus files). |
| TableGen | 2 / 1,439 | Extract [tablegen](https://github.com/felixtensor/tree-sitter-tablegen) corpus inputs (7 corpus files). |
| Taskfile | 1 / 349 | Extract [yaml--taskfile](https://github.com/tree-sitter-grammars/tree-sitter-yaml) corpus inputs (6 corpus files). |
| Templ | 0 / 0 | Extract [templ](https://github.com/vrischmann/tree-sitter-templ) corpus inputs (9 corpus files). |
| Tera | 4 / 215 | Extract [tera](https://github.com/uncenter/tree-sitter-tera) corpus inputs (3 corpus files). |
| Tera (CSS) | 0 / 0 | Use the appropriate host-format templates from Tera fixtures. A generic Tera corpus does not prove each host-format variant is represented. |
| Tera (HTML) | 2 / 20 | Use the appropriate host-format templates from Tera fixtures. A generic Tera corpus does not prove each host-format variant is represented. |
| Tera (JSON) | 0 / 0 | Use the appropriate host-format templates from Tera fixtures. A generic Tera corpus does not prove each host-format variant is represented. |
| Tera (TOML) | 0 / 0 | Use the appropriate host-format templates from Tera fixtures. A generic Tera corpus does not prove each host-format variant is represented. |
| Tera (XML) | 0 / 0 | Use the appropriate host-format templates from Tera fixtures. A generic Tera corpus does not prove each host-format variant is represented. |
| Tera (YAML) | 0 / 0 | Use the appropriate host-format templates from Tera fixtures. A generic Tera corpus does not prove each host-format variant is represented. |
| Terraform Vars | 20 / 578 | [Upstream source/examples/tests](https://github.com/hashicorp/nomad). |
| Textproto | 3 / 285 | [Upstream source/examples/tests](https://github.com/cel-expr/cel-spec). |
| TL-B | 0 / 0 | [Inspect upstream examples/tests](https://github.com/ton-blockchain/ton). |
| TLA+ | 3 / 162 | Extract [tlaplus](https://github.com/tlaplus-community/tree-sitter-tlaplus) corpus inputs (52 corpus files). |
| tmux | 0 / 0 | Extract [tmux](https://github.com/Freed-Wu/tree-sitter-tmux) corpus inputs (19 corpus files). |
| Todo | 3 / 148 | Inspect [registered extension](https://github.com/cseelus/plaintasks-zed.git) examples/docs. |
| TOON | 0 / 0 | Extract [toon](https://github.com/3swordman/tree-sitter-toon) corpus inputs (15 corpus files). |
| TQL | 12 / 46 | Extract [tql](https://github.com/tenzir/tree-sitter-tql) corpus inputs (15 corpus files). |
| TSRX | 0 / 0 | Extract [tsrx](https://github.com/tsrx-org/tsrx) corpus inputs (6 corpus files). |
| Turtle | 0 / 0 | Extract [turtle](https://github.com/GordianDziwis/tree-sitter-turtle) corpus inputs (2 corpus files). |
| Txtar | 0 / 0 | [Upstream source/examples/tests](https://github.com/grafana/alloy). |
| Typespec | 0 / 0 | [Upstream source/examples/tests](https://github.com/microsoft/typespec). |
| TyranoScript | 0 / 0 | Extract [tyranoscript](https://github.com/void2610/tree-sitter-tyranoscript) corpus inputs (1 corpus files). |
| Uiua | 0 / 0 | [Rosetta Code labelled tasks](https://github.com/acmeism/RosettaCodeData). |
| Umka | 0 / 0 | [Compiler and language tests](https://github.com/vtereshkov/umka-lang). |
| Umple | 0 / 0 | [Compiler and language tests](https://github.com/umple/umple). |
| Ungrammar | 4 / 27 | Extract [ungrammar](https://github.com/tree-sitter-grammars/tree-sitter-ungrammar) corpus inputs (1 corpus files). |
| Unison | 6 / 18 | [Rosetta Code labelled tasks](https://github.com/acmeism/RosettaCodeData). |
| URDF | 0 / 0 | Extract [xml](https://github.com/tree-sitter-grammars/tree-sitter-xml) corpus inputs (5 corpus files). |
| USD | 0 / 0 | Extract [usd](https://github.com/ColinKennedy/tree-sitter-usd) corpus inputs (25 corpus files). |
| UTL | 0 / 0 | Extract [utl](https://github.com/JekRock/tree-sitter-utl) corpus inputs (5 corpus files). |
| vCard | 0 / 0 | Extract [vcard](https://github.com/TitouanReal/tree-sitter-vcard) corpus inputs (7 corpus files). |
| Vento | 0 / 0 | Extract [vento](https://github.com/ventojs/tree-sitter-vento) corpus inputs (3 corpus files). |
| Veryl | 0 / 0 | [Compiler and language tests](https://github.com/veryl-lang/veryl). |
| VEX | 0 / 0 | [Inspect upstream examples/tests](https://github.com/jtomori/vex_tutorial). |
| VHS | 1 / 99 | Extract [vhs](https://github.com/charmbracelet/tree-sitter-vhs) corpus inputs (4 corpus files). |
| Vibescript | 0 / 0 | Extract [vibescript](https://github.com/mgomes/tree-sitter-vibescript) corpus inputs (19 corpus files). |
| ViewTree ($mol) | 0 / 0 | [Inspect upstream examples/tests](https://github.com/hyoo-ru/mam_mol). |
| VRL | 0 / 0 | Extract [vrl](https://github.com/belltoy/tree-sitter-vrl) corpus inputs (40 corpus files). |
| WDL | 0 / 0 | Extract [wdl](https://github.com/broadinstitute/tree-sitter-wdl) corpus inputs (4 corpus files). |
| WebAssembly Text Format | 10 / 286 | [Upstream source/examples/tests](https://github.com/bytecodealliance/wasmtime). |
| WeiXin Markup Language | 0 / 0 | Extract [wxml](https://github.com/BlockLune/tree-sitter-wxml) corpus inputs (20 corpus files). |
| WFG | 0 / 0 | Extract [wfl](https://github.com/wp-labs/tree-sitter-wfl) corpus inputs (2 corpus files). |
| WFL | 0 / 0 | Extract [wfl](https://github.com/wp-labs/tree-sitter-wfl) corpus inputs (2 corpus files). |
| WFS | 0 / 0 | Inspect [registered extension](https://github.com/wp-labs/zed-warplabs.git) examples/docs. |
| Whim | 0 / 0 | Extract [whim](https://github.com/carthage-software/tree-sitter-whim) corpus inputs (7 corpus files). |
| whkd | 0 / 0 | Extract [whkd](https://github.com/LGUG2Z/tree-sitter-whkd) corpus inputs (1 corpus files). |
| Wikitext | 15 / 1,226 | Extract [wikitext](https://github.com/santhoshtr/tree-sitter-wikitext) corpus inputs (13 corpus files). |
| WIT | 1 / 40 | [Upstream source/examples/tests](https://github.com/bytecodealliance/wasmtime). |
| WoW TOC | 1 / 36 | Inspect [registered extension](https://github.com/Alexayy/zed-wow-toc.git) examples/docs. |
| WPL | 0 / 0 | Inspect [registered extension](https://github.com/wp-labs/zed-warplabs.git) examples/docs. |
| XDR Syntax Highlight | 0 / 0 | Inspect [registered extension](https://github.com/algebnaly/xdr.zed.git) examples/docs. |
| xmake | 2 / 96 | Extract [lua--lua](https://github.com/tree-sitter-grammars/tree-sitter-lua) corpus inputs (4 corpus files). |
| XQuery | 0 / 0 | [Rosetta Code labelled tasks](https://github.com/acmeism/RosettaCodeData). |
| YAML+ERB | 4 / 968 | Extract [embedded_template](https://github.com/dangh/tree-sitter-embedded-template) corpus inputs (1 corpus files). |
| YANG | 0 / 0 | Extract [yang](https://github.com/Hubro/tree-sitter-yang) corpus inputs (1 corpus files). |
| Yara | 1 / 28 | [Linguist labelled samples](https://github.com/github-linguist/linguist). |
| Yarn Spinner | 5 / 57 | [Inspect upstream examples/tests](https://github.com/YarnSpinnerTool/YarnSpinner). |
| Yuck | 0 / 0 | Extract [yuck](https://github.com/tree-sitter-grammars/tree-sitter-yuck) corpus inputs (1 corpus files). |
| Yul | 0 / 0 | Extract [yul](https://github.com/czepluch/tree-sitter-yul) corpus inputs (9 corpus files). |
| Yulang | 0 / 0 | [Compiler and language tests](https://github.com/momota1029/yulang). |
| ziggy | 1 / 8 | [Inspect upstream examples/tests](https://github.com/kristoff-it/ziggy). |
| ziggy-schema | 2 / 230 | [Inspect upstream examples/tests](https://github.com/kristoff-it/ziggy). |
| ZoKrates | 0 / 0 | Extract [zokrates](https://github.com/threonyl/tree-sitter-zokrates) corpus inputs (2 corpus files). |
| zwirn | 0 / 0 | Inspect [registered extension](https://codeberg.org/polymorphicengine/zwirn-zed-extension.git) examples/docs. |
