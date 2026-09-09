"""Check incremental-image integrity without a VM or container execution."""
import importlib.util
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch


class AppendServersTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root/'repo').mkdir()
        (self.root/'images').mkdir()
        (self.root/'repo/selected-servers.toml').write_text(
            '[[repo]]\nname="old"\nsha="old-pin"\n[[repo]]\nname="new"\nsha="new-pin"\n')
        self.records = {}
        for name in ('old', 'new'):
            directory = self.root/'artifacts/servers'/name
            directory.mkdir(parents=True)
            (directory/'server').write_text(name)
            (directory/'server').chmod(0o755)
            record = {'name':name, 'sha':name+'-pin', 'status':'built-unverified',
                      'artifact':{'executables':[{'name':'shared', 'path':'server'}]}}
            (directory/'build.json').write_text(json.dumps(record))
            self.records[name] = record
        self.catalog = [self.records['old'], {'name':'new', 'sha':'new-pin', 'status':'failed'}]
        def atomic_json(path, value):
            path.write_text(json.dumps(value))
        fake = SimpleNamespace(ROOT=self.root, USER=SimpleNamespace(pw_uid=1000, pw_gid=1000),
                               PODMAN=['podman'], atomic_json=atomic_json)
        spec = importlib.util.spec_from_file_location('append_test_assemble', Path(__file__).with_name('assemble.py'))
        self.module = importlib.util.module_from_spec(spec)
        with patch.dict('sys.modules', {'build_grammars':fake}):
            spec.loader.exec_module(self.module)
        self.calls = []
        def call(arguments):
            self.calls.append(arguments)
            if arguments[:2] == ['podman', 'cp']:
                Path(arguments[-1]).write_text(json.dumps(self.catalog))
        self.call_patch = patch.object(self.module, 'call', call)
        self.call_patch.start()
        self.addCleanup(self.call_patch.stop)
        def inspect(arguments, **kwargs):
            return 'a'*64 if '--format={{.Id}}' in arguments else json.dumps([{'Id':'b'*64}])
        self.inspect_patch = patch.object(self.module.subprocess, 'check_output', inspect)
        self.inspect_patch.start()
        self.addCleanup(self.inspect_patch.stop)

    def test_adds_only_new_artifacts_and_removes_ambiguous_launchers(self):
        self.module.append_servers('base', 'repaired')
        context = next((self.root/'images').iterdir())
        self.assertEqual([path.name for path in (context/'servers').iterdir()], ['new'])
        self.assertEqual(list((context/'bin').iterdir()), [])
        containerfile = (context/'Containerfile').read_text()
        self.assertTrue(containerfile.startswith('FROM '+'a'*64+'\n'))
        self.assertIn('RUN rm -rf /opt/corpus/bin', containerfile)
        catalog = {row['name']:row for row in json.loads((context/'server-catalog.json').read_text())}
        self.assertEqual(catalog, self.records)

    def test_rejects_replacement_of_existing_distribution(self):
        path = self.root/'artifacts/servers/old/build.json'
        record = dict(self.records['old'], image='different-build')
        path.write_text(json.dumps(record))
        with self.assertRaisesRegex(ValueError, 'Base distribution changed'):
            self.module.append_servers('base', 'repaired')
        self.assertFalse(any(command[:2] == ['podman', 'build'] for command in self.calls))

    def test_rejects_stale_base_pin(self):
        self.catalog[0] = dict(self.catalog[0], sha='obsolete')
        with self.assertRaisesRegex(ValueError, 'selected server commit'):
            self.module.append_servers('base', 'repaired')


if __name__ == '__main__':
    unittest.main()
