#!/usr/bin/env python3
"""Bounded protocol diagnostics; invoke only through containers/run."""
import json
import os
import subprocess
import sys
import time

os.makedirs('/work/home', exist_ok=True)
os.makedirs('/work/project', exist_ok=True)
request = json.dumps({'jsonrpc':'2.0','id':1,'method':'initialize','params':{
    'processId':None,'rootUri':'file:///work/project','capabilities':{}}}).encode()
data = f'Content-Length: {len(request)}\r\n\r\n'.encode()+request
p = subprocess.Popen(sys.argv[1:], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
p.stdin.write(data)
p.stdin.flush()
time.sleep(2)
if p.poll() is None: p.kill()
out, err = p.communicate()
print(json.dumps({'exit':p.returncode,'stdout':out[:4000].decode(errors='replace'),'stderr':err[:4000].decode(errors='replace')}))
