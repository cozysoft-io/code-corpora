# Repository selection

`selected-repos.toml` owns the repository choices, immutable commits, and splits.
Its opening comments preserve the original selection criteria and split history.
The rationale comes from heuristic-jump's `design/data-collection.md`, section 1.
This document makes the process usable without that checkout.

The current pass is in [`repo-selection.md`](repo-selection.md). Its
[`JSON audit`](repo-selection.json) freezes the coverage baseline and records
candidate snapshots, source scopes, exceptions, and unresolved languages.

## Which languages need repositories

Use `language-coverage.json` to identify languages with at most 20 UTF-8 files
**or** fewer than 2,000 raw lines across training and test combined. Freeze these
baseline measurements for a selection pass. Recounting after each addition would
make the order of selection determine which languages get considered.
Earlier selection audits retain their original 50-file threshold.

The coverage census includes hidden and ignored files. Its counts identify gaps;
they do not establish that a repository contains useful handwritten source.
Shared suffixes are also ambiguous: `.cls`, for example, does not establish that
a file contains Apex. Check the actual language before selecting a repository.

For this expansion, select one training and one test repository per programming
language. Focus on source with named definitions and references: calls, imports,
types, variables, modules, or equivalent constructs. Configuration and data
formats are deferred. Their incidental coverage can grow as programming-language
repositories are fetched. Record deferrals explicitly; do not count them as
completed repository selections.

Aliases and companion source syntaxes can use the same pair when both projects
contain the required files. A repository can cover several languages, but it has
one split and one checkout. A compiler written in another language qualifies only
through substantial source in the target language, not through its implementation
language, parser tables, or a handful of syntax fixtures.

## Choosing candidates

1. Start with maintained applications, libraries, and self-hosted language tools.
   Prefer established projects with independent users. Record the source of each
   candidate, its purpose, maintenance evidence, and license. Popularity is useful
   evidence, not a replacement for checking the source.
   Mature legacy implementations can qualify with an explicit maintenance
   exception; do not describe an archived project as actively maintained.
2. Prefer **20,000–200,000 target-language lines**. Smaller projects do not exercise
   whole-project search latency well; larger ones can make server indexing
   dominate collection. Record a specific size exception when a useful project
   falls outside that band. Small libraries can still exercise correctness, but
   should not stand in for a latency workload.
3. Inspect the source at an immutable commit. Count matching UTF-8 files and raw
   lines, including comments and blanks. Separate implementation source from
   tests, examples, tutorials, generated code, vendored dependencies, and build
   outputs. Retain paths that substantiate the target-language classification.
4. Prefer mostly handwritten production code. Reject tutorial collections,
   benchmark-only projects, forks duplicating another candidate, and repositories
   whose target-language content is only parser fixtures. A repository name or
   GitHub language label alone is insufficient evidence.
5. Choose varied projects: different maintainers and domains where possible,
   ideally an application and a library. Check repository identity and ancestry
   against the existing corpus and the other selections before assigning splits.
   Do not put a fork or another checkout of training code into test.
6. Record all candidates considered and the reason for selection or rejection.
   If two suitable independent repositories cannot be established, record the
   unresolved gap. Do not invent a second project or silently substitute grammar
   fixtures for real source.

Archive measurements used during selection are identified as such. They are not
`corpus-lock.toml` measurements: upstream archive export rules can omit tracked
files. `./corpus clone` measures the actual selected checkout separately.

The expansion's candidate ledger is `repo-selection.json`; the original
`[[considered]]` entries remain historical evidence. Distinguish rejected
candidates from unqualified discovery results. An unsuccessful search does not
establish that no suitable repository exists.

Scoped counts exclude known fixtures, generated code, vendored libraries and
copied files. These filters are conservative screening, not semantic proof that
every retained line is handwritten implementation. The recorded source paths
and exact-copy check make that screening reviewable; near copies and fetched
dependencies still need review before evaluation.

## Pinning and split rules

- Assign `train` or `test` before using a project to tune heuristic-jump.
- A repository that has been used for training must never move to test.
- Preserve existing pins. A replacement gets a new entry; the old entry is
  retired rather than repinned or deleted.
- Reuse an existing repository's pin and split if it supplies another language.
- Keep selection inspection separate from heuristic development and scoring.
  Inspecting a candidate to establish its language, size, or build procedure is
  part of selection, not permission to tune against its held-out answers.

For each selected project, retain its URL, full commit SHA, split, language
coverage, domain, source measurements, selection rationale, size exceptions, and
dependency setup notes. Keep per-language decisions so a shared repository does
not hide an unfilled language pair.

New manifest entries declare `path_suffixes`, `coverage_languages`, and selection
language identifiers in `languages`. These identifiers enable CLI filtering;
they do not register a heuristic-jump handler or promise an LSP language ID.
`evaluation_source_roots` and `evaluation_exclude_paths`, where present, describe
the intended source scope. The JSON audit also records the common exclusion
pattern. Fetching preserves whole repositories; downstream evaluation must
apply this scope before approving readiness.

## Readiness for heuristic-jump evaluation

RosettaCodeData is an explicit example-collection exception to the production
source and paired-repository criteria above. The entire pinned collection stays
in training. Its canonical source tree is `Task/`; `Lang/` is an alternate view.
Language directory labels guide source review because some export suffixes are
guessed. Selection evidence is in [`DATA-PROPOSALS.md`](DATA-PROPOSALS.md).

Selecting and pinning source does not establish an LSP oracle. Before collecting
ground truth, the language needs a grammar, a supported heuristic-jump handler,
and a usable language server or a separately specified reference oracle.

Install the project's dependencies and configure its build. Examples include a
populated module cache, the correct virtual environment, or a compile database
whose entries refer to the current checkout. Check that the pinned checkout is
clean and that build artifacts refer to its current path.

Then sample imports or equivalent cross-file references and require the server
to resolve every probe. Investigate each miss. Fix the setup, replace the
candidate, or document a specific unavoidable exception such as a platform-only
dependency. A successful build or a server that answers same-file queries does
not prove that cross-file resolution works.

Record readiness independently of source selection. Projects with unverified
dependencies or unsupported languages must not be presented as ready for ground
truth collection. Do not run heuristic-jump scoring to decide which repositories
to select: that would select for the behavior being measured.
