import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('icons', ROOT / 'tools/build_icon_cache.py')
icons = importlib.util.module_from_spec(spec)
spec.loader.exec_module(icons)

class PackageTests(unittest.TestCase):
    def test_icon_cache(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root/'applications').mkdir()
            (root/'icons/hicolor/48x48/apps').mkdir(parents=True)
            (root/'applications/example.desktop').write_text('[Desktop Entry]\nIcon=example\n')
            expected = root/'icons/hicolor/48x48/apps/example.svg'
            expected.write_text('<svg/>')
            (expected.parent/'application-x-executable.svg').symlink_to(root/'missing')
            output=root/'cache/icons.json'
            icons.build(output,root,[])
            self.assertEqual(json.loads(output.read_text()),{'example':str(expected)})

    def test_install_uninstall(self):
        with tempfile.TemporaryDirectory() as tmp:
            prefix=Path(tmp)
            sentinel=prefix/'keep.txt';sentinel.write_text('keep')
            subprocess.run([sys.executable,str(ROOT/'install.py'),'--prefix',tmp],check=True,capture_output=True)
            self.assertTrue((prefix/'bin/lilt-launcher').is_file())
            self.assertTrue((prefix/'share/lilt-launcher/payload/shell.qml').is_file())
            subprocess.run([sys.executable,str(ROOT/'install.py'),'--prefix',tmp,'--uninstall'],check=True,capture_output=True)
            self.assertEqual(sentinel.read_text(),'keep')
            self.assertFalse((prefix/'share/lilt-launcher').exists())

    def test_no_local_paths(self):
        for relative in ['bin/lilt-launcher','config.json','payload/shell.qml','payload/services/AppSearch.qml']:
            text=(ROOT/relative).read_text()
            self.assertNotIn(str(Path.home())+'/',text,relative)
            self.assertNotIn('Documents/Codex',text,relative)
        self.assertFalse((ROOT/'payload/assets/launcher-icons.json').exists())
        self.assertFalse((ROOT/'runtime').exists())

if __name__=='__main__':unittest.main()
