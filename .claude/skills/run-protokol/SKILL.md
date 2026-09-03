---
name: run-protokol
description: Build, run, and drive PROTOKOL (static single-file fitness-tracking PWA). Use when asked to start PROTOKOL, serve it locally, take a screenshot of its UI, test a change on a phone-sized viewport, or interact with the running app (tap a tab, log water/protein, complete a session).
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
- **Day-tab pills vs. the exercise-card heading collide on text.** The today
  tab shows both a `<button>Gün D ...</button>` pill and, once selected, an
  `<h2>Gün D · ...</h2>` card heading with overlapping text. Scope the
  selector to `button:has-text('Gün D')` (as `driver.py` does) or a bare
  `text=` locator will match the wrong (or both) elements.
- **The day-tab preview and the water tab both reset on tab switch/reload.**
  `selectedDayPreview` is in-memory JS state, not persisted — a `smoke` run
  that reloads mid-flow (to test water persistence) will already be back on
  the actual next day by the time you're done; don't assume the day-tab
  preview survives a reload in a longer flow.

## Troubleshooting

- **`playwright._impl._errors.TimeoutError` on `wait_for_selector("text=1
  şişe")`**: see the `.counter-value` gotcha above — fix the selector, not
  the app.
- **Driver hangs on `served()`**: something else is already listening on
  port 8934 but isn't serving PROTOKOL (stale unrelated server). Pass
  `--port` with a free port, or `lsof -ti:8934 -sTCP:LISTEN | xargs -r kill`
  first.
