import fcntl
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from import_servers import import_one, validate


class ImportTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.source = self.root/'incoming/example'
        self.source.mkdir(parents=True)
        (self.source/'server').write_bytes(b'compiled executable')
        (self.source/'server').chmod(0o755)
        self.selection = {'example': {'sha':'a'*40}}
        self.artifact = dict(name='example', sha='a'*40, selected_sha='a'*40,
                             source_head='a'*40, builder_image='b'*64,
                             executables=[{'name':'server', 'path':'server'}],
                             hashes={'server':hashlib.sha256(b'compiled executable').hexdigest()})
        (self.source/'artifact.json').write_text(json.dumps(self.artifact))

    def test_import_records_origin_and_preserves_failure(self):
        job = self.root/'jobs/server-example'
        job.mkdir(parents=True)
        (job/'result.json').write_text('{"status":"failed"}')
        import_one(self.source, self.root, self.selection)
        record = json.loads((self.root/'artifacts/servers/example/build.json').read_text())
        self.assertEqual(record['build_origin'], 'local-rootless-podman')
        self.assertEqual(record['artifact'], self.artifact)
        self.assertEqual(json.loads(next(job.glob('result-before-*.json')).read_text()), {'status':'failed'})
        with self.assertRaises(FileExistsError): import_one(self.source, self.root, self.selection)

    def test_wrong_pin_and_modified_bytes_are_rejected(self):
        with self.assertRaises(ValueError): validate(self.source, {'example':{'sha':'c'*40}})
        (self.source/'server').write_bytes(b'changed')
        with self.assertRaises(ValueError): import_one(self.source, self.root, self.selection)
        self.assertFalse((self.root/'artifacts/servers/example').exists())

    def test_unlisted_files_and_escaping_links_are_rejected(self):
        extra = self.source/'extra'
        extra.write_bytes(b'unlisted')
        with self.assertRaises(ValueError): validate(self.source, self.selection)
        extra.unlink()
        extra.symlink_to('/etc/passwd')
        with self.assertRaises(ValueError): validate(self.source, self.selection)

    def test_active_build_lock_is_respected(self):
        locks = self.root/'jobs/.locks'
        locks.mkdir(parents=True)
        with (locks/'example.lock').open('w') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            with self.assertRaises(BlockingIOError): import_one(self.source, self.root, self.selection)
        self.assertFalse((self.root/'artifacts/servers/example').exists())


if __name__ == '__main__': unittest.main()
