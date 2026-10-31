# Attribution and modifications

Based on iNiR by snowarch (https://github.com/snowarch/inir).

Upstream snapshot: 48cdcecb0f6089cfbb7019054602eab28e154b3b.
Copyright (C) 2025–2026 snowarch and contributors. The project also derives from end-4's illogical-impulse. Keep LICENSE and NOTICE with every copy.

This is a modified standalone derivative called **Lilt Launcher**, not an official upstream product. No affiliation or endorsement is claimed. Internal upstream class names remain to preserve source provenance and compatibility.

Modifications, 2026-10-31:

- Replace the full-shell entry point with a launcher-only overlay and IPC interface.
- Expose application search and optional browser search, without the upstream bar, Dock or shell installation flow.
- Adapt IrisPalette, IrisMorphSurface and their original motion system to a self-contained surface with synchronized fade.
- Keep input geometry fixed during resizing; suppress the placeholder during IME composition.
- Remove initial suggestions and per-query fading; cap the all-applications viewport while retaining scrolling.
- Resolve real icon files with fallback artwork.
- Launch apps through the normal user systemd session.
- Add relocatable startup, user-prefix installation/uninstallation and package checks.

Shared modules remain bundled but are not all loaded. Unused desktop installers, service definitions, wallpaper collections, product logos and desktop entries are excluded from the install flow.
