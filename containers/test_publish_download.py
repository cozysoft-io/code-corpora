"""Verify signed downloads without credentials or network access."""
import ast
import copy
import hashlib
import io
from pathlib import Path
import tempfile
import unittest
import urllib.parse
import urllib.request
from unittest.mock import patch


class SignedDownloadTest(unittest.TestCase):
    def setUp(self):
        tree = ast.parse((Path(__file__).parent/'publisher/publish.py').read_text())
        function = next(node for node in tree.body if isinstance(node, ast.FunctionDef)
                        and node.name == 'download_signed_archive')
        namespace = {'hashlib':hashlib, 'urllib':urllib}
        exec(compile(ast.Module(body=[function], type_ignores=[]), 'publish.py', 'exec'), namespace)
        self.download = namespace['download_signed_archive']
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.archive = Path(self.temporary.name)/'image.tar'
        self.spec = {'archive_url':'https://storage.googleapis.com/bucket/image?signature=secret',
                     'sha256':hashlib.sha256(b'abcde').hexdigest(),
                     'parts':[{'bytes':len(part), 'sha256':hashlib.sha256(part).hexdigest()}
                              for part in (b'abc', b'de')]}

    def run_download(self, contents, spec=None):
        response = io.BytesIO(contents)
        response.status = 200
        with patch.object(urllib.request, 'urlopen', return_value=response):
            self.download(spec or self.spec, self.archive)

    def test_validates_multiple_chunks_and_whole_archive(self):
        self.run_download(b'abcde')
        self.assertEqual(self.archive.read_bytes(), b'abcde')
        spec = copy.deepcopy(self.spec)
        spec['sha256'] = '0'*64
        with self.assertRaisesRegex(ValueError, 'Archive checksum'):
            self.run_download(b'abcde', spec)

    def test_rejects_corruption_truncation_and_extra_bytes(self):
        for contents in (b'abcXe', b'abcd', b'abcdef'):
            with self.subTest(contents=contents), self.assertRaises(ValueError):
                self.run_download(contents)

    def test_rejects_other_endpoints_without_network_access(self):
        spec = dict(self.spec, archive_url='http://169.254.169.254/')
        with patch.object(urllib.request, 'urlopen') as request, self.assertRaises(ValueError):
            self.download(spec, self.archive)
        request.assert_not_called()

    def test_does_not_disclose_signed_url_in_errors(self):
        with patch.object(urllib.request, 'urlopen', side_effect=RuntimeError(self.spec['archive_url'])):
            with self.assertRaises(RuntimeError) as error:
                self.download(self.spec, self.archive)
        self.assertNotIn('signature', str(error.exception))
        self.assertTrue(error.exception.__suppress_context__)


if __name__ == '__main__':
    unittest.main()
