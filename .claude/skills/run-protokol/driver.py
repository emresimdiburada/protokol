#!/usr/bin/env python3
"""Driver for running / driving PROTOKOL (static single-file PWA) headlessly.

PROTOKOL has no build step and no dev server of its own -- it's index.html +
service-worker.js served as static files. This driver serves the repo root
with `python3 -m http.server`, drives it with Playwright's Chromium in a
mobile viewport, and can screenshot it or run the full smoke flow.

Why Playwright and not chromium-cli / macOS screencapture: this machine has
no `node`/`chromium-cli`, and `screencapture` fails here with "could not
create image from display" because the Terminal process running this driver
lacks Screen Recording permission -- and granting it only takes effect after
Terminal.app is fully quit and relaunched, which would kill the session
driving this driver. Playwright renders offscreen via CDP, so it needs
neither and is unaffected by that permission. See SKILL.md Gotchas.

Usage:
  python3 driver.py smoke [--port 8934]
      Serves the app, runs the full smoke flow (today tab renders, a day-tab
      preview shows the read-only note, the water counter increments and
      *persists across a reload*), saves screenshots into ./screenshots/,
      and prints one PASS/FAIL line per step plus any browser console errors.

  python3 driver.py shot <output.png> [--tab today|water|protein|history|settings]
                                       [--day A|B|C|D] [--port 8934]
      Serves the app, navigates to one tab (optionally selecting one of the
      Gun A/B/C/D preview pills on the today tab first), and saves a single
      mobile-viewport screenshot to <output.png>.

Both commands reuse an already-running server on --port if one is already
answering with the PROTOKOL page; otherwise they start their own
`python3 -m http.server` and tear it down when done.
"""
import argparse
import subprocess
import sys
import time
import urllib.request
from contextlib import contextmanager
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO_ROOT = Path(__file__).resolve().parents[3]

MOBILE_VIEWPORT = {
    "viewport": {"width": 390, "height": 844},
    "device_scale_factor": 3,
    "user_agent": (
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
    ),
    "is_mobile": True,
    "has_touch": True,
}

TAB_TO_HEADING = {
    "today": "PROTOKOL",  # today always renders; header brand is the stable anchor
    "water": "Bugünkü Su Tüketimi",
    "protein": "Bugünkü Protein",
    "history": None,  # renders either the empty state or "Geçmiş" -- checked separately
    "settings": "Profil",
}


def _server_is_up(port):
    try:
        with urllib.request.urlopen(f"http://localhost:{port}/index.html", timeout=1) as r:
            return b"PROTOKOL" in r.read()
    except Exception:
        return False


@contextmanager
def served(port):
    """Yield the base URL. Reuses an already-running server on `port` if one
    already serves this app; otherwise starts and tears down our own."""
    if _server_is_up(port):
        yield f"http://localhost:{port}"
        return

    proc = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(port), "--directory", str(REPO_ROOT)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        deadline = time.time() + 10
        while time.time() < deadline:
            if _server_is_up(port):
                break
            time.sleep(0.2)
        else:
            raise RuntimeError(f"server on port {port} never came up")
        yield f"http://localhost:{port}"
    finally:
        proc.terminate()
        proc.wait(timeout=5)


@contextmanager
def page_session(base_url):
    """Yield (page, errors) -- errors is a list that fills with console
    'error' messages and uncaught page exceptions as they happen."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(**MOBILE_VIEWPORT)
        page = context.new_page()
        errors = []
        page.on("console", lambda m: errors.append(f"console.error: {m.text}") if m.type == "error" else None)
        page.on("pageerror", lambda exc: errors.append(f"pageerror: {exc}"))
        page.goto(f"{base_url}/index.html", wait_until="networkidle")
        page.wait_for_selector("text=PROTOKOL", timeout=5000)
        try:
            yield page, errors
        finally:
            browser.close()


def goto_tab(page, tab):
    if tab != "today":
        page.click(f"button[data-tab={tab}]")
    heading = TAB_TO_HEADING[tab]
    if heading:
        page.wait_for_selector(f"text={heading}")


def select_day(page, day):
    """Click a Gun A/B/C/D preview pill on the today tab."""
    page.click(f"button:has-text('Gün {day}')")


def cmd_shot(args):
    with served(args.port) as base_url, page_session(base_url) as (page, errors):
        goto_tab(page, args.tab)
        if args.day:
            select_day(page, args.day)
        page.screenshot(path=args.output)
        print(f"saved {args.output}")
        if errors:
            print("console errors:", errors)


def cmd_smoke(args):
    out_dir = Path(__file__).resolve().parent / "screenshots"
    out_dir.mkdir(exist_ok=True)
    failures = []

    with served(args.port) as base_url, page_session(base_url) as (page, errors):
        def check(label, fn):
            try:
                fn()
                print(f"PASS  {label}")
            except Exception as e:
                print(f"FAIL  {label}: {e}")
                failures.append(label)

        check("today tab renders", lambda: page.wait_for_selector("text=PROTOKOL"))
        page.screenshot(path=str(out_dir / "today.png"))

        check(
            "day-tab preview shows read-only note",
            lambda: (select_day(page, "D"), page.wait_for_selector("text=önizleme modundasın")),
        )
        page.screenshot(path=str(out_dir / "preview_D.png"))

        check("water tab renders", lambda: goto_tab(page, "water"))
        check(
            "water counter increments",
            lambda: (
                page.click(".counter-btn:has-text('+')"),
                page.wait_for_function(
                    "document.querySelector('.counter-value').textContent.trim().startsWith('1')"
                ),
            ),
        )
        check(
            "water count persists across reload",
            lambda: (
                page.reload(wait_until="networkidle"),
                goto_tab(page, "water"),
                page.wait_for_function(
                    "document.querySelector('.counter-value').textContent.trim().startsWith('1')"
                ),
            ),
        )
        page.screenshot(path=str(out_dir / "water.png"))

        print("console errors:", errors if errors else "none")

    if failures:
        print(f"\n{len(failures)} step(s) failed: {failures}")
        sys.exit(1)
    print(f"\nAll steps passed. Screenshots in {out_dir}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_smoke = sub.add_parser("smoke", help="run the full smoke flow")
    p_smoke.add_argument("--port", type=int, default=8934)
    p_smoke.set_defaults(func=cmd_smoke)

    p_shot = sub.add_parser("shot", help="screenshot one tab")
    p_shot.add_argument("output")
    p_shot.add_argument("--tab", choices=list(TAB_TO_HEADING), default="today")
    p_shot.add_argument("--day", choices=["A", "B", "C", "D"], default=None)
    p_shot.add_argument("--port", type=int, default=8934)
    p_shot.set_defaults(func=cmd_shot)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
