#!/usr/bin/env python3
"""Runs only inside an isolated builder. Prepare online; compile offline."""
import hashlib
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys

job = json.loads(Path('/input/job.json').read_text())
source = Path('/work/source')
if not source.exists():
    shutil.copytree('/input/source', source, symlinks=True, ignore=shutil.ignore_patterns('.git'))
os.makedirs('/work/home', exist_ok=True)
os.makedirs('/work/tmp', exist_ok=True)
os.chdir(source)
os.environ.update(HOME='/work/home', CARGO_HOME='/work/cargo', GOMODCACHE='/work/gomod',
                  LANG='C.UTF-8', LC_ALL='C.UTF-8',
                  GOCACHE='/work/gocache', GOPATH='/work/gopath', GOTOOLCHAIN='local',
                  npm_config_cache='/work/npm-cache', TMPDIR='/work/tmp', CI='true', GIT_CONFIG_NOSYSTEM='1',
                  GIT_CONFIG_GLOBAL='/dev/null', CARGO_BUILD_JOBS='2',
                  DOTNET_ROOT='/opt/toolchains/dotnet', DOTNET_CLI_HOME='/work/home',
                  DOTNET_CLI_TELEMETRY_OPTOUT='1', DOTNET_SKIP_FIRST_TIME_EXPERIENCE='1',
                  NUGET_PACKAGES='/work/nuget',
                  PATH='/opt/toolchains/dotnet:/opt/toolchains/node/bin:/opt/toolchains/go/bin:/opt/toolchains/rust/bin:'+os.environ['PATH'])


def run(command):
    print('+', ' '.join(command), flush=True)
    subprocess.run(command, check=True)


def copy_runtime_tree(src, dest):
    # Source/dependency links are only allowed when they remain within this tree.
    absolute_links = []
    for path in src.rglob('*'):
        if path.is_symlink():
            resolved = path.resolve()
            if not resolved.is_relative_to(src.resolve()):
                raise ValueError(f'Runtime link escapes package: {path}')
            if Path(os.readlink(path)).is_absolute():
                absolute_links.append((path.relative_to(src), resolved.relative_to(src.resolve())))
    shutil.copytree(src, dest, symlinks=True, ignore=shutil.ignore_patterns('.git', 'target', '.cache'))
    for link, target in absolute_links:
        copied = dest/link
        if copied.is_symlink():
            copied.unlink()
            copied.symlink_to(os.path.relpath(dest/target, copied.parent))


kind = job['kind']
phase = sys.argv[1]
if phase == 'prepare' and job.get('fetch_git'):
    # Fetch public, pinned Git metadata only inside the networked sandbox.
    # Some compilers need git describe and some sources have pinned submodules.
    git = ['git', '-c', 'protocol.allow=never', '-c', 'protocol.https.allow=always']
    run([*git, 'init', '.'])
    remotes = subprocess.check_output([*git, 'remote'], text=True).splitlines()
    run([*git, 'remote', 'set-url' if 'origin' in remotes else 'add', 'origin', job['url']])
    run([*git, 'fetch', '--depth=1', 'origin', job['sha']])
    run([*git, 'reset', '--mixed' if job.get('local_development') else '--hard', 'FETCH_HEAD'])
    actual = subprocess.check_output([*git, 'rev-parse', 'HEAD'], text=True).strip()
    if actual != job['sha']: raise ValueError('Fetched source pin mismatch')
    if job.get('submodules') and not job.get('local_development'):
        if job.get('submodule_urls'):
            run([*git, 'submodule', 'init'])
            for name, url in job['submodule_urls'].items():
                run([*git, 'config', 'submodule.'+name+'.url', url])
        run([*git, 'submodule', 'update', '--init', '--recursive', '--depth=1'])
    Path('/work/source-provenance.json').write_text(json.dumps({
        'sha': actual, 'submodules': subprocess.check_output(
            [*git, 'submodule', 'status', '--recursive'], text=True).splitlines()}))
