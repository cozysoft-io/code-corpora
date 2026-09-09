#!/usr/bin/env python3
"""Count UTF-8 corpus files using the pinned Zed language registrations."""

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tarfile
import tempfile
import tomllib
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parent
CACHE = ROOT / ".corpus" / "language-configs"
MINIMUM_FILES = 21
MINIMUM_LINES = 2000
# RosettaCodeData exports use these longer extensions.
SUFFIX_ALIASES = {"Arturo": ["arturo"], "Uiua": ["uiua"], "Simula": ["simula"]}


def read_extension(extension):
    url = extension.get("fetch_url", extension["url"])
    sha = extension["sha"]
    directory = extension.get("directory", "").strip("/")
    key = hashlib.sha256(f"{url}@{sha}:{directory}".encode()).hexdigest()
    cached = CACHE / f"{key}.json"
    if cached.exists():
        return json.loads(cached.read_text())
    files = {}
    parsed = urllib.parse.urlparse(url)
    if parsed.netloc == "github.com":
        repository = parsed.path.removesuffix(".git").strip("/")
        address = f"https://codeload.github.com/{repository}/tar.gz/{sha}"
        with urllib.request.urlopen(address, timeout=90) as response:
            with tarfile.open(fileobj=response, mode="r|gz") as archive:
                for member in archive:
                    relative = member.name.partition("/")[2]
                    if member.isfile() and relative.endswith(("config.toml", "extension.toml", "extension.json")):
                        files[relative] = archive.extractfile(member).read().decode("utf-8-sig")
    else:
        with tempfile.TemporaryDirectory(dir=CACHE) as temporary:
            for command in (["init", "-q"], ["fetch", "--depth", "1", url, sha]):
                subprocess.run(["git", "-C", temporary, *command], check=True,
                               capture_output=True, timeout=180)
            paths = subprocess.check_output(
                ["git", "-C", temporary, "ls-tree", "-r", "--name-only", "FETCH_HEAD"], text=True)
            for relative in paths.splitlines():
                if relative.endswith(("config.toml", "extension.toml", "extension.json")):
                    files[relative] = subprocess.check_output(
                        ["git", "-C", temporary, "show", f"FETCH_HEAD:{relative}"]).decode("utf-8-sig")
    prefix = directory + "/" if directory else ""
    manifest_path = prefix + "extension.toml"
    if manifest_path in files:
        manifest = tomllib.loads(files[manifest_path])
        explicit = {prefix + path.rstrip("/") + "/config.toml"
                    for path in manifest.get("languages", [])}
    elif prefix + "extension.json" in files:
        explicit = set()
    else:
        raise ValueError(f"missing extension manifest in {directory or '.'}")
    configs = {}
    for path, contents in sorted(files.items()):
        relative = path.removeprefix(prefix)
        if path in explicit or (path.startswith(prefix + "languages/")
                                and len(relative.split("/")) == 3
                                and relative.endswith("/config.toml")):
            configs[path] = tomllib.loads(contents)
    missing = explicit - configs.keys()
    if missing:
        raise ValueError(f"missing language configs: {sorted(missing)}")
    cached.write_text(json.dumps(configs, indent=2) + "\n")
    return configs


def registration(config, source, path, sha):
    return dict(name=config["name"], grammar=config.get("grammar"),
                path_suffixes=config.get("path_suffixes", []),
                first_line_pattern=config.get("first_line_pattern"),
                source=source, path=path, sha=sha)


def inventory(document, jobs):
    CACHE.mkdir(parents=True, exist_ok=True)
    registrations = []
    errors = []
    reference = next(row for row in document["reference"] if row["path"] == "zed")
    sha = reference["sha"]
    paths = subprocess.check_output(
        ["git", "-C", str(ROOT / "zed"), "ls-tree", "-r", "--name-only", sha], text=True)
    for path in paths.splitlines():
        if path.endswith("/config.toml") and (
                path.startswith("crates/grammars/src/") or
                any(path.startswith(row["source"].removeprefix("zed/").rsplit("/", 1)[0] + "/languages/")
                    for row in document["bundled_extension"] if row["id"] != "zed/test-extension")):
            contents = subprocess.check_output(
                ["git", "-C", str(ROOT / "zed"), "show", f"{sha}:{path}"], text=True)
            registrations.append(registration(tomllib.loads(contents), "zed", path, sha))
    # These two built-in registrations are constructed in Rust rather than config.toml.
    for name, grammar, suffix in [("Plain Text", None, "txt"), ("Git Commit", "gitcommit", "COMMIT_EDITMSG")]:
        registrations.append(registration(dict(name=name, grammar=grammar, path_suffixes=[suffix]),
                                          "zed", "crates/languages/src/lib.rs" if grammar else
                                          "crates/language/src/language.rs", sha))
    extensions = document["extension"]
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        futures = {pool.submit(read_extension, extension): extension for extension in extensions}
        for completed, future in enumerate(as_completed(futures), 1):
            extension = futures[future]
            try:
                configs = future.result()
                for path, config in configs.items():
                    registrations.append(registration(config, extension["id"], path, extension["sha"]))
            except Exception as error:
                details = str(error)
                if isinstance(error, subprocess.CalledProcessError) and error.stderr:
                    details = error.stderr.decode("utf-8", errors="replace").strip()
                errors.append(dict(source=extension["id"], url=extension["url"],
                                   sha=extension["sha"], error=details))
                print(f"unavailable {extension['id']}: {details}", flush=True)
            if completed % 100 == 0 or completed == len(extensions):
                print(f"read {completed}/{len(extensions)} extensions", flush=True)
    return sorted(registrations, key=lambda row: (row["name"].casefold(), row["source"], row["path"])), sorted(errors, key=lambda row: row["source"])


