# MyGym — Design review (sample output, abridged)

A real run of `senior-design-review` against [MyGym](https://my-gym-com.duckdns.org/),
a workout tracker, on 2026-10-25. Abridged to show the shape of the output; the full
report has twelve findings.

Scope: Journal, Programs, Progress, Exercises, workout editor · desktop 1440×900 and
mobile 375×812 · dark theme only · browser tier B (Claude desktop built-in browser,
mobile preset: Android UA, coarse pointer, DPR 2) · read-only on a real account ·
standards: skill defaults (no project brief found) · fitness domain module applied.

## Verdict

MyGym does not look like a template. Bebas Neue headings, an orange brand mark, a
consistency calendar and the "N/M sessions to progress" mechanic give it a face of
its own, which is rare for a developer's side project.

Three things hold it back. Colour carries no meaning: the accent, the "missed" red,
the progress green and five more hues are mixed, and progress towards the next weight
is drawn in almost the same red as a missed day. In the workout editor the destructive
controls outweigh the data and the primary action. On mobile the journal is genuinely
recomposed, but navigation hides in a hamburger and "+ New workout" scrolls away.

## Scorecard

| Axis | Score | Why |
| --- | --- | --- |
| Identity | 4 | Own display type, brand colour, domain-specific calendar |
| Hierarchy & clarity | 3 | Journal reads well; editor puts destructive actions above data |
| Typography | 3 | 6 sizes, 3 weights; but 12 px body on two screens |
| Spacing & rhythm | 3 | 98 % on the 4 px grid on Programs, 57 % on Exercises |
| Colour & theme | 2 | Correct dark theme; 8 saturated hues, accent ≈ danger |
| States & feedback | 2 | No `:active` or `:focus-visible` rules; no reduced-motion |
| Mobile composition | 3 | Journal recomposed; nav in hamburger, CTA at the top |
| Desktop composition | 2 | Mobile lists in a 1024 px column; no planning surface |

## Top priorities (impact ÷ effort)

1. Action hierarchy in the workout editor — sticky Save, Delete/Remove into ⋮ with undo.
2. Colour semantics — accent for actions only, green for progress, red only for missed/delete.
3. Inputs fit for a thumb — 16 px font, ≥ 44 px height, ±2.5 kg steppers.
4. Chart axes — wider left margin, "12k" format, "kg" unit.

## Selected findings

### F04 · Workout editor · mobile — severity 3 · effort S–M · measured + observed
**Claim.** "Save as program", "Delete" and "Save" share one row at the top at equal
size; the disabled Save is a faded orange-red that reads as destructive.
**Why it matters here.** Delete next to Save at the same weight is one mis-tap from
losing a workout, and the row sits at y = 202 of 812 — out of thumb reach.
**Recommendation.** A sticky bottom bar with one filled Save (neutral grey when
disabled); Delete in an overflow menu with confirm or undo.

### F05 · Workout editor · mobile — severity 3 · effort S · measured
**Claim.** The most prominent text on each exercise card is a red "Remove" on its own
row; the remove-set "×" buttons are 11×24 px and sit against the reps inputs.
**Recommendation.** "Remove" into the card's ⋮ menu; "×" with a 44×44 hit area and
≥ 8 px gap, or swipe-to-delete with an undo toast.

### F02 · Journal — severity 2 · effort S · measured
**Claim.** The progress-bar track is the same colour as its row (rgb 42,47,58 on
rgb 42,47,58, contrast 1:1), so only the 16×6 px fill shows.
**Why it matters here.** A 25 % bar reads as a stray red dash after the text.
**Recommendation.** A track ≥ 1.5:1 against its row, or ●○○○ segments for 4–6 steps.

### F01 · Progress chart · desktop and mobile — severity 2 · effort S · measured
**Claim.** Y-axis labels 3000–12000 start 3–8 px left of an SVG with
`overflow: hidden` and are clipped; the axis has no unit.
**Recommendation.** Left margin ≥ 40 px, "12k" format, an axis title in kg.

## What works

- **A face of its own.** No genericness tells found (no nested cards, emoji icons or
  purple gradients).
- **A correct dark theme.** Page #14171C, raised surfaces lighter, no pure black.
- **A recomposed mobile journal.** Value bold on the right, name left, detail smaller —
  readable at arm's length.
- **Right keyboards.** Weight `inputmode=decimal`, reps `numeric`.

## Not verified

The live workout (core logging loop) was not walked because it writes data: tap count
per set, previous values per row, auto-starting rest timer, Wake Lock, offline logging
(no service worker controls the page), resume after reload, PR and end-of-workout
moments. Plus a real-phone pass for iOS input zoom, keyboard overlap and safe areas.
