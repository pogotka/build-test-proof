"""Build plugin and standalone skill archives using only bundled source files."""
from pathlib import Path
import hashlib
import json
import zipfile
from install_skill import payload

root = Path(__file__).resolve().parent.parent
source = root / 'plugins/build-test-proof'
version = json.loads((source / 'plugin.json').read_text())['version']
output = root / 'dist'
output.mkdir(exist_ok=True)
plugin = {}
for p in sorted(source.rglob('*')):
    if p.is_symlink() or p.name == '.DS_Store' or '__pycache__' in p.parts:
        raise ValueError(f'Unexpected package resource: {p}')
    if p.is_file():
        plugin[p.relative_to(source).as_posix()] = p.read_bytes()
standalone = {'build-test-proof/' + name: data for name, data in payload().items()}
archives = [(f'build-test-proof-{version}.zip', plugin),
            (f'build-test-proof-skill-{version}.zip', standalone)]
checksums = []
for name, files in archives:
    path = output / name
    with zipfile.ZipFile(path, 'w', compression=zipfile.ZIP_DEFLATED) as bundle:
        for relative, data in sorted(files.items()):
            info = zipfile.ZipInfo(relative, date_time=(2026, 10, 13, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            bundle.writestr(info, data)
    with zipfile.ZipFile(path) as bundle:
        assert bundle.testzip() is None
        assert set(bundle.namelist()) == set(files)
        for relative, data in files.items():
            assert bundle.read(relative) == data
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    checksums.append(f'{digest}  {name}\n')
    print(f'{name}: {len(files)} files; SHA256 {digest}')
(output / 'SHA256SUMS').write_text(''.join(checksums))
