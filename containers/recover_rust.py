#!/usr/bin/env python3
"""Recover the selected Rust parser from its same-SHA published crate."""
import hashlib
import json
from pathlib import Path
import tarfile
import tempfile
import urllib.request

root = Path('/srv/corpus/repo')
url = 'https://crates.io/api/v1/crates/tree-sitter-rust/0.24.2/download'
checksum = '439e577dbe07423ec2582ac62c7531120dbfccfa6e5f92406f93dd271a120e45'
rows = json.loads((root/'grammar-inputs.json').read_text())
row = next(r for r in rows if r['name'] == 'rust')
with tempfile.TemporaryDirectory() as tmp:
    archive = Path(tmp)/'rust.crate'
    urllib.request.urlretrieve(url, archive)
    assert hashlib.sha256(archive.read_bytes()).hexdigest() == checksum
    with tarfile.open(archive) as tar:
        info = json.load(tar.extractfile('tree-sitter-rust-0.24.2/.cargo_vcs_info.json'))
        assert info['git']['sha1'] == row['sha'], 'Crate does not match the selected SHA'
        tar.extractall(Path(tmp)/'source', filter='data')
    destination = root/'grammars/rust'
    if destination.exists(): raise RuntimeError('Rust source already staged')
    import shutil
    shutil.copytree(Path(tmp)/'source/tree-sitter-rust-0.24.2', destination)
row.update(status='staged', source_archive=url, source_archive_sha256=checksum,
           source_provenance='Published crate .cargo_vcs_info matches selected Git SHA; source is a crate-packaged subset')
(root/'grammar-inputs.json').write_text(json.dumps(rows, indent=2)+'\n')
print(json.dumps(row))