os.chdir(source / job.get('directory', ''))
os.environ.update(job.get('environment', {}))
if job.get('rust_toolchain'):
    os.environ['PATH'] = '/opt/toolchains/'+job['rust_toolchain']+'/bin:'+os.environ['PATH']
if job.get('go_toolchain'):
    os.environ['PATH'] = '/opt/toolchains/'+job['go_toolchain']+'/bin:'+os.environ['PATH']
if job.get('java_toolchain'):
    os.environ['JAVA_HOME'] = '/opt/toolchains/'+job['java_toolchain']
    os.environ['PATH'] = os.environ['JAVA_HOME']+'/bin:'+os.environ['PATH']
if kind == 'composer':
    os.environ.update(COMPOSER_HOME='/work/home/composer', COMPOSER_CACHE_DIR='/work/composer-cache')
if kind == 'bundler':
    os.environ.update(BUNDLE_WITHOUT='development:test', BUNDLE_PATH='/work/bundle')
if kind == 'gradle':
    os.environ.update(GRADLE_USER_HOME='/work/gradle')
if kind == 'cabal':
    os.environ.update(CABAL_DIR='/work/cabal')
if kind == 'pnpm':
    os.environ.update(PNPM_HOME='/work/manager/bin', COREPACK_ENABLE_NETWORK='0')
    os.environ['PATH'] = '/work/manager/node_modules/.bin:'+os.environ['PATH']
if phase == 'prepare':
    original_locks = Path('/work/original-locks')
    original_locks.mkdir(exist_ok=True)
    for name in ('Cargo.lock', 'package-lock.json', 'pnpm-lock.yaml', 'Gemfile.lock', 'composer.lock', 'mix.lock', 'rebar.lock'):
        if Path(name).is_file() and not (original_locks/name).exists():
            shutil.copyfile(name, original_locks/name)
    for command in job.get('before_prepare', []): run(command)
    if kind == 'cargo':
        command = ['cargo', 'fetch']
        if Path('Cargo.lock').exists() and not job.get('repair_lock'): command.append('--locked')
        run(command)
    elif kind == 'go': run(['go', 'mod', 'download', 'all'])
    elif kind == 'npm':
        for directory in job.get('npm_install_directories', ['.']):
            mode = 'ci' if (Path(directory)/'package-lock.json').exists() and not job.get('repair_lock') else 'install'
            run(['npm', '--prefix', directory, mode, '--ignore-scripts', '--no-audit', '--no-fund'])
    elif kind == 'pnpm':
        package = json.loads(Path('package.json').read_text())
        manager = job.get('package_manager', package.get('packageManager', '')).split('+')[0]
        if not manager.startswith('pnpm@') or not manager[5:]: raise ValueError('Missing pinned pnpm version')
        run(['npm', 'install', '--prefix=/work/manager', '--ignore-scripts', '--no-audit', '--no-fund', manager])
        if int(manager.split('@')[1].split('.')[0]) >= 12:
            # pnpm 12 ships a placeholder plus a platform-specific optional binary.
            # Initialize only this pinned manager, keeping project scripts disabled.
            run(['node', '/work/manager/node_modules/pnpm/install.js'])
        run(['pnpm', 'install', '--frozen-lockfile', '--ignore-scripts', '--store-dir=/work/pnpm-store'])
    elif kind == 'python':
        run(['python3', '-m', 'pip', 'wheel', '--wheel-dir=/work/wheels', '.'])
    elif kind == 'dotnet':
        run(['dotnet', 'restore', job['project'], '--runtime', 'linux-x64',
             '-p:SelfContained=true', '-p:Configuration=Release', '--use-lock-file',
             *['-p:'+k+'='+v for k,v in job.get('dotnet_properties', {}).items()]])
    elif kind == 'composer':
        run(['composer', 'install', '--no-dev', '--no-scripts', '--no-plugins', '--prefer-dist', '--no-interaction'])
    elif kind == 'bundler':
        # Resolve production gemspec dependencies without the project's development tools.
        Path('Gemfile.runtime').write_text('source "https://rubygems.org"\ngemspec\n')
        run(['bundle', 'lock', '--gemfile=Gemfile.runtime'])
        run(['bundle', 'cache', '--gemfile=Gemfile.runtime', '--no-install'])
    elif kind == 'gradle':
        # Resolve project/plugin dependencies in the public-network sandbox.
        # Application compilation and distribution tasks run offline below.
        Path('/work/prepare.gradle').write_text('''
gradle.projectsEvaluated {
    rootProject.tasks.register("corpusPrepareDependencies") {
        doLast {
            gradle.rootProject.allprojects.each { p ->
                (p.configurations + p.buildscript.configurations).each { c ->
                    if (c.canBeResolved) {
                        def artifacts = c.incoming.artifactView { lenient true }.artifacts
                        artifacts.artifactFiles.files.each { println("cached: " + it) }
                        artifacts.failures.each { println("unresolved: " + it.message) }
                    }
                }
            }
        }
    }
}
''')
        run(['bash', 'gradlew', '--no-daemon', '--max-workers=2',
             '--init-script=/work/prepare.gradle', 'corpusPrepareDependencies'])
    elif kind == 'cabal':
        run(['cabal', 'user-config', 'init', '--force'])
        config = Path('/work/cabal/config')
        config.write_text(config.read_text().replace('http://hackage.haskell.org/', 'https://hackage.haskell.org/'))
        run(['cabal', 'update'])
        run(['cabal', 'v2-build', '--only-download', '--disable-tests', '--disable-benchmarks', *job['cabal_targets']])
    elif kind == 'maven':
        run(['mvn', '--batch-mode', '-Dmaven.repo.local=/work/maven', *job.get('maven_args', []), 'dependency:go-offline'])
    elif kind != 'commands': raise ValueError(kind)
    for command in job.get('prepare_commands', []): run(command)
