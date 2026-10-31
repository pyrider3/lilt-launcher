# Lilt Launcher

[简体中文](README.zh-CN.md) · English

A modified standalone application launcher for **niri / Wayland**, with continuous motion and a quiet search interface.

**Based on iNiR by snowarch (https://github.com/snowarch/inir).**

This is an unofficial derivative, not the official iNiR or iRiS project. The original QML interface and motion system belong to their upstream authors; this repository packages the standalone adaptation under a different name.

## Features

- A search field at rest, without application suggestions.
- Shared panel/content fade and scale transitions.
- Stable result updates without per-keystroke flashing.
- Animated height with a fixed search field when clearing text.
- IME composition hides the placeholder.
- `>` shows all applications in a capped, scrollable viewport; `> name` filters them.
- `? keywords` opens a web search in the default browser.
- Actual icon-file lookup and a generic fallback.
- Coexists with Noctalia without changing its bar or your window animations.

## Requirements

Initial target: Arch Linux, niri 26.04, Quickshell 0.3.2, Qt 6.12, and a systemd user session. Other distributions have not been validated.

```sh
sudo pacman -S --needed quickshell bubblewrap python go gtk3 kirigami syntax-highlighting \
  qt6-5compat qt6-multimedia qt6-svg qt6-wayland qt6-imageformats \
  ttf-material-symbols-variable breeze-icons
```

Go 1.26+ builds the upstream palette solver locally on first use; without Go, its bundled default palette is used.

No precompiled runtimes, package archives, personal configuration, clipboard data or caches are included.

## Install

```sh
git clone https://github.com/pyrider3/lilt-launcher.git
cd lilt-launcher
python3 install.py
~/.local/bin/lilt-launcher check
~/.local/bin/lilt-launcher open
```

The installer adds application files and a desktop entry under `~/.local`; choose another prefix with `--prefix`. It does not edit niri or enable autostart.

Add a binding inside your niri `binds` block:

```kdl
Mod+Space repeat=false { spawn "lilt-launcher" "toggle"; }
```

If `~/.local/bin` is not in niri's PATH, use the full path to your installed command. You may use `Mod+D` after removing its existing binding. Run `niri validate` after editing.

## Use

| Input | Action |
| --- | --- |
| Application name | Search apps |
| `>` | Browse all applications |
| `> name` | Filter applications |
| `? keywords` | Search the web |
| Up / Down / Tab | Change selection |
| Enter | Open result |
| Escape | Clear query; Escape again closes |

Commands: `open`, `toggle`, `close`, `search "query"`, `status`, `stop`, `check`.

The host starts on demand and stays warm. `stop` exits it; the next invocation starts it again.

## Configuration

State is isolated under `${XDG_STATE_HOME:-~/.local/state}/lilt-launcher/`:

- `config/illogical-impulse/config.json`: launcher settings (nested directory retained for upstream compatibility).
- `logs/session.log`: runtime diagnostics.
- `icons.json`: icon-file cache, rebuilt at cold startup.

`search.engineBaseUrl` defaults to `https://www.google.com/search?q=`. Search queries are URL-encoded. Applications and browser searches launch through the normal systemd user session, preserving their ordinary profiles.

Bubblewrap makes the filesystem read-only except for launcher state and the session runtime directory. The launcher retains session-bus/compositor access; this is not a security boundary for untrusted QML.

## Uninstall

```sh
~/.local/bin/lilt-launcher stop
python3 install.py --uninstall
```

Remove the niri binding you added. User state is retained; delete it separately if desired.

## Scope and validation

This is an application launcher, not a full desktop shell. It does not expose the original settings panels, Dock, clipboard manager or shell actions. Shared upstream QML modules are retained for import compatibility; not all bundled modules are instantiated. A future dependency reduction should preserve authorship and notices.

The package is generalized from a working local adaptation. Fresh-machine dependency coverage, other distributions and GPU-specific rendering still need testing. See the repository tests for installation and icon-cache checks.

## Provenance and license

Upstream snapshot: `snowarch/iNiR` commit `48cdcecb0f6089cfbb7019054602eab28e154b3b`.

Modified areas: standalone host, search providers, isolated startup, install/uninstall, icon resolution, IME placeholder, result layout and synchronized opening/closing opacity.

GPL-3.0, with applicable upstream additional terms preserved in [NOTICE](NOTICE). See [UPSTREAM.md](UPSTREAM.md). Bundled fonts retain their adjacent licenses. No upstream product logo is used.
