"""Pinned fetching, selection migration, and preservation tests using local Git."""
import argparse
import contextlib
import importlib.machinery
import importlib.util
import io
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import tomllib
import unittest
from unittest.mock import patch

TOOL = Path(__file__).with_name("corpus")
loader = importlib.machinery.SourceFileLoader("corpus_tool", str(TOOL))
spec = importlib.util.spec_from_loader(loader.name, loader)
corpus = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = corpus
loader.exec_module(corpus)


class CorpusTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.upstream = self.root / "upstream"
        self.upstream.mkdir()
        self.git("init", "-q")
        self.git("config", "user.name", "Corpus Test")
        self.git("config", "user.email", "corpus@example.invalid")
        (self.upstream / "Main.java").write_text("pinned\n")
        self.git("add", ".")
        self.git("commit", "-qm", "pin")
        self.sha = self.git("rev-parse", "HEAD")
        self.repo = dict(name="example", language="java", split="train",
                         url=self.upstream.as_uri(), domain="test", sha=self.sha)
        self.pin = dict(self.repo, sha=self.sha, branch="main", lines=1,
                        lines_nonblank=1, source_files=1, tracked_files=1,
                        clone=corpus.CLONE_STYLE, added="2026-09-08")
        self.pin.pop("domain")
        self.target = self.root / "checkouts"

    def git(self, *args):
        return corpus.git(*args, cwd=self.upstream).strip()

    def args(self, **kwargs):
        return argparse.Namespace(directory=self.target, language=None, split=None,
                                  repo=None, jobs=2, **kwargs)

    def test_training_filter_alias_selects_train_paths(self):
        selection = corpus.Selection(self.target, {}, [self.repo], [], [])
        arguments = self.args()
        arguments.split = "training"
        self.assertEqual(corpus.selected(selection, arguments), [self.repo])
        self.assertEqual(corpus.checkout_path(self.target, self.repo), self.target / "train" / "example")

    def test_pin_is_fetched_even_when_upstream_advances_and_local_edits_survive(self):
        (self.upstream / "Main.java").write_text("newer\n")
        self.git("commit", "-qam", "advance")
        cloned = corpus.clone_one(self.target, self.repo, self.pin)
        self.assertEqual(cloned.problems, [])
        self.assertEqual(cloned.entry, self.pin)
        checkout = corpus.checkout_path(self.target, self.repo)
        self.assertEqual((checkout / "Main.java").read_text(), "pinned\n")
        self.assertEqual(corpus.git("rev-parse", "--abbrev-ref", "HEAD", cwd=checkout).strip(), "HEAD")
        self.assertEqual(corpus.verify_one(self.target, self.repo, self.pin), [])
        (checkout / "Main.java").write_text("local edit\n")
        (checkout / "untracked").write_text("keep me\n")
        self.assertEqual(corpus.clone_one(self.target, self.repo, self.pin).entry, self.pin)
        self.assertTrue(any("dirty:" in p for p in corpus.verify_one(self.target, self.repo, self.pin)))
        different = dict(self.pin, sha=self.git("rev-parse", "HEAD"))
        self.assertTrue(corpus.clone_one(self.target, self.repo, different).problems)
        self.assertEqual((checkout / "Main.java").read_text(), "local edit\n")
        self.assertEqual((checkout / "untracked").read_text(), "keep me\n")

    def test_failed_clone_cleans_only_its_own_staging_directory(self):
        destination = corpus.checkout_path(self.target, self.repo)
        unrelated = destination.with_name("example.partial")
        unrelated.mkdir(parents=True)
        (unrelated / "keep").write_text("other invocation\n")
        result = corpus.clone_one(self.target, self.repo, dict(self.pin, sha="0" * 40))
        self.assertTrue(result.problems)
        self.assertEqual(list(destination.parent.iterdir()), [unrelated])
        destination.mkdir()
        (destination / "keep").write_text("not a checkout\n")
        self.assertIn("not a checkout", corpus.clone_one(self.target, self.repo, self.pin).problems[0])
        self.assertTrue((destination / "keep").exists())

    def test_filtered_clone_preserves_complete_lock_and_uses_flat_paths(self):
        second = dict(self.repo, name="second")
        selection = corpus.Selection(self.target, {"size_lines": [1, 10]},
                                     [self.repo, second], [], [])
        lock = {corpus.key_of(self.repo): self.pin,
                corpus.key_of(second): dict(self.pin, name="second")}
        lock_path = self.root / "corpus-lock.toml"
        args = self.args()
        args.repo = ["example"]
        with patch.object(corpus, "LOCK", lock_path), patch.object(corpus, "load_selection", return_value=selection):
            corpus.write_lock(selection, lock)
            original = lock_path.read_bytes()
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(corpus.command_clone(args), 0)
                self.assertEqual(corpus.command_status(args), 0)
                args.repo = None
                self.assertEqual(corpus.command_status(args), 1)
                args.repo = ["example"]
                self.assertEqual(corpus.command_verify(args), 0)
            self.assertTrue((self.target / "train" / "example" / ".git").exists())
            self.assertFalse(corpus.checkout_path(self.target, second).exists())
            self.assertFalse((self.target / "train" / "java").exists())
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(corpus.command_clone(args), 0)
            self.assertEqual(lock_path.read_bytes(), original)

    def test_selected_sha_is_fetched_without_a_lock_and_measured_once(self):
        selection = corpus.Selection(self.target, {"size_lines": [1, 10]}, [self.repo], [], [])
        (self.upstream / "Main.java").write_text("new HEAD before first clone\n")
        self.git("commit", "-qam", "advance before clone")
        with patch.object(corpus, "LOCK", self.root / "lock.toml"), patch.object(corpus, "load_selection", return_value=selection):
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(corpus.command_clone(self.args()), 0)
            original = corpus.load_lock()
            pin = original[corpus.key_of(self.repo)]
            self.assertEqual((pin["sha"], pin["lines"], pin["source_files"]), (self.sha, 1, 1))
            (self.upstream / "Main.java").write_text("upstream changed\nmore\n")
            self.git("commit", "-qam", "advance")
            shutil.rmtree(corpus.checkout_path(self.target, self.repo))
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(corpus.command_clone(self.args()), 0)
            self.assertEqual(corpus.load_lock(), original)
            self.assertEqual((corpus.checkout_path(self.target, self.repo) / "Main.java").read_text(), "pinned\n")

    def test_selection_and_measurements_preserve_all_repositories(self):
        selection = corpus.load_selection()
        lock = corpus.load_lock()
        self.assertEqual(len(selection.repos), 256)
        self.assertEqual(len(lock), 256)
        self.assertEqual({r["language"] for r in selection.repos}, set(corpus.EXTENSIONS))
        self.assertEqual(len(selection.considered), 248)
        self.assertEqual(len(selection.reserves), 14)
        corpus.validate_measurements(selection, lock)
        paths = [corpus.checkout_path(self.target, repo) for repo in selection.repos]
        self.assertEqual(len(set(paths)), len(paths))
        self.assertTrue(all(len(path.relative_to(self.target).parts) == 2 for path in paths))

    def test_invalid_paths_duplicates_and_pins_are_rejected(self):
        path = self.root / "selection.toml"
        prefix = 'corpus_root = "."\n[criteria]\nsize_lines = [1, 10]\n'
        with patch.object(corpus, "SELECTION", path), contextlib.redirect_stderr(io.StringIO()):
            for repos in ([dict(self.repo, name="../escape")], [self.repo, self.repo], [self.repo, dict(self.repo, language="rust")],
                          [dict(self.repo, url="--bad-url")], [dict(self.repo, sha="main")],
                          [{k: v for k, v in self.repo.items() if k != "sha"}]):
                path.write_text(prefix + "\n".join("\n".join(corpus.emit_table("repo", repo)) for repo in repos))
                with self.assertRaises(SystemExit):
                    corpus.load_selection()
        with patch.object(corpus, "LOCK", path), contextlib.redirect_stderr(io.StringIO()):
            for pins in ([dict(self.pin, sha="not-a-pin")], [self.pin, self.pin]):
                path.write_text("\n".join("\n".join(corpus.emit_table("repo", pin)) for pin in pins))
                with self.assertRaises(SystemExit):
                    corpus.load_lock()

    def test_cli_is_independent_of_working_directory_and_validates_jobs(self):
        fixture = self.root / "fixture"
        fixture.mkdir()
        shutil.copy2(TOOL, fixture / "corpus")
        (fixture / "selected-repos.toml").write_text(
            'corpus_root = "."\n[criteria]\nsize_lines = [1, 10]\n' +
            "\n".join(corpus.emit_table("repo", self.repo)) + "\n")
        run = subprocess.run([str(fixture / "corpus"), "clone", "--repo", "example"],
                             cwd=self.root, capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        self.assertTrue(corpus.checkout_path(fixture, self.repo).is_dir())
        self.assertTrue((fixture / "corpus-lock.toml").exists())
        run = subprocess.run([str(fixture / "corpus"), "clone", "--jobs", "0"],
                             cwd=self.root, capture_output=True, text=True)
        self.assertEqual(run.returncode, 2)
        self.assertIn("--jobs must be positive", run.stderr)

    def test_conflicting_lock_cannot_override_selected_sha(self):
        selection = corpus.Selection(self.target, {"size_lines": [1, 10]}, [self.repo], [], [])
        lock = {corpus.key_of(self.repo): dict(self.pin, sha="0" * 40)}
        with patch.object(corpus, "load_selection", return_value=selection), \
                patch.object(corpus, "load_lock", return_value=lock), \
                contextlib.redirect_stderr(io.StringIO()):
            for command in (corpus.command_clone, corpus.command_status, corpus.command_verify):
                with self.assertRaises(SystemExit):
                    command(self.args())
        self.assertFalse(self.target.exists())

    def test_status_and_verify_use_selection_without_measurements(self):
        selection = corpus.Selection(self.target, {"size_lines": [1, 10]}, [self.repo], [], [])
        self.assertFalse(corpus.clone_one(self.target, self.repo, None).problems)
        with patch.object(corpus, "load_selection", return_value=selection), \
                patch.object(corpus, "load_lock", return_value={}), \
                contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(corpus.command_status(self.args()), 0)
            self.assertEqual(corpus.command_verify(self.args()), 0)

    def test_recursive_clone_skips_optional_sources_and_explicit_opt_in_works(self):
        fixture = self.root / "source-fixture"
        fixture.mkdir()

        def git(*args):
            return corpus.git(*args, cwd=fixture)

        git("init", "-q")
        git("config", "user.name", "Corpus Test")
        git("config", "user.email", "corpus@example.invalid")
        modules = [("reference", "zed", False), ("reference", "zed-extensions", False),
                   ("data", "lsp-data", False)]
        configs, tables = [], []
        for kind, path, active in modules:
            entry = dict(path=path, sha=self.sha, url=self.upstream.as_uri(), active=active)
            tables += corpus.emit_table(kind, entry)
            configs += [f'[submodule "{path}"]', f'path = {path}',
                        f'url = {entry["url"]}', f'active = {str(active).lower()}',
                        f'update = {"checkout" if active else "none"}']
            git("update-index", "--add", "--cacheinfo", f"160000,{self.sha},{path}")
        (fixture / ".gitmodules").write_text("\n".join(configs) + "\n")
        (fixture / "zed-sources.toml").write_text("\n".join(tables) + "\n")
        git("add", ".gitmodules", "zed-sources.toml")
        git("commit", "-qm", "sources")
        clone = self.root / "recursive-clone"
        git("-c", "protocol.file.allow=always", "clone", "-q", "--recurse-submodules",
            str(fixture), str(clone))
        self.assertFalse((clone / "zed-extensions/.git").exists())
        self.assertFalse((clone / "lsp-data/.git").exists())
        self.assertFalse((clone / "zed/.git").exists())
        args = argparse.Namespace(check=False, path=None, data=False, references=False, jobs=2)
        with patch.object(corpus, "REPO", clone), \
                patch.object(corpus, "SOURCES", clone / "zed-sources.toml"), \
                patch.dict(os.environ, {"GIT_CONFIG_COUNT": "1",
                                       "GIT_CONFIG_KEY_0": "protocol.file.allow",
                                       "GIT_CONFIG_VALUE_0": "always"}):
            sources = corpus.source_modules()
            with patch.object(corpus, "source_modules", return_value=sources), \
                    patch.object(corpus.subprocess, "run") as run, \
                    contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(corpus.command_submodules(args), 0)
                run.assert_not_called()
            args.references = True
            self.assertEqual(corpus.command_submodules(args), 0)
            self.assertTrue((clone / "zed-extensions/.git").exists())
            self.assertFalse((clone / "lsp-data/.git").exists())
            self.assertTrue((clone / "zed/.git").exists())
            args.path = ["lsp-data"]
            self.assertEqual(corpus.command_submodules(args), 0)
            self.assertTrue((clone / "lsp-data/.git").exists())
            self.assertTrue((clone / "zed/.git").exists())
            source = clone / "zed-sources.toml"
            source.write_text(source.read_text().replace(self.sha, "0" * 40, 1))
            with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                corpus.source_modules()

    def test_source_inventory_and_all_selection_pins_are_consistent(self):
        selection = corpus.load_selection()
        corpus.validate_measurements(selection, corpus.load_lock())
        document, modules = corpus.source_modules()
        self.assertEqual(len(document["extension"]), document["registry_extensions"])
        self.assertEqual({entry["name"] for entry in document["grammar"]} & set(corpus.EXTENSIONS),
                         set(corpus.EXTENSIONS) - {"csharp"})  # upstream calls it c_sharp
        self.assertEqual({entry["path"] for entry in modules}, {"zed", "zed-extensions", "lsp-data"})
        paths = {entry["path"] for kind in ("grammar", "server") for entry in document[kind]}
        self.assertIn("grammars/csharp", paths)
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(corpus.command_sources(argparse.Namespace(write=False)), 0)
        unavailable = {entry["extension"] for entry in document["unavailable_server"]}
        for entry in document["extension"] + document["bundled_extension"]:
            self.assertTrue(set(entry.get("grammars", [])) <= paths)
            self.assertTrue(set(entry.get("server_repositories", [])) <= paths)
            if entry.get("language_servers"):
                self.assertTrue(entry.get("server_repositories") or entry["id"] in unavailable,
                                entry["id"])

    def test_toml_sources_clone_exact_pin_preserve_edits_and_validate_names(self):
        for kind in ("grammars", "servers"):
            entry = dict(name="example", url=self.upstream.as_uri(), sha=self.sha)
            path = self.root / f"selected-{kind}.toml"
            path.write_text("\n".join(corpus.emit_table("repo", entry)))
            args = self.args(command="clone", set=kind)
            with patch.object(corpus, "REPO", self.root), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(corpus.command_clone(args), 0)
                checkout = self.target / kind / "example"
                self.assertTrue((checkout / ".git").is_dir())
                self.assertFalse((self.root / "corpus-lock.toml").exists())
                (checkout / "Main.java").write_text("local edit\n")
                self.assertEqual(corpus.command_clone(args), 0)
                args.command = "status"
                self.assertEqual(corpus.command_status(args), 0)
                args.command = "verify"
                self.assertEqual(corpus.command_verify(args), 1)
                self.assertEqual((checkout / "Main.java").read_text(), "local edit\n")
                args.repo = ["nonexistent"]
                with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                    corpus.command_status(args)
                path.write_text("\n".join(corpus.emit_table("repo", dict(entry, name="../escape"))))
                with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                    corpus.load_sources(kind)



if __name__ == "__main__":
    unittest.main()
