import argparse
import importlib.machinery
import importlib.util
import json
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from dev_worker import source_hash, stage_source

loader = importlib.machinery.SourceFileLoader('corpus_dev', str(Path(__file__).with_name('dev')))
specification = importlib.util.spec_from_loader(loader.name, loader)
dev = importlib.util.module_from_spec(specification)
loader.exec_module(dev)


class DevelopmentTests(unittest.TestCase):
    def test_lsp_initialize_does_not_expose_host_pid_to_server(self):
        message = {'jsonrpc':'2.0', 'id':1, 'method':'initialize',
                   'params':{'processId':12345, 'rootUri':'file:///project'}}
        body = json.dumps(message).encode()
        following = b'Content-Length: 2\r\n\r\n{}'
        source = io.BytesIO(b'Content-Length: '+str(len(body)).encode()+b'\r\n\r\n'+body+following)
        output = io.BytesIO()
        dev.relay_lsp_input(source, output)
        header, payload = output.getvalue().split(b'\r\n\r\n', 1)
        length = int(header.split(b':')[1])
        message['params']['processId'] = None
        self.assertEqual(json.loads(payload[:length]), message)
        self.assertEqual(payload[length:], following)

    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)

    def test_staged_inputs_include_untracked_edits_and_keep_links_inside_snapshot(self):
        source = self.root/'source'
        source.mkdir()
        (source/'grammar.js').write_text('first')
        (source/'.git').mkdir()
        (source/'.git/config').write_text('not a build input')
        (source/'linked').symlink_to(source/'grammar.js')
        destination = self.root/'staged'
        stage_source(source, destination)
        original = source_hash(destination)
        self.assertFalse((destination/'.git').exists())
        (source/'grammar.js').write_text('second')
        self.assertEqual((destination/'linked').read_text(), 'first')
        (source/'untracked.h').write_text('new input')
        stage_source(source, destination)
        self.assertNotEqual(source_hash(destination), original)
        self.assertEqual((destination/'linked').read_text(), 'second')
        self.assertEqual((destination/'untracked.h').read_text(), 'new input')

    def test_source_and_artifact_links_cannot_escape(self):
        source = self.root/'source'
        source.mkdir()
        (self.root/'outside').write_text('outside')
        (source/'escape').symlink_to(self.root/'outside')
        with self.assertRaises(ValueError):
            stage_source(source, self.root/'staged')
        self.assertFalse((self.root/'staged').exists())
        with self.assertRaises(ValueError):
            dev.publish(source, self.root/'current')
        self.assertFalse((self.root/'current').exists())

    def test_override_replacement_keeps_previous_output_and_target_locks(self):
        first, second = self.root/'first', self.root/'second'
        first.mkdir()
        second.mkdir()
        (first/'parser.so').write_text('old')
        (second/'parser.so').write_text('new')
        target = self.root/'current'
        dev.publish(first, target)
        dev.publish(second, target)
        self.assertEqual((target/'parser.so').read_text(), 'new')
        self.assertEqual((first/'parser.so').read_text(), 'old')
        with dev.locked(self.root/'lock'):
            with self.assertRaises(RuntimeError):
                with dev.locked(self.root/'lock'):
                    self.fail('concurrent writer acquired lock')

    def test_profile_applies_matching_grammar_and_requires_every_server_override(self):
        state = self.root/'state'
        extension = state/'extensions/example'
        (extension/'grammars').mkdir(parents=True)
        (extension/'extension.toml').write_text('id="example"\nversion="1.0"\n[grammars.example]\n[language_servers.example-lsp]\n')
        (extension/'grammars/example.wasm').write_bytes(b'original')
        override = state/'overrides/grammars/example'
        override.mkdir(parents=True)
        (override/'parser.wasm').write_bytes(b'edited')
        (override/'artifact.json').write_text('{"source_sha256":"edited"}')
        project = self.root/'project'
        project.mkdir()
        server_map = self.root/'servers.json'
        server_map.write_text(json.dumps({'example-lsp': {'repository':'example-server',
                                'executable':'example', 'arguments':['--stdio']}}))
        arguments = argparse.Namespace(extension=['example'], server_map=server_map,
                                       server_image='image', project=project)
        def select(filename, *unused):
            return {'grammars':['grammars/example']} if filename == 'zed-sources.toml' else {'grammar':'example'}
        with patch.object(dev, 'select', side_effect=select), patch.object(dev, 'image_id', return_value='a'*64):
            dev.prepare_profile(arguments, state)
            installed = state/'zed-profile/extensions/installed/example'
            self.assertTrue(installed.is_symlink())
            self.assertEqual((installed/'grammars/example.wasm').read_bytes(), b'edited')
            self.assertEqual((extension/'grammars/example.wasm').read_bytes(), b'original')
            settings_path = state/'zed-profile/config/settings.json'
            settings = json.loads(settings_path.read_text())
            self.assertEqual(settings['lsp']['example-lsp']['binary']['path'], str(state/'launchers/example-lsp'))
            self.assertFalse(settings['auto_update_extensions']['example'])
            self.assertFalse(settings['auto_install_extensions']['html'])
            self.assertEqual(settings['granted_extension_capabilities'], [])
            server_map.write_text('{"unrelated":{}}')
            with self.assertRaisesRegex(ValueError, 'Missing explicit launch'):
                dev.prepare_profile(arguments, state)
            self.assertEqual(json.loads(settings_path.read_text()), settings)


if __name__ == '__main__':
    unittest.main()
