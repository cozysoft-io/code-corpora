#!/usr/bin/env python3
"""Harmless probes executed inside each proposed container profile."""
import json
import os
from pathlib import Path
import socket
import sys
import urllib.request

online = '--online' in sys.argv
assert os.getuid() != 0
status = dict(line.split(':', 1) for line in Path('/proc/self/status').read_text().splitlines() if ':' in line)
assert int(status['CapEff'].strip(), 16) == 0
assert status['NoNewPrivs'].strip() == '1'
assert status['Seccomp'].strip() == '2'
assert Path('/sys/fs/cgroup/memory.max').read_text().strip() != 'max'
assert Path('/sys/fs/cgroup/pids.max').read_text().strip() != 'max'
for path in ('/srv/corpus/host-only-sentinel', '/home/mgsloan/.ssh', '/run/podman/podman.sock', '/var/run/docker.sock'):
    assert not Path(path).exists(), path
for key in os.environ:
    assert not any(s in key.upper() for s in ('TOKEN', 'PASSWORD', 'SECRET', 'GOOGLE_APPLICATION_CREDENTIALS', 'SSH_AUTH_SOCK')), key
try:
    Path('/input/boundary-write').write_text('probe')
    raise AssertionError('Input is writable')
except OSError: pass
for host in ('169.254.169.254', '10.73.0.1', '10.0.2.2') + (() if online else ('1.1.1.1',)):
    try:
        sock = socket.create_connection((host, 80 if host != '1.1.1.1' else 443), timeout=1)
    except OSError: continue
    else:
        sock.close()
        raise AssertionError('Unexpected network connection to '+host)
if online:
    with urllib.request.urlopen('https://registry.npmjs.org', timeout=20) as result:
        assert result.status == 200
print(json.dumps({'boundary': 'passed', 'network': 'public-downloads' if online else 'none', 'uid': os.getuid()}))
