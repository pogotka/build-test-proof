#!/usr/bin/env python3
"""Install the bundled portable skill. No network, package installs or rule edits."""
import argparse
import json
from pathlib import Path
import shutil
import tempfile

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / 'plugins/build-test-proof/skills/build-test-proof'
LOCATIONS = {
    'cursor': ('.cursor/skills', '.cursor/skills'),
    'claude': ('.claude/skills', '.claude/skills'),
    'copilot': ('.copilot/skills', '.github/skills'),
    'opencode': ('.config/opencode/skills', '.opencode/skills'),
}

def payload():
    files = {}
    for p in SOURCE.rglob('*'):
        if p.is_symlink():
            raise ValueError(f'Symlink source is unsupported: {p}')
        if p.is_file() and 'agents' not in p.relative_to(SOURCE).parts:
            if p.name == '.DS_Store' or '__pycache__' in p.parts:
                raise ValueError(f'Unexpected source resource: {p}')
            files[p.relative_to(SOURCE).as_posix()] = p.read_bytes()
    files['LICENSE'] = (ROOT / 'LICENSE').read_bytes()
    files['INSTALLATION.json'] = (json.dumps({
        'source': 'https://github.com/pogotka/build-test-proof',
        'version': json.loads((ROOT / 'plugins/build-test-proof/plugin.json').read_text())['version'],
        'mode': 'standalone_skill',
    }, indent=2) + '\n').encode()
    return files

def destination(host, scope, home, project):
    if scope == 'project':
        if project is None or not project.is_dir():
            raise ValueError('--project must name an existing directory for project scope')
        base = project.resolve()
    else:
        base = home.resolve()
    location = LOCATIONS[host][scope == 'project']
    return base / location / 'build-test-proof'

def install(target, files, dry_run=False):
    if target.is_symlink():
        raise ValueError(f'Refusing symlink destination: {target}')
    if target.exists():
        if not target.is_dir():
            raise ValueError(f'Destination is not a directory: {target}')
        actual = {}
        for p in target.rglob('*'):
            if p.is_symlink():
                raise ValueError(f'Refusing existing symlink: {p}')
            if p.is_file():
                actual[p.relative_to(target).as_posix()] = p.read_bytes()
        if actual == files:
            return 'already_current'
        raise ValueError(f'Destination differs: {target}. Preserve/review that folder before replacing it; no files were overwritten.')
    if dry_run:
        return 'would_install'
    # Do not follow a pre-existing linked parent into an unexpected location.
    if any(p.is_symlink() for p in target.parents):
        raise ValueError('Refusing symlink parent directory')
    target.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix='.build-test-proof-', dir=target.parent))
    try:
        for name, data in files.items():
            path = staging / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        staging.rename(target)
    finally:
        if staging.exists():
            shutil.rmtree(staging)
    return 'installed'

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host', choices=LOCATIONS, required=True)
    parser.add_argument('--scope', choices=['user', 'project'], default='user')
    parser.add_argument('--home', type=Path, default=Path.home(), help='Home override for portable environments/tests')
    parser.add_argument('--project', type=Path)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    try:
        if args.scope == 'user' and args.project is not None:
            raise ValueError('--project requires --scope project')
        target = destination(args.host, args.scope, args.home, args.project)
        status = install(target, payload(), args.dry_run)
    except (OSError, ValueError) as error:
        parser.exit(2, str(error) + '\n')
    print(json.dumps({'status': status, 'host': args.host, 'path': str(target),
                      'limits': 'File installation only; open a fresh host session to verify discovery and activation.'}, indent=2))

if __name__ == '__main__':
    main()
