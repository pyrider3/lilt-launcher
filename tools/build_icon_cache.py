"""Resolve installed desktop icons once at cold startup, never per keystroke."""
import json
import os
import re
from pathlib import Path


def build(output: Path, data_home: Path, data_dirs: list[Path]) -> int:
    wanted = {"application-x-executable", "utilities-terminal", "google-chrome", "system-run"}
    for folder in [data_home, *data_dirs]:
        for desktop in (folder / "applications").glob("*.desktop"):
            try:
                for line in desktop.read_text(errors="replace").splitlines():
                    if line.startswith("Icon="):
                        wanted.add(line[5:].strip())
            except OSError:
                continue
    roots = [data_home / "icons"]
    roots += [d / "icons" / theme for d in data_dirs for theme in ("hicolor", "breeze", "Adwaita")]
    roots += [d / "pixmaps" for d in data_dirs]
    icons, scores = {}, {}
    for rank, root in enumerate(roots):
        if not root.is_dir():
            continue
        for path in root.rglob("*"):
            if path.suffix.lower() not in (".svg", ".png", ".xpm") or path.stem not in wanted:
                continue
            if not path.is_file():
                continue
            size = max([int(n) for n in re.findall(r"/(\d+)(?:x\d+)?/", str(path))] or [48])
            score = (len(roots) - rank) * 10000 + (1000 if path.suffix == ".svg" else 0) + min(size, 512)
            if score > scores.get(path.stem, -1):
                icons[path.stem], scores[path.stem] = str(path), score
    for name in wanted:
        path = Path(name.removeprefix("file://"))
        if path.is_absolute() and path.is_file():
            icons[name] = str(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    temp = output.with_suffix(".tmp")
    temp.write_text(json.dumps(icons, ensure_ascii=False))
    os.replace(temp, output)
    return len(icons)
