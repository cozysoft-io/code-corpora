#!/usr/bin/env python3
"""Probe LSP initialize in the final runtime, never on the host."""
import json
import os
import re
from pathlib import Path
import selectors
import signal
import subprocess
import sys
import tempfile
import time


def probe(command, diagnostic, initialization_options=None):
    # Temporary stderr is bounded by the container's tmpfs; only a short excerpt
    # reaches the report. Keep protocol stdout separate.
    stderr = tempfile.TemporaryFile()
    try:
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=stderr, start_new_session=True)
    except BaseException:
        stderr.close()
        raise
    def send(message):
        data = json.dumps(message).encode()
        process.stdin.write(f'Content-Length: {len(data)}\r\n\r\n'.encode()+data)
        process.stdin.flush()
    selector = selectors.DefaultSelector()
    selector.register(process.stdout, selectors.EVENT_READ)
    buf = b''
    deadline = time.monotonic()+8
    try:
        send({'jsonrpc': '2.0', 'id': 1, 'method': 'initialize', 'params': {
            'processId': None, 'rootUri': 'file:///work/project', 'capabilities': {},
            'initializationOptions': initialization_options or {},
            'workspaceFolders': [{'uri': 'file:///work/project', 'name': 'probe'}]}})
        while time.monotonic() < deadline:
            for key, _ in selector.select(timeout=0.25):
                chunk = os.read(key.fileobj.fileno(), 65536)
                if not chunk: return False
                buf += chunk
                if len(buf) > 4*1024*1024: return False
                while b'\r\n\r\n' in buf:
                    header, body = buf.split(b'\r\n\r\n', 1)
                    length = next((int(line.split(b':',1)[1]) for line in header.split(b'\r\n') if line.lower().startswith(b'content-length:')), None)
                    if length is None or length < 0 or length > 4*1024*1024: return False
                    if len(body) < length: break
                    message = json.loads(body[:length])
                    buf = body[length:]
                    if message.get('id') == 1 and 'result' in message:
                        return isinstance(message['result'], dict) and 'capabilities' in message['result']
                    if message.get('id') == 1 and 'error' in message:
                        diagnostic['protocol_error'] = str(message['error'])[:2000]
                        return False
                    if 'method' in message and 'id' in message:
                        send({'jsonrpc': '2.0', 'id': message['id'], 'result': None})
            if process.poll() is not None: return False
        return False
    except (OSError, ValueError): return False
    finally:
        selector.close()
        try: os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError: pass
        process.wait()
        diagnostic['exit_code'] = process.returncode
        stderr.seek(0)
        diagnostic['stderr'] = stderr.read(2000).decode(errors='replace')
        stderr.close()


os.makedirs('/work/project', exist_ok=True)
os.makedirs('/work/home', exist_ok=True)
os.environ.update(HOME='/work/home', XDG_CACHE_HOME='/work/cache', LANG='C.UTF-8', LC_ALL='C.UTF-8')
results = []
# The trusted supervisor starts a fresh container for each repository. A server
# cannot poison another target's HOME, leave a daemon behind, or alter its report.
if len(sys.argv) != 2 or Path(sys.argv[1]).name != sys.argv[1]:
    raise SystemExit('Usage: smoke_servers.py REPOSITORY')
for directory in [Path('/opt/corpus/servers')/sys.argv[1]]:
    manifest = directory/'artifact.json'
    if not manifest.is_file(): continue
    meta = json.loads(manifest.read_text())
    initialization_options = {}
    tsdk = directory/'package/node_modules/typescript/lib'
    if directory.name == 'astro' and tsdk.is_dir():
        initialization_options = {'typescript': {'tsdk': str(tsdk)}}
    record = {'name': directory.name, 'status': 'no-initialize-response', 'attempts': []}
    hints = {meta['name'].replace('_', '-')}
    hints.update(name.replace('_', '-') for ref in meta.get('references', []) for name in ref['ids'])
    def rank(entry):
        name = entry['name'].replace('_', '-')
        return (0 if name in hints else 1 if re.search(r'(^|-)(lsp|ls)($|-)|server|analyzer', name) else 2, name)
    executables = sorted((b for b in meta['executables'] if not b['name'].startswith(('python', 'pip'))), key=rank)
    for entry in executables[:3]:
        command = ([entry['interpreter']] if entry.get('interpreter') else [])+[str(directory/entry['path'])]
        for arguments in ([], ['--stdio'], ['--lsp'], ['lsp'], ['server'], ['language-server'], ['move-analyzer'], ['serve'], ['lsp-proxy'], ['start', '--stdio']):
            record['attempts'].append([entry['name'], *arguments])
            diagnostic = {'command': [entry['name'], *arguments]}
            try: passed = probe(command+arguments, diagnostic, initialization_options)
            except (OSError, ValueError, TypeError) as error:
                passed = False
                record['last_error'] = str(error)[:500]
            if not passed: record.setdefault('failures', []).append(diagnostic)
            if passed:
                record.update(status='passed', executable=entry['name'], arguments=arguments)
                break
        if record['status'] == 'passed': break
    results.append(record)
    print(json.dumps(record), flush=True)
Path('/out/server-smoke.json').write_text(json.dumps(results, indent=2)+'\n')
