---
name: run-protokol
description: Build, run, and drive PROTOKOL (static single-file fitness-tracking PWA). Use when asked to start PROTOKOL, serve it locally, take a screenshot of its UI, test a change on a phone-sized viewport, interact with the running app (tap a tab, log water/protein, complete a session), generate fake usage history for testing, or run/review a UX walkthrough.
---

PROTOKOL is a single static `index.html` (plus `service-worker.js`) with no
build step and no framework — all state lives in `localStorage`. Drive it
with `.claude/skills/run-protokol/driver.py`, a Playwright-based headless
Chromium driver that serves the file over HTTP, opens it in a real mobile
viewport, and can screenshot it or run a full interaction smoke test. This
does not use `screencapture`/macOS screenshots and does not need Screen
Recording permission — see Gotchas.

All paths below are relative to `protokol/` (repo root).

## Prerequisites

```bash
pip3 install playwright
python3 -m playwright install chromium
```

(Already satisfied on this machine — `playwright` 1.60.0 and a Chromium
build were both already present under `~/Library/Caches/ms-playwright/`.)

## Build

None — `index.html` is served as-is, no compile step.

## Run (agent path)

```bash
python3 .claude/skills/run-protokol/driver.py smoke
```

This serves the repo root on `localhost:8934` (reusing a server already
running there if one already answers with the PROTOKOL page, otherwise
starting and tearing down its own `python3 -m http.server`), then in one
headless Chromium session with an iPhone-sized viewport (390×844, 3x DSF,
mobile UA, touch enabled):

1. loads the Bugün (today) tab
2. clicks the "Gün D" day-tab pill and confirms the read-only preview note
   appears (proves the rolling-schedule guard against out-of-order
   completion works)
3. switches to the Su (water) tab, taps `+`, confirms the counter reads 1
4. **reloads the page** and confirms the water count survived — this is the
   one that actually matters, since the whole app's state model is
   `localStorage`, and Playwright's browser context keeps it across a
   reload the same way a real browser tab does

It prints one `PASS`/`FAIL` line per step, any browser console errors, and
saves screenshots to `.claude/skills/run-protokol/screenshots/` (`today.png`,
`preview_D.png`, `water.png`). Exits non-zero if any step failed.

For a single screenshot of one tab:

```bash
python3 .claude/skills/run-protokol/driver.py shot /tmp/out.png --tab settings
python3 .claude/skills/run-protokol/driver.py shot /tmp/out.png --tab today --day C
```

| flag | values | effect |
|---|---|---|
| `--tab` | `today`\|`water`\|`protein`\|`history`\|`settings` | which bottom tab to land on |
| `--day` | `A`\|`B`\|`C`\|`D` | on the today tab, click that Gün pill first (previews that day; only meaningful with `--tab today`) |
| `--port` | int, default `8934` | server port |

### `simulate` — deterministic fake usage history

```bash
python3 .claude/skills/run-protokol/driver.py simulate            # days=140, seed=42
python3 .claude/skills/run-protokol/driver.py simulate --days 200 --seed 7
python3 .claude/skills/run-protokol/driver.py simulate --reset    # clear it
```

