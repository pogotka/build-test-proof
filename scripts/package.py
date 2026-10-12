from pathlib import Path
import hashlib, json, zipfile
root = Path(__file__).resolve().parent.parent
source = root / "plugins/build-test-proof"
version = json.loads((source / "plugin.json").read_text())["version"]
output = root / "dist" / f"build-test-proof-{version}.zip"
output.parent.mkdir(exist_ok=True)
files = sorted(p for p in source.rglob("*") if p.is_file())
with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
    for p in files:
        if p.is_symlink() or p.name == ".DS_Store" or "__pycache__" in p.parts:
            raise ValueError(f"Unexpected resource: {p}")
        bundle.write(p, p.relative_to(source))
with zipfile.ZipFile(output) as bundle:
    assert bundle.testzip() is None
    assert "plugin.json" in bundle.namelist()
    for p in files:
        assert bundle.read(p.relative_to(source).as_posix()) == p.read_bytes()
digest = hashlib.sha256(output.read_bytes()).hexdigest()
(output.parent / "SHA256SUMS").write_text(f"{digest}  {output.name}\n")
print(f"{output.name}: {len(files)} files; SHA256 {digest}")
