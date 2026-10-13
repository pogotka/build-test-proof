import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('installer', Path(__file__).resolve().parents[1] / 'scripts/install_skill.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class InstallTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name).resolve()
        self.files = m.payload()
    def tearDown(self):
        self.tmp.cleanup()
    def test_host_paths_and_full_payload(self):
        expected={'cursor':('.cursor/skills','.cursor/skills'), 'claude':('.claude/skills','.claude/skills'),
                  'copilot':('.copilot/skills','.github/skills'), 'opencode':('.config/opencode/skills','.opencode/skills')}
        for host, paths in expected.items():
            for scope, location in zip(['user','project'], paths):
                with self.subTest(host=host,scope=scope):
                    base=self.base/host/scope; base.mkdir(parents=True)
                    target=m.destination(host,scope,base,base if scope=='project' else None)
                    self.assertEqual(target,base/location/'build-test-proof')
                    self.assertEqual(m.install(target,self.files),'installed')
                    for name,data in self.files.items(): self.assertEqual((target/name).read_bytes(),data)
    def test_dry_run_has_no_side_effects(self):
        target=self.base/'not-created'/'skill'
        self.assertEqual(m.install(target,self.files,True),'would_install')
        self.assertFalse(target.parent.exists())
    def test_repeated_install_is_idempotent(self):
        target=self.base/'skill'; m.install(target,self.files)
        stamp=(target/'SKILL.md').stat().st_mtime_ns
        self.assertEqual(m.install(target,self.files),'already_current')
        self.assertEqual((target/'SKILL.md').stat().st_mtime_ns,stamp)
    def test_preserves_modified_skill(self):
        target=self.base/'skill';m.install(target,self.files);(target/'SKILL.md').write_text('user work')
        with self.assertRaises(ValueError):m.install(target,self.files)
        self.assertEqual((target/'SKILL.md').read_text(),'user work')
    def test_preserves_unrelated_extra_file(self):
        target=self.base/'skill';m.install(target,self.files);(target/'notes.txt').write_text('private notes')
        with self.assertRaises(ValueError):m.install(target,self.files)
        self.assertEqual((target/'notes.txt').read_text(),'private notes')
    def test_rejects_file_destination(self):
        target=self.base/'skill';target.write_text('user work')
        with self.assertRaises(ValueError):m.install(target,self.files)
        self.assertEqual(target.read_text(),'user work')
    def test_rejects_linked_destination(self):
        real=self.base/'real';real.mkdir();target=self.base/'skill';target.symlink_to(real,target_is_directory=True)
        with self.assertRaises(ValueError):m.install(target,self.files)
        self.assertEqual(list(real.iterdir()),[])
    def test_rejects_linked_parent(self):
        real=self.base/'real';real.mkdir();parent=self.base/'linked';parent.symlink_to(real,target_is_directory=True)
        with self.assertRaises(ValueError):m.install(parent/'skill',self.files)
        self.assertEqual(list(real.iterdir()),[])
    def test_project_scope_requires_existing_project(self):
        for project in [None,self.base/'missing']:
            with self.assertRaises(ValueError):m.destination('claude','project',self.base,project)
    def test_standalone_is_self_contained(self):
        import re
        self.assertIn('INSTALLATION.json',self.files);self.assertIn('LICENSE',self.files)
        self.assertFalse(any(name.startswith('agents/') for name in self.files))
        for name,data in self.files.items():
            if not name.endswith('.md'):continue
            prose=re.sub(r'```.*?```','',data.decode(),flags=re.S)
            for link in re.findall(r'\]\(([^)]+)\)',prose):
                if link.startswith(('https:','http:','/','#')):continue
                from posixpath import normpath,join,dirname
                self.assertIn(normpath(join(dirname(name),link.split('#')[0])),self.files)

if __name__=='__main__':unittest.main()