def language_suffixes(registration):
    return set(registration["path_suffixes"]) | set(SUFFIX_ALIASES.get(registration["name"], []))


def matching_suffixes(relative, suffixes):
    filename = relative.rsplit("/", 1)[-1]
    candidates = {relative, filename, filename.rsplit(".", 1)[-1]}
    candidates.update(relative[index + 1:] for index, character in enumerate(relative) if character == ".")
    return candidates & suffixes


def count_split(directory, suffixes):
    if not directory.is_dir():
        raise FileNotFoundError(directory)
    counts = {suffix: dict(files=0, lines=0, invalid_utf8=0) for suffix in sorted(suffixes)}
    groups = {}
    total = dict(files=0, lines=0, invalid_utf8=0, unmatched_files=0, symlinks_skipped=0)
    errors = []
    for parent, directories, filenames in os.walk(directory):
        for name in directories[:]:
            if name == ".git" or (Path(parent) / name).is_symlink():
                directories.remove(name)
        for name in filenames:
            path = Path(parent) / name
            if name == ".git":
                continue
            if path.is_symlink():
                total["symlinks_skipped"] += 1
                continue
            matches = matching_suffixes(path.relative_to(directory).as_posix(), suffixes)
            if not matches:
                total["unmatched_files"] += 1
                continue
            try:
                data = path.read_bytes()
                data.decode("utf-8", errors="strict")
            except UnicodeDecodeError:
                total["invalid_utf8"] += 1
                for suffix in matches:
                    counts[suffix]["invalid_utf8"] += 1
                continue
            except OSError as error:
                errors.append(dict(path=str(path), error=str(error)))
                continue
            lines = data.count(b"\n") + int(bool(data) and not data.endswith(b"\n"))
            total["files"] += 1
            total["lines"] += lines
            group = groups.setdefault(tuple(sorted(matches)), dict(files=0, lines=0))
            group["files"] += 1
            group["lines"] += lines
            for suffix in matches:
                counts[suffix]["files"] += 1
                counts[suffix]["lines"] += lines
    return dict(total=total, suffixes=counts,
                match_groups=[dict(suffixes=list(key), **value) for key, value in sorted(groups.items())],
                errors=errors)