Generates a full `protokol_state` (sessions with progressive-overload
weights, ~15% of sessions intentionally delayed 1-3 days to exercise the
rolling calendar, ~80% of days logged for water/protein/supplements,
weekly measurements trending the weight/body-fat down) from the app's own
`DEFAULT_BLOCK_START` out to a **fake "today"** (`block start + --days`).
`--days 140` was picked empirically to land around week 16-17 (Faz 2) with
the default 15% skip rate — comfortably past the week-12 phase transition
so that's actually reachable to test. Same `--seed` always reproduces the
exact same history (Python's `random.Random(seed)`).

The fake "today" is pinned across the whole browser context with
Playwright's Clock API (`context.clock.set_fixed_time(...)`), so the app's
own `todayISO()` / rolling-calendar math sees a self-consistent in-universe
date — not the real one. `DAY_INFO`/`EXERCISES` are pulled live from the
loaded app via `page.evaluate` rather than hand-duplicated in Python, so
the generator can't silently drift from `index.html`.

State is written to `.claude/skills/run-protokol/.sim-storage-state.json`
(a Playwright `storage_state` file — cookies + localStorage) plus a small
`.sim-meta.json` recording the fake-today date. Both are gitignored and
**never touch a real browser's storage** — this is this driver's own
throwaway Chromium profile, not Safari. `simulate --reset` deletes both.

Prints a summary: sessions generated, skipped/delayed count, water/protein/
supplement logging coverage, week/phase reached, first/last measurement.

### `ux-walkthrough` — drive it as a returning user, screenshot every step

```bash
python3 .claude/skills/run-protokol/driver.py simulate   # must run first
python3 .claude/skills/run-protokol/driver.py ux-walkthrough
```

Requires a prior `simulate` run (refuses with a clear message otherwise).
Loads `.sim-storage-state.json`, re-pins the clock to the same fake
"today" from `.sim-meta.json`, and drives the 9-step flow a returning user
follows: open Bugün → fill every exercise for the due day (bumping each
from its real previous value, read off `data-prev`) → toggle the warm-up
card open → complete the session → log 3 water bottles → quick-add 30g
protein → check Geçmiş → check the progress bar/week/phase → click through
all four Gün pills checking the "Program kaymış" banner stays constant.

Screenshots land in `screenshots/walkthrough/NN_step.png` (plus one shot
per Gün pill in step 9). A `walkthrough-log.json` next to them records the
**mechanical facts only** of each step (values typed, click counts, raw
button/attribute state) — it does not contain UX judgments. See "Reviewing
a walkthrough" below for what to do with it.

## Reviewing a walkthrough

`ux-walkthrough` only gathers evidence — it cannot judge whether a label
was confusing or a confirmation was missing, that takes actual reasoning.
After running it:

1. Read `screenshots/walkthrough/walkthrough-log.json` for the mechanical
   facts (what was typed/clicked/observed).
2. Look at every `NN_*.png` screenshot yourself.
3. Write the critique against these four angles (this is the checklist a
   prior review used, in `ux-friction-report.md` at repo root):
   - Where was it unclear what to do (ambiguous label/icon/location)?
   - Where did something take more clicks/steps than it should?
   - Where was feedback missing (unclear whether a save/action succeeded)?
   - What information should have been visible but was buried/hidden?
4. Reference specific screenshot filenames as evidence for each finding —
   a claim like "no confirmation after completing a session" should point
   at the exact screenshot that shows it.

Don't just re-describe what the log already says mechanically ("clicked
the + button 3 times") — that's not a finding, it's an action. A finding
is a judgment about whether that action's *result* was clear, fast, and
well-communicated.

## Run (human path)

```bash
python3 -m http.server 8934 --directory .
```

Then open `http://localhost:8934/index.html` in a real browser. Useless
headless — this is the manual-testing path, not the agent path. To test on
an actual phone on the same LAN instead of a resized desktop window:

```bash
ipconfig getifaddr en0   # -> e.g. 192.168.1.156
```

then open `http://<that-ip>:8934/` from the phone.

## Test

No test suite — this is a single static HTML file. `driver.py smoke` (above)
is the closest thing to one; treat it as the regression check after editing
`index.html`.

---

## Gotchas

- **Don't reach for macOS `screencapture` here.** It fails with `could not
  create image from display` unless the Terminal process has Screen
  Recording permission — and macOS only applies a freshly-granted Screen
  Recording permission after the granted app (Terminal.app) is fully quit
  and relaunched. Since Terminal.app is the root process of this whole
  Claude Code session, that restart would kill the session driving the
  screenshot. Playwright sidesteps this entirely: it renders offscreen over
  CDP, so it needs no screen-capture permission and is unaffected by this.
- **No `node` / `chromium-cli` on this machine.** The generic web-app
  pattern (`chromium-cli`) isn't available here — `driver.py` uses the
  Python `playwright` package directly instead (already installed).
- **`.counter-value` text has no space before the unit.** The water/protein
  counters render as `'<div class="counter-value">' + n + '<small>şişe
  ...</small></div>' ` — no literal space between the number and the
  `<small>` text node, so a Playwright `text=1 şişe` locator times out even
  though it's visually on separate lines (CSS `display:block`). Match on
  `.counter-value` content instead (`driver.py` uses
  `page.wait_for_function` checking `textContent.trim().startsWith('1')`).
- **Three different elements can all contain "Gün D" text.** The today tab
  has a `<button class="daytab-btn">Gün D ...</button>` pill, an
  `<h2>Gün D · ...</h2>` card heading once selected, AND (once ≥1 session
  exists) a `<button>↩ Son Seansı Geri Al (Gün D · ...)</button>` undo
  button — all on the same screen. A bare `button:has-text('Gün D')`
  matched the undo button in a real run once `select_day()`/`step9` had
  simulated history loaded, silently clicking it (dismissed by Playwright's
  default auto-cancel of the resulting `confirm()`) instead of the day
  pill. Always scope to `.daytab-btn:has-text('Gün D')` — `select_day()` in
  `driver.py` does this now.
- **`goto_tab()` must always click, even for "today."** It used to skip the
  click when `tab == "today"` (reasoning: that's the initial tab, no click
  needed) and check readiness via `text=PROTOKOL` — but that's the sticky
  header brand, present on *every* tab, so returning to "today" from
  water/protein/history silently failed to switch tabs and the stale
  readiness check passed anyway. Fixed by always clicking
  `button[data-tab=...]` and checking a tab-specific marker (`.daytabs` for
  today, since the header brand can't tell tabs apart). This is exactly
  the kind of thing a `ux-walkthrough` run surfaces that a single-tab
  `smoke`/`shot` never would, since those never need to *return* to today.
- **The day-tab preview and the water tab both reset on tab switch/reload.**
  `selectedDayPreview` is in-memory JS state, not persisted — a `smoke` run
  that reloads mid-flow (to test water persistence) will already be back on
  the actual next day by the time you're done; don't assume the day-tab
  preview survives a reload in a longer flow.
- **`simulate`'s schedule generator must stop strictly *before* the fake
  "today,"** not on-or-before it. `while planned_date <= fake_today` let
  the last fabricated session land exactly on fake-today; then
  `ux-walkthrough` completes a session dated fake-today too (via the app's
  own `todayISO()`), producing two sessions under the same Geçmiş date —
  something a real user could never do. Use `< fake_today` for the loop
  and `>= fake_today` for the break check, so fake-today is always
  untouched before the walkthrough starts.
- **Playwright's Clock survives `page.reload()` and separate process runs
  (via `storage_state`), but must be re-armed each time a new browser
  launches.** `simulate` sets it once before injecting localStorage;
  `ux-walkthrough` is a *separate* `driver.py` invocation/process, so it
  must independently call `context.clock.set_fixed_time(...)` again with
  the same date (read from `.sim-meta.json`) — the fixed time itself isn't
  part of `storage_state` and doesn't carry over on its own.

## Troubleshooting

- **`playwright._impl._errors.TimeoutError` on `wait_for_selector("text=1
  şişe")`**: see the `.counter-value` gotcha above — fix the selector, not
  the app.
- **Driver hangs on `served()`**: something else is already listening on
  port 8934 but isn't serving PROTOKOL (stale unrelated server). Pass
  `--port` with a free port, or `lsof -ti:8934 -sTCP:LISTEN | xargs -r kill`
  first.
- **`ux-walkthrough` exits with "No simulated state found"**: run
  `driver.py simulate` first — it depends on `.sim-storage-state.json` +
  `.sim-meta.json` existing.
- **Two sessions under the same date in a `simulate`-generated history**:
  you're on an old build of `driver.py` with the off-by-one boundary bug
  (`<=` instead of `<` against fake-today) — see the matching Gotcha above.
  `simulate --reset && simulate` regenerates clean.