elif phase == 'build':
    output = Path('/out')
    bins = []
    for command in job.get('before_build', []): run(command)
    if kind == 'cargo':
        meta = json.loads(subprocess.check_output(['cargo', 'metadata', '--no-deps', '--format-version=1', '--offline']))
        candidates = [(p, t) for p in meta['packages'] for t in p['targets'] if 'bin' in t['kind']]
        hints = {job['name'].replace('_', '-')}
        hints.update(s.replace('_', '-') for ref in job['references'] for s in ref['ids'])
        selected = [(p,t) for p,t in candidates if t['name'].replace('_','-') in hints or p['name'].replace('_','-') in hints]
        for pair in candidates:
            if any(s in pair[1]['name'] for s in ('lsp', 'language-server', 'langserver')) and pair not in selected:
                selected.append(pair)
        if job.get('cargo_packages'): selected = [(p,t) for p,t in candidates if p['name'] in job['cargo_packages']]
        if not selected:
            selected = [(p,t) for p,t in candidates if 'lsp' in t['name'] or 'language-server' in t['name']]
        if not selected: selected = candidates
        if not selected: raise RuntimeError('Workspace contains no standalone executable')
        command = ['cargo', 'build', '--release', '--bins', '--locked', '--offline', '-j', '2']
        for name in sorted({p['name'] for p,t in selected}): command += ['--package', name]
        run(command)
        # Cargo metadata is evaluated only in this offline container.
        release = Path(meta['target_directory'])/'release'
        for package in meta['packages']:
            if package['name'] not in {p['name'] for p,t in selected}: continue
            for target in package['targets']:
                artifact = release/target['name']
                if 'bin' in target['kind'] and artifact.is_file():
                    shutil.copyfile(artifact, output/artifact.name)
                    (output/artifact.name).chmod(0o755)
                    bins.append({'name': artifact.name, 'path': artifact.name})
    elif kind == 'go':
        os.environ.update(GOPROXY='off', GOSUMDB='off')
        packages = subprocess.check_output(['go', 'list', '-mod=readonly', '-f', '{{if eq .Name "main"}}{{.ImportPath}}{{end}}', *job.get('go_packages', ['./...'])], text=True).split()
        hints = {job['name'], *(s for ref in job['references'] for s in ref['ids'])}
        selected = [p for p in packages if p.rsplit('/', 1)[-1] in hints and not any(part in p.split('/') for part in ('examples', 'testdata', 'testfixtures', 'tests'))]
        if not selected:
            selected = [p for p in packages if '/cmd/' in p and not any(part in p.split('/') for part in ('examples', 'testdata', 'testfixtures', 'tests'))]
        if not selected:
            selected = [p for p in packages if not any(part in p.split('/') for part in ('examples', 'testdata', 'testfixtures', 'tests'))]
        packages = selected
        seen = set()
        for package in packages:
            name = package.rsplit('/', 1)[-1]
            if name == 'cmd': name = job['name']
            if name in seen: raise ValueError('Conflicting executable names: '+name)
            seen.add(name)
            run(['go', 'build', '-mod=readonly', '-p', '2', '-trimpath', '-o', str(output/name), package])
            bins.append({'name': name, 'path': name})
    elif kind == 'cabal':
        run(['cabal', 'v2-build', '--offline', '-j2', '--disable-tests', '--disable-benchmarks', *job['cabal_targets']])
        for target in job['cabal_targets']:
            artifact = Path(subprocess.check_output(['cabal', 'list-bin', '--offline', target], text=True).strip())
            shutil.copyfile(artifact, output/artifact.name)
            (output/artifact.name).chmod(0o755)
            bins.append({'name': artifact.name, 'path': artifact.name})
    elif kind in ('npm', 'pnpm'):
        os.environ['npm_config_offline'] = 'true'
        package = json.loads(Path('package.json').read_text())
        if job.get('script'): run(['pnpm' if kind == 'pnpm' else 'npm', 'run', job['script']])
        paths = job.get('node_bins', package.get('bin', {}))
        if isinstance(paths, str): paths = {package['name'].rsplit('/', 1)[-1]: paths}
        for name, path in paths.items():
            if not Path(path).is_file(): raise FileNotFoundError(path)
            bins.append({'name': name, 'path': 'package/'+path.removeprefix('./'), 'interpreter': 'node'})
        copy_runtime_tree(Path.cwd(), output/'package')
    elif kind in ('commands', 'gradle', 'maven'):
        if kind == 'gradle':
            run(['bash', 'gradlew', '--offline', '--no-daemon', '--max-workers=2', *job['gradle_tasks']])
        if kind == 'maven':
            run(['mvn', '--offline', '--batch-mode', '-Dmaven.repo.local=/work/maven', *job.get('maven_args', []), *job['maven_goals']])
        for command in job.get('build_commands', []): run(command)
        for entry in job.get('runtime_directories', []):
            copy_runtime_tree(Path(entry['source']), output/entry['path'])
        for entry in job['outputs']:
            target = output/entry['path']
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(entry['source'], target)
            target.chmod(0o755)
            bins.append({k:v for k,v in entry.items() if k != 'source'})
        for entry in job.get('runtime_files', []):
            target = output/entry['path']
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(entry['source'], target)
    elif kind == 'python':
        prefix = Path('/opt/corpus/servers')/job['name']/'venv'
        run(['python3', '-m', 'venv', '--copies', str(prefix)])
        wheels = list(Path('/work/wheels').glob('*.whl'))
        if not wheels: raise RuntimeError('No wheels prepared')
        run([str(prefix/'bin/pip'), 'install', '--no-index', '--find-links=/work/wheels', *map(str, wheels)])
        for path in (prefix/'bin').iterdir():
            if path.is_file() and not path.is_symlink() and not path.name.startswith(('python', 'pip')) and path.name not in ('activate', 'activate.csh', 'activate.fish', 'Activate.ps1'):
                bins.append({'name': path.name, 'path': 'venv/bin/'+path.name})
    elif kind == 'dotnet':
        run(['dotnet', 'publish', job['project'], '--no-restore', '--configuration', 'Release',
             '--runtime', 'linux-x64', '--self-contained', 'true', '--output', '/out/publish',
             *['-p:'+k+'='+v for k,v in job.get('dotnet_properties', {}).items()]])
        executable = output/'publish'/job['executable']
        if not executable.is_file(): raise FileNotFoundError(executable)
        bins.append({'name': job.get('command_name', job['executable']), 'path': 'publish/'+job['executable']})
    elif kind == 'composer':
        os.environ['COMPOSER_DISABLE_NETWORK'] = '1'
        run(['composer', 'dump-autoload', '--no-dev', '--no-scripts', '--no-plugins', '--no-interaction'])
        copy_runtime_tree(Path.cwd(), output/'package')
        for path in json.loads(Path('composer.json').read_text()).get('bin', []):
            if not Path(path).is_file(): raise FileNotFoundError(path)
            run(['php', '-l', path])
            bins.append({'name': Path(path).name, 'path': 'package/'+path, 'interpreter': 'php'})
    elif kind == 'bundler':
        copy_runtime_tree(Path.cwd(), output/'package')
        prefix = Path('/opt/corpus/servers')/job['name']/'package'
        os.environ.update(BUNDLE_GEMFILE=str(prefix/'Gemfile.runtime'),
                          BUNDLE_PATH=str(prefix/'vendor/bundle'), BUNDLE_FROZEN='true')
        run(['bundle', 'install', '--local', '--jobs=2'])
        for name, path in job['ruby_bins'].items():
            if not (prefix/path).is_file(): raise FileNotFoundError(path)
            wrapper = output/name
            wrapper.write_text('#!/bin/sh\nexport BUNDLE_GEMFILE='+shlex.quote(str(prefix/'Gemfile.runtime'))+
                '\nexport BUNDLE_PATH='+shlex.quote(str(prefix/'vendor/bundle'))+
                '\nexport BUNDLE_WITHOUT=development:test BUNDLE_FROZEN=true\nexec bundle exec ruby '+
                shlex.quote(str(prefix/path))+' "$@"\n')
            wrapper.chmod(0o755)
            bins.append({'name': name, 'path': name})
    if not bins: raise RuntimeError('Build produced no standalone executable')
    locks = output/'dependency-locks'
    locks.mkdir(exist_ok=True)
    if Path('/work/source-provenance.json').exists():
        shutil.copyfile('/work/source-provenance.json', locks/'source-provenance.json')
    for name in ('Cargo.lock', 'go.mod', 'go.sum', 'package-lock.json', 'pnpm-lock.yaml', 'yarn.lock', 'Gemfile.runtime.lock', 'composer.lock', 'mix.lock', 'rebar.lock', 'build.zig.zon', 'gradle.lockfile'):
        if Path(name).is_file(): shutil.copyfile(name, locks/name)
    if Path('/work/original-locks').exists():
        shutil.copytree('/work/original-locks', locks/'original')
    for name in ('manager', 'tools'):
        path = Path('/work')/name/'package-lock.json'
        if path.is_file(): shutil.copyfile(path, locks/(name+'-package-lock.json'))
    if Path('dist-newstyle/cache/plan.json').is_file():
        shutil.copyfile('dist-newstyle/cache/plan.json', locks/'cabal-plan.json')
    for pattern in ('LICENSE*', 'COPYING*', 'NOTICE*'):
        for file in Path.cwd().glob(pattern):
            if file.is_file() and not file.is_symlink(): shutil.copyfile(file, output/file.name)
    hashes = {str(p.relative_to(output)): hashlib.sha256(p.read_bytes()).hexdigest() for p in output.rglob('*') if p.is_file() and not p.is_symlink()}
    (output/'artifact.json').write_text(json.dumps(dict(job, executables=bins, hashes=hashes,
        worker_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()), indent=2)+'\n')
else: raise ValueError(phase)
