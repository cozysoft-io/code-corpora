import os
from pathlib import Path
import tempfile
import unittest

from runtime_layers import stage_layers


class RuntimeLayers(unittest.TestCase):
    def test_split_preserves_package_links_and_file_modes(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root/'source'
            (source/'package').mkdir(parents=True)
            (source/'package/a').write_bytes(b'1234')
            (source/'package/a').chmod(0o755)
            (source/'package/b').write_bytes(b'5678')
            (source/'alias').symlink_to('package', target_is_directory=True)
            layers = stage_layers(source, root/'layers', limit=4)
            self.assertEqual(len(layers), 2)
            self.assertTrue((layers[0]/'alias').is_symlink())
            self.assertEqual(os.readlink(layers[0]/'alias'), 'package')
            for layer in layers:
                files = [p for p in layer.rglob('*') if p.is_file() and not p.is_symlink()]
                self.assertLessEqual(sum(p.stat().st_size for p in files), 4)
            self.assertEqual((layers[0]/'package/a').stat().st_mode & 0o777, 0o755)
            self.assertEqual((layers[1]/'package/b').read_bytes(), b'5678')

    def test_escape_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root/'source').mkdir()
            (root/'source/escape').symlink_to('/etc/passwd')
            with self.assertRaises(ValueError): stage_layers(root/'source', root/'layers')


if __name__ == '__main__': unittest.main()
