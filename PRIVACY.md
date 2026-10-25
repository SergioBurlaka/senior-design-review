# Privacy

_Last updated: 2026-10-25_

**Senior Design Review** is a Claude plugin made of instructions and scripts. It has no
server, no account system, no analytics and no telemetry. The author receives no data from
anyone who uses it.

## What the plugin reads

When you ask Claude for a design review, the skill opens the web app **you** point it at
in a browser you control, and reads:

- the page's rendered text, structure and computed styles, through the bundled probe
  scripts that run inside that page;
- screenshots of the page at desktop and mobile sizes.

If the app is behind a login, these pages can contain personal data — for example names,
emails or customer records shown on screen. The skill does not look for personal data and
does not extract it on purpose, but whatever is on screen becomes part of your Claude
conversation, the same as anything else you show Claude.

## What it stores

Nothing outside your own machine and your Claude session.

- The review report stays in your conversation, or in a file or document you ask Claude to
  create.
- `scripts/capture.py`, if you run it, writes screenshots and probe results to a local
  folder you choose (default `review-shots/`).
- `capture.py --login` saves a browser session to a local `auth.json` file you name. It
  never stores your password. Treat that file like a password and keep it out of version
  control.
- During a review, the skill may keep a copy of its own probe code in the reviewed page's
  `localStorage` so it survives a reload, and removes it when the review ends.

## What it sends, and where

The plugin sends no data to the author or to any third-party service. Network traffic is
limited to:

- your browser loading the app you asked it to review;
- Claude itself, under your Claude plan's terms.

The skill never types your password and walks flows that write data only on a test
account or with your explicit go-ahead.

## Recommendations

- Prefer a test or staging account with non-sensitive data for reviews.
- Don't commit `auth.json` or `review-shots/` to a repository (both are in this
  repository's `.gitignore`).

## Children

The plugin is a developer tool and is not intended for users under 18.

## Contact

Questions or concerns: open an issue at
<https://github.com/SergioBurlaka/senior-design-review/issues>.
