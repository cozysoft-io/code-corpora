import json
import os
import shutil
import subprocess
from build_grammars import ROOT, USER, PODMAN, atomic_json

os.chdir(ROOT)
context = ROOT/'images/sdk-compat'
context.mkdir(parents=True, exist_ok=True)
os.chown(context, USER.pw_uid, USER.pw_gid)
for source, target in [('Containerfile.build-compat', 'Containerfile'),
                       ('install_rust_compat.py', 'install_rust_compat.py'),
                       ('toolchains.rust-compat.json', 'toolchains.rust-compat.json'),
                       ('toolchains.more.json', 'toolchains.more.json'),
                       ('install_more.py', 'install_more.py'),
                       ('toolchains.go-compat.json', 'toolchains.go-compat.json'),
                       ('install_go_compat.py', 'install_go_compat.py'),
                       ('toolchains.java.json', 'toolchains.java.json'),
                       ('toolchains.java-11.json', 'toolchains.java-11.json'),
                       ('install_tar_toolchain.py', 'install_tar_toolchain.py')]:
    shutil.copyfile(ROOT/'repo/containers'/source, context/target)
base = subprocess.check_output([*PODMAN, 'inspect', '--format={{.Id}}', 'localhost/code-corpora-build:expanded'], text=True).strip()
subprocess.run([*PODMAN, 'build', '--network=slirp4netns', '--memory=4g', '--cpu-period=100000', '--cpu-quota=200000',
    '--build-arg=BUILDER_IMAGE='+base, '-t', 'localhost/code-corpora-build:compat', str(context)], check=True)
atomic_json(ROOT/'artifacts/build-compat-image.json', json.loads(subprocess.check_output(
    [*PODMAN, 'image', 'inspect', 'localhost/code-corpora-build:compat'])))
