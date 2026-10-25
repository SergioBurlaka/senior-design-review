# Changelog

All notable changes to this plugin. Versions follow [semver](https://semver.org);
`version` in `.claude-plugin/plugin.json` is raised with every release, otherwise
`claude plugin update` keeps the old copy.

## 1.0.0 — 2026-10-25

First public release.

- Senior product-designer review flow: brief → choose the browser ("eyes") →
  map and capture → measure → designer passes → second look → report.
- `probe-craft.js`: 4/8 px grid discipline, type-scale steps and ratios, body size
  weighted by text volume, colour and depth systems, data-viz defects (invisible
  progress tracks, chart labels clipped by the SVG), genericness tells, use of width,
  input ergonomics, dark-mode / motion / touch / PWA support.
- `capture.py`: screenshot and probe matrix with real device emulation
  (mobile 390 / tablet 768 / desktop 1440 × light / dark) via Python Playwright.
- Bundled ux-ui-audit probes (MIT) for contrast, tap targets, Fitts, Hick, Gestalt.
- Browser tiers: Chrome DevTools MCP, Playwright MCP, `capture.py`, Claude desktop
  built-in browser (mobile preset), Claude in Chrome — each labelled in the report.
- Domain module for workout and fitness trackers.
- `DESIGN_PRINCIPLES.template.md` for projects that want a written standard.
