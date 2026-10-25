<h1 align="center">Senior Design Review</h1>

<p align="center">
  A Claude skill that reviews your <b>live</b> web app the way an experienced product designer would —<br>
  on desktop <b>and</b> on mobile, with measured evidence behind every finding.
</p>

<p align="center">
  <a href="#install">Install</a> ·
  <a href="#use">Use</a> ·
  <a href="examples/sample-report-mygym.md">Sample report</a> ·
  <a href="README.uk.md">Українською</a>
</p>

---

Linters and accessibility audits tell you a contrast ratio is 3.1:1. They don't tell you that
your app *looks developer-made*, that red means three different things, that the delete button
outweighs the data, or that your mobile layout is a desktop page squeezed into 375 px.

This skill does. It opens your running app in a real browser, emulates a phone and a desktop,
measures what can be measured, and then judges the rest like a senior designer would — in the
context the product is actually used in.

## What you get

A report that reads like a design critique, not a checklist:

- **Verdict** — what the product gets right, the one or two things holding it back, and how far it
  is from feeling crafted.
- **Scorecard** — per axis (hierarchy, typography, spacing, colour, states, mobile, desktop,
  identity, domain fit). Never a single total.
- **Top priorities** — ranked by impact ÷ effort.
- **Findings** — each with a claim, why it matters *here*, evidence, the principle it breaks,
  Nielsen severity 0–4, effort S/M/L, a before → after fix, and its basis:
  `measured` (a probe number), `observed` (a named screenshot) or `judged` (an argued opinion).
- **What works**, and **what to verify on a real device**.

See a real one: [MyGym review](examples/sample-report-mygym.md).

## How it works

| Layer | What it does |
| --- | --- |
| **Eyes** | Picks the best browser available and says which: Chrome DevTools MCP or Playwright MCP (true device emulation), the bundled `capture.py`, Claude's desktop built-in browser, or Claude in Chrome. A narrow desktop window is labelled as an approximation, never passed off as a phone. |
| **Metrics** | `probe-craft.js` — 4/8 px grid discipline, type-scale ratios, body size and measure, colour semantics, depth, invisible progress tracks, clipped chart labels, genericness tells (default font, purple gradients, nested cards, emoji icons), use of width, input ergonomics (iOS zoom, decimal input). Plus contrast, tap targets, Fitts, Hick and Gestalt probes from [ux-ui-audit](NOTICE.md). |
| **Taste** | Designer passes: first impression (5-second, squint and "could another product ship this?" tests), visual craft, identity, states and motion, mobile recomposition vs desktop composition, emotional peaks. Then a second look from a design director's seat and from the real user's. |
| **Domain** | A module for workout and fitness trackers (tap budget per set, readability at arm's length, rest timers, offline in the gym, PR moments). The module is a template for adding your own domain. |
| **Your standard** | If your repo has a `DESIGN_PRINCIPLES.md`, its rules outrank the skill's defaults and each finding cites the rule it breaks. A [template](skills/senior-design-review/assets/DESIGN_PRINCIPLES.template.md) is included. |

## Install

### Claude Code

```bash
claude plugin marketplace add SergioBurlaka/senior-design-review
claude plugin install senior-design-review@sergioburlaka
```

Or inside a session: `/plugin install senior-design-review --marketplace SergioBurlaka/senior-design-review`.

Update later with `claude plugin update senior-design-review@sergioburlaka`.

**Recommended:** give the skill true mobile emulation with Chrome DevTools MCP:

```bash
claude mcp add chrome-devtools --scope user -- npx chrome-devtools-mcp@latest --autoConnect
```

### Claude apps (claude.ai, desktop, mobile)

1. Download `senior-design-review.zip` from the [latest release](https://github.com/SergioBurlaka/senior-design-review/releases/latest).
2. In Claude, open **Customize → Skills**, choose **Add** and upload the zip (code execution must be on).
3. Enable the skill.

In the Claude desktop app the skill drives the built-in browser, and its mobile preset emulates a
phone user agent and coarse pointer.

### Just the folder

Copy `skills/senior-design-review/` into `~/.claude/skills/` (all projects) or `.claude/skills/`
in one repository.

## Use

Ask in your own words — the skill triggers on design-review intent:

```text
Do a design review of https://staging.myapp.com on desktop and mobile
Does our checkout look professional? Be honest.
Review only the Progress screen on mobile, as a designer would
I fixed F02–F05 — check those spots again and compare with the last report
```

Tips:

- **Logged-in apps.** The skill never types your password. Sign in yourself in the browser it uses
  (DevTools MCP `--autoConnect` attaches to your own Chrome), or save a session once with
  `python3 skills/senior-design-review/scripts/capture.py --login <url> --storage-state auth.json`. Prefer a test account —
  everything on screen goes into the model's context.
- **Flows that write data** (checkout, starting a workout) are walked only on a test account or
  with your go-ahead; otherwise the report lists them under "not verified".
- **Local dev servers** work too, and are the safest place to walk write flows.

## Repository layout

```text
.claude-plugin/
  plugin.json            plugin manifest
  marketplace.json       makes this repo installable as a marketplace
skills/senior-design-review/
  SKILL.md               the review flow
  references/            visual craft, responsive & browser tiers, states & motion,
                         fitness domain module, report template
  scripts/               probe-craft.js, capture.py, ux-ui-audit probes (MIT)
  assets/                DESIGN_PRINCIPLES.template.md
examples/                sample report
tests/                   probe regression tests (Playwright + pytest)
scripts/build_release.py builds the claude.ai zip
```

## Develop

```bash
pip install playwright pytest pyyaml && python -m playwright install chromium
pytest tests                              # probe regression tests
claude plugin validate --strict .         # manifests
python3 scripts/build_release.py          # dist/senior-design-review.zip
```

To release: raise `version` in `.claude-plugin/plugin.json`, add a `CHANGELOG.md` entry, then tag
`vX.Y.Z` — the release workflow builds the archives and publishes the GitHub release.

Contributions are welcome, especially new **domain modules** (e-commerce, dashboards, booking,
content apps): copy `references/domain-fitness.md`, keep its sections, and add a fixture-backed
test for any new probe check.

## Limits

- Emulation is Chromium. iOS Safari quirks (`100vh`, input zoom, safe areas on a real notch, PWA
  standalone) need a real device; the report lists them separately.
- Severity from a single reviewer is an estimate. Treat the report as a strong second opinion,
  not a verdict from your design team.

## Privacy

The plugin has no server and sends no data to its author or any third party. It reads the pages you ask it to review; see [PRIVACY.md](PRIVACY.md).

## Licence

[MIT](LICENSE). Bundles probe scripts from **ux-ui-audit** by UXBYISSA under MIT — see [NOTICE.md](NOTICE.md).
