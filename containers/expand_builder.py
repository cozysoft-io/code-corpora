#!/usr/bin/env python3
"""Layer additional pinned SDKs onto the existing builder, without source mounts."""
import json
import os
import shutil
import subprocess
from build_grammars import ROOT, USER, PODMAN, atomic_json

os.chdir(ROOT)
context = ROOT/'images/sdk-extra'
context.mkdir(parents=True, exist_ok=True)
os.chown(context, USER.pw_uid, USER.pw_gid)
for source, target in [('Containerfile.build-extra', 'Containerfile'),
                       ('install_extra.py', 'install_extra.py'),
                       ('toolchains.extra.json', 'toolchains.extra.json')]:
    shutil.copyfile(ROOT/'repo/containers'/source, context/target)
base = subprocess.check_output([*PODMAN, 'image', 'inspect', '--format={{.Id}}', 'localhost/code-corpora-build:toolchains'], text=True).strip()
subprocess.run([*PODMAN, 'build', '--network=slirp4netns', '--memory=4g',
    '--build-arg=BUILDER_IMAGE='+base, '-t', 'localhost/code-corpora-build:expanded', str(context)], check=True)
atomic_json(ROOT/'artifacts/build-expanded-image.json', json.loads(subprocess.check_output(
    [*PODMAN, 'image', 'inspect', 'localhost/code-corpora-build:expanded'])))
