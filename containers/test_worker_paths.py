"""Test the path boundary without running the sandbox worker entry point."""
import ast
import os
from pathlib import Path
import shutil
import tempfile
import unittest

# The worker deliberately reads its job and starts immediately inside a container.
# Load only its pure filesystem helper for these host-side fixture tests.
module = ast.parse(Path(__file__).with_name('server_worker.py').read_text())
function = next(node for node in module.body if isinstance(node, ast.FunctionDef) and node.name == 'copy_runtime_tree')
namespace = {'Path': Path, 'os': os, 'shutil': shutil}
exec(compile(ast.Module(body=[function], type_ignores=[]), '<worker path helper>', 'exec'), namespace)
copy_runtime_tree = namespace['copy_runtime_tree']


class RuntimePathsTest(unittest.TestCase):
    def test_internal_absolute_links_survive_removing_build_tree(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source, output = root/'source', root/'output'
            (source/'nested').mkdir(parents=True)
            (source/'data').write_text('runtime data')
            (source/'nested/absolute').symlink_to(source/'data')
            (source/'nested/relative').symlink_to('../data')
            copy_runtime_tree(source, output)
            shutil.rmtree(source)
            self.assertFalse(Path(os.readlink(output/'nested/absolute')).is_absolute())
            self.assertEqual((output/'nested/absolute').read_text(), 'runtime data')
            self.assertEqual((output/'nested/relative').read_text(), 'runtime data')

    def test_escaping_links_are_rejected_before_copy(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root/'source'
            source.mkdir()
            (root/'private').write_text('outside the artifact')
            (source/'escape').symlink_to('../private')
            with self.assertRaisesRegex(ValueError, 'escapes package'):
                copy_runtime_tree(source, root/'output')
            self.assertFalse((root/'output').exists())


if __name__ == '__main__':
    unittest.main()
