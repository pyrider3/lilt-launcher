#!/usr/bin/env python3
"""Install only this launcher. Never edits compositor or shell configuration."""
import argparse
from pathlib import Path
import shutil

parser = argparse.ArgumentParser()
parser.add_argument("--prefix", type=Path, default=Path.home() / ".local")
parser.add_argument("--uninstall", action="store_true")
args = parser.parse_args()
root = Path(__file__).resolve().parent
prefix = args.prefix.expanduser().resolve()
package = prefix / "share/lilt-launcher"
binary = prefix / "bin/lilt-launcher"
desktop = prefix / "share/applications/lilt-launcher.desktop"
if args.uninstall:
    if package.is_dir():
        shutil.rmtree(package)
    binary.unlink(missing_ok=True)
    desktop.unlink(missing_ok=True)
    print("Removed launcher files. Your state and niri bindings were retained.")
else:
    for name in ("payload", "tools"):
        shutil.copytree(root / name, package / name, dirs_exist_ok=True)
    for name in ("config.json", "LICENSE", "NOTICE", "README.md"):
        shutil.copy2(root / name, package / name)
    binary.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(root / "bin/lilt-launcher", binary)
    binary.chmod(0o755)
    desktop.parent.mkdir(parents=True, exist_ok=True)
    desktop.write_text(f'[Desktop Entry]\nType=Application\nName=Lilt Launcher\nExec="{binary}" toggle\nIcon=system-search\nTerminal=false\nCategories=Utility;\n')
    print(f"Installed {binary}. Add a niri key binding as described in README.md.")
