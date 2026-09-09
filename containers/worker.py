#!/usr/bin/env python3
"""Untrusted build/test worker: this file runs INSIDE an isolated container."""
import argparse
import ctypes
import hashlib
import json
import os
from pathlib import Path
import re
import resource
import shutil
import subprocess
import sys


def run(args, **kwargs):
    print('+', ' '.join(map(str, args)), flush=True)
    subprocess.run(list(map(str, args)), check=True, **kwargs)


def build_grammar(job, source_root=Path('/input/source'), work=Path('/work/build'), output=Path('/out')):
    source = source_root / job.get('directory', '')
    parser = source / 'src/parser.c'
    text = parser.read_text()
    symbols = re.findall(r'\b(tree_sitter_\w+)\s*\(\s*(?:void)?\s*\)', text)
    symbols = sorted(set(s for s in symbols if 'external_scanner' not in s))
    if len(symbols) != 1:
        raise ValueError(f'Expected one parser entry point, found {symbols}')
    work.mkdir(parents=True)
    includes = ['-I', source/'src', '-I', source, '-I', source_root]
    flags = ['-O2', '-fPIC', '-fno-omit-frame-pointer']
    run(['gcc', '-std=c11', *flags, *includes, '-c', parser, '-o', work/'parser.o'])
    objects = [work/'parser.o']
    linker = 'gcc'
    scanners = [p for p in (source/'src').glob('scanner.*') if p.suffix in ('.c', '.cc', '.cpp', '.cxx')]
    # Some projects retain an old C++ scanner alongside its C replacement.
    if source.joinpath('src/scanner.c') in scanners:
        scanners = [source/'src/scanner.c']
    for n, scanner in enumerate(scanners):
        compiler = 'gcc' if scanner.suffix == '.c' else 'g++'
        if compiler == 'g++': linker = compiler
        obj = work/f'scanner{n}.o'
        run([compiler, *flags, *includes, '-c', scanner, '-o', obj])
        objects.append(obj)
    target = output/'parser.so'
    run([linker, '-shared', '-Wl,-z,defs', *objects, '-o', target])
    meta = dict(job, symbol=symbols[0], sha256=hashlib.sha256(target.read_bytes()).hexdigest())
    (output/'artifact.json').write_text(json.dumps(meta, indent=2)+'\n')
    run(['/opt/corpus/python/bin/python', '/opt/corpus/worker.py', 'smoke-grammar', str(output)])
    for pattern in ('LICENSE*', 'COPYING*', 'NOTICE*'):
        for path in source_root.glob(pattern):
            if path.is_file() and not path.is_symlink(): shutil.copyfile(path, output/path.name)


def smoke_grammar(directory):
    # Bound parser bugs independently of the compiler's larger memory allowance.
    resource.setrlimit(resource.RLIMIT_AS, (512*1024*1024, 512*1024*1024))
    resource.setrlimit(resource.RLIMIT_CPU, (10, 10))
    from tree_sitter import Language, Parser
    directory = Path(directory)
    meta = json.loads((directory/'artifact.json').read_text())
    lib = ctypes.CDLL(str(directory/'parser.so'))
    fn = getattr(lib, meta['symbol'])
    fn.restype = ctypes.c_void_p
    pointer = fn()
    capsule = ctypes.pythonapi.PyCapsule_New
    capsule.restype = ctypes.py_object
    capsule.argtypes = (ctypes.c_void_p, ctypes.c_char_p, ctypes.c_void_p)
    lang = Language(capsule(pointer, b'tree_sitter.Language', None))
    parser = Parser(lang)
    for sample in (b'', b'hello\n', b'{}\n', b'let x = 1;\n'):
        tree = parser.parse(sample)
        assert tree.root_node is not None
    print(json.dumps({'grammar': meta['name'], 'abi': lang.abi_version, 'smoke': 'passed'}), flush=True)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('action', choices=['build-grammar', 'smoke-grammar', 'exec'])
    p.add_argument('args', nargs='*')
    args = p.parse_args()
    os.makedirs('/work/home', exist_ok=True)
    if args.action == 'build-grammar':
        build_grammar(json.loads(Path(args.args[0]).read_text()))
    elif args.action == 'smoke-grammar': smoke_grammar(args.args[0])
    else: run(args.args)


if __name__ == '__main__': main()