def report(document):
    document["suffix_aliases"] = SUFFIX_ALIASES
    suffix_names = {}
    languages = {}
    for row in document["registrations"]:
        language = languages.setdefault(row["name"], dict(suffixes=set(), grammars=set(), sources=set()))
        language["suffixes"].update(language_suffixes(row))
        if row["grammar"]:
            language["grammars"].add(row["grammar"])
        language["sources"].add(row["source"])
        for suffix in language_suffixes(row):
            suffix_names.setdefault(suffix, set()).add(row["name"])
    for name, language in languages.items():
        for split, measurement in document["splits"].items():
            matches = [group for group in measurement["match_groups"]
                       if language["suffixes"].intersection(group["suffixes"])]
            language[split] = {field: sum(group[field] for group in matches) for field in ["files", "lines"]}
        language["below_threshold"] = bool(language["suffixes"]) and (
            sum(language[split]["files"] for split in document["splits"]) < MINIMUM_FILES or
            sum(language[split]["lines"] for split in document["splits"]) < MINIMUM_LINES)
        for field in ["suffixes", "grammars", "sources"]:
            language[field] = sorted(language[field])
    document["languages"] = dict(sorted(languages.items(), key=lambda item: item[0].casefold()))
    document["ambiguous_suffixes"] = {suffix: sorted(names) for suffix, names in sorted(suffix_names.items()) if len(names) > 1}
    lines = ["# Corpus language coverage", "", f"Source snapshot: {document['snapshot_date']}. Regenerate with `python3 corpus_coverage.py`.", "",
             "Files match registered Zed `path_suffixes`, including exact filenames and compound suffixes, "
             "plus aliases `.arturo` (Arturo), `.uiua` (Uiua), and `.simula` (Simula). "
             "Matching is case-sensitive. Only strictly valid UTF-8 files count. Lines include blanks and comments; "
             "a final unterminated line counts once. Empty files count as files with zero lines.", "",
             "The scan includes hidden and ignored files, skips `.git` and symlinks, and scans `training/` "
             "(the `train/` alias) once. First-line patterns and user overrides are not applied. "
             "A file matching several registrations counts toward each language, once per language. "
             "Split totals count each file only once. Shared suffixes indicate possible coverage, not a verified language classification.", "",
             "| Split | UTF-8 files | Raw lines | Rejected non-UTF-8 files | Unmatched files |",
             "| --- | ---: | ---: | ---: | ---: |"]
    for split, measurement in document["splits"].items():
        total = measurement["total"]
        lines.append(f"| {split} | {total['files']:,} | {total['lines']:,} | {total['invalid_utf8']:,} | {total['unmatched_files']:,} |")
    below = sum(language["below_threshold"] for language in languages.values())
    lines += ["", f"{len(document['registrations'])} registrations; {len(languages)} language names; "
              f"{len(suffix_names)} unique suffixes/filenames; {below} languages below {MINIMUM_FILES} files or {MINIMUM_LINES:,} raw lines combined. "
              f"{len(document['unavailable_extensions'])} extension inventories unavailable.", "",
              "Full registrations, pins, per-suffix counts, ambiguities, and failures are in [language-coverage.json](language-coverage.json).", "",
              "| Language | Suffixes / filenames | Training files | Training lines | Test files | Test lines | Below threshold |",
              "| --- | --- | ---: | ---: | ---: | ---: | --- |"]
    for name, language in document["languages"].items():
        suffixes = ", ".join(f"`{suffix.replace('|', '&#124;')}`" for suffix in language["suffixes"]) or "—"
        status = "yes" if language["below_threshold"] else ("no" if language["suffixes"] else "no filename registration")
        training, test = language["training"], language["test"]
        lines.append(f"| {name.replace('|', '&#124;')} | {suffixes} | {training['files']:,} | {training['lines']:,} | {test['files']:,} | {test['lines']:,} | {status} |")
    if document["unavailable_extensions"]:
        lines += ["", "## Unavailable extension inventories", ""]
        lines.extend(f"- `{row['source']}`: {row['error']}" for row in document["unavailable_extensions"])
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh", action="store_true", help="rebuild the inventory from pinned sources (cached downloads reused)")
    parser.add_argument("--jobs", type=int, default=12)
    arguments = parser.parse_args()
    output = ROOT / "language-coverage.json"
    sources = tomllib.loads((ROOT / "zed-sources.toml").read_text())
    source_hash = hashlib.sha256((ROOT / "zed-sources.toml").read_bytes()).hexdigest()
    if output.exists() and not arguments.refresh:
        document = json.loads(output.read_text())
        if document["source_sha256"] != source_hash:
            parser.error("zed-sources.toml changed; use --refresh")
    else:
        registrations, errors = inventory(sources, arguments.jobs)
        document = dict(snapshot_date=sources["snapshot_date"], source_sha256=source_hash,
                        registrations=registrations, unavailable_extensions=errors)
        output.write_text(json.dumps(document, indent=2) + "\n")
    suffixes = {suffix for row in document["registrations"] for suffix in language_suffixes(row)}
    document["registry_extensions"] = len(sources["extension"])
    document["counting"] = dict(encoding="strict UTF-8", lines="LF bytes plus a final unterminated line",
                                hidden_files=True, ignored_files=True, symlinks=False,
                                excluded_directories=[".git"], first_line_patterns=False,
                                threshold=dict(files=MINIMUM_FILES, lines=MINIMUM_LINES, split="combined", operator="or"))
    document["splits"] = {}
    for split in ["training", "test"]:
        directory = ROOT / split
        if split == "training" and not directory.exists():
            directory = ROOT / "train"
        document["splits"][split] = count_split(directory, suffixes)
        print(split, document["splits"][split]["total"], flush=True)
    markdown = report(document)
    output.write_text(json.dumps(document, indent=2) + "\n")
    (ROOT / "language-coverage.md").write_text(markdown)
    print(f"wrote {output.name} and language-coverage.md")


if __name__ == "__main__":
    main()
