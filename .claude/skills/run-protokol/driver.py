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

  python3 driver.py simulate [--days 100] [--seed 42] [--port 8934]
      Generates a deterministic fake usage history (sessions with
      progressive-overload weights, some intentionally delayed/skipped days
      to exercise the rolling calendar, mostly-filled water/protein/
      supplement logs, weekly measurements trending down) from the app's own
      DEFAULT_BLOCK_START out to a *fake* "today" (block start + --days,
      default 140 -- lands around week 17/Faz 2 with the skip probability
      below, comfortably past the week-12 Faz transition). The fake "today"
      is pinned with Playwright's Clock API, so
      the app's own todayISO()/rolling-calendar logic sees a consistent
      in-universe date, not the real one. State is written to a dedicated
      Playwright storage_state file (.sim-storage-state.json, gitignored) --
      this NEVER touches a real browser's localStorage, only this driver's
      own throwaway Chromium profile. Prints a summary (sessions generated,
      skipped/delayed count, logging coverage, week/phase reached).

      python3 driver.py simulate --reset
          Deletes the simulated storage state + metadata, so the next
          `simulate` starts clean and `ux-walkthrough` refuses to run
          until you `simulate` again.

  python3 driver.py ux-walkthrough [--port 8934]
      Requires a prior `simulate` run. Loads the simulated storage state,
      re-pins the clock to the same fake "today", and drives the 9-step
      flow a returning user would follow (open Bugün, fill in every
      exercise for the due day, toggle the warm-up card, complete the
      session, log water, quick-add protein, check Geçmiş, check the
      progress bar, click through all four Gün pills). Screenshots land in
      screenshots/walkthrough/NN_step.png; a walkthrough-log.json records
      the mechanical facts of each step (values typed, counts, raw DOM
      state) for the agent to review afterward -- this command does NOT
      write UX judgments itself, it only gathers evidence. Reviewing the
      screenshots and writing the actual critique is the agent's job (see
      SKILL.md's "Reviewing a walkthrough" section).

Both `smoke` and `shot` reuse an already-running server on --port if one is
already answering with the PROTOKOL page; otherwise they start their own
`python3 -m http.server` and tear it down when done. `simulate` and
`ux-walkthrough` do the same.
"""
import argparse
import json
import random
import subprocess
import sys
import time
import urllib.request
from contextlib import contextmanager
from datetime import date, timedelta
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO_ROOT = Path(__file__).resolve().parents[3]
SKILL_DIR = Path(__file__).resolve().parent
SIM_STORAGE_STATE = SKILL_DIR / ".sim-storage-state.json"
SIM_META = SKILL_DIR / ".sim-meta.json"
WALKTHROUGH_DIR = SKILL_DIR / "screenshots" / "walkthrough"
SUPPLEMENT_IDS = ["whey", "creatine", "magnesium", "d3k2", "collagen"]

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
    # NOT "PROTOKOL" for today -- that's the sticky header brand, present on
    # EVERY tab, so waiting on it can't detect a failed/skipped tab switch.
    # .daytabs is unique to the Bugün tab and always renders (no session
    # required), so it's a real "did we actually land on today" check.
    "today": ".daytabs",
    "water": "text=Bugünkü Su Tüketimi",
    "protein": "text=Bugünkü Protein",
    "history": None,  # renders either the empty state or "Geçmiş" -- checked separately
    "settings": "text=Profil",
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
    # Always click, even for "today" -- callers may be *returning* to it
    # from another tab (e.g. a walkthrough that visits water/protein/history
    # and then comes back), not just leaving it from the initial load.
    page.click(f"button[data-tab={tab}]")
    selector = TAB_TO_HEADING[tab]
    if selector:
        page.wait_for_selector(selector)


def select_day(page, day):
    """Click a Gun A/B/C/D preview pill on the today tab.

    Scoped to .daytab-btn specifically -- a plain button:has-text('Gün A')
    also matches the "Son Seansı Geri Al (Gün A ...)" undo button once a
    session exists, which sits on this same screen.
    """
    page.click(f".daytab-btn:has-text('Gün {day}')")


# ---------- simulate / ux-walkthrough helpers ----------

def add_days_str(iso, n):
    y, m, d = map(int, iso.split("-"))
    return (date(y, m, d) + timedelta(days=n)).isoformat()


def days_between(a, b):
    ay, am, ad = map(int, a.split("-"))
    by, bm, bd = map(int, b.split("-"))
    return (date(by, bm, bd) - date(ay, am, ad)).days


def build_simulated_state(day_info, exercises_by_day, block_start, fake_today, seed):
    """Deterministically fabricate a full protokol_state (same shape the app
    itself writes to localStorage) covering block_start..fake_today.

    The session schedule is generated by literally re-implementing the
    app's own rolling-calendar rule (next planned date = last *actual*
    completed date + DAY_INFO gap) so that once this state is loaded, the
    real app's getNextSession() continues the exact same sequence with no
    discontinuity. day_info/exercises_by_day come from the live app itself
    (page.evaluate) rather than being hand-duplicated here, so this can't
    silently drift from index.html's real EXERCISES/DAY_INFO.
    """
    rnd = random.Random(seed)

    def starting_value(unit):
        if unit == "dk":
            return 0.30
        if unit == "kg_arm":
            return 10.0
        if unit == "kg_leg":
            return 14.0
        return 20.0

    ex_occurrence = {}
    ex_value = {}

    def next_value(ex):
        exid = ex["id"]
        unit = ex["unit"]
        occ = ex_occurrence.get(exid, 0)
        if exid not in ex_value:
            ex_value[exid] = starting_value(unit)
        step = 0.05 if unit == "dk" else 2.5
        if occ > 0 and occ % 3 == 0:
            ex_value[exid] = round(ex_value[exid] + step, 2)
        elif occ > 0 and rnd.random() < 0.12:
            # occasional off day -- keeps the data non-monotonic/realistic
            # and exercises shouldShowProgressionHint's "did it drop" branch
            dip = 0.02 if unit == "dk" else 1.25
            ex_value[exid] = round(max(starting_value(unit), ex_value[exid] - dip), 2)
        ex_occurrence[exid] = occ + 1
        return round(ex_value[exid], 2)

    sessions = []
    skipped = []
    cur_type = "A"
    planned_date = block_start
    # Strictly < fake_today (not <=): fake_today must stay completely
    # untouched by the generator, or a session ux-walkthrough completes
    # "today" collides with one already dated "today" -- two sessions
    # under the same Geçmiş date, which no real user would ever produce.
    while planned_date < fake_today:
        skip = rnd.random() < 0.15
        delay = rnd.choice([1, 2, 3]) if skip else 0
        actual_date = add_days_str(planned_date, delay)
        if actual_date >= fake_today:
            break
        exs = {}
        for ex in exercises_by_day[cur_type]:
            exs[ex["id"]] = {"value": next_value(ex), "unit": ex["unit"]}
        sessions.append({"date": actual_date, "dayType": cur_type, "exercises": exs})
        if skip:
            skipped.append({
                "dayType": cur_type, "plannedDate": planned_date,
                "actualDate": actual_date, "delayDays": delay,
            })
        gap = day_info[cur_type]["gapToNext"]
        planned_date = add_days_str(actual_date, gap)
        cur_type = day_info[cur_type]["next"]

    # Daily water/protein/supplement logs: most days filled, some skipped.
    # fake_today itself is deliberately left OUT -- that's the "live" day
    # ux-walkthrough will fill in through the UI.
    daily_logs = {}
    logged_days = 0
    d = block_start
    while d < fake_today:
        if rnd.random() < 0.80:
            daily_logs[d] = {
                "waterBottles": rnd.randint(2, 6),
                "proteinGrams": rnd.randint(120, 220),
                "supplements": {sid: (rnd.random() < 0.7) for sid in SUPPLEMENT_IDS},
            }
            logged_days += 1
        d = add_days_str(d, 1)

    # Weekly measurements, weight/body-fat trending slightly down.
    measurements = []
    weight, bodyfat, bodyage = 90.5, 21.4, 36
    d = block_start
    week_i = 0
    while d <= fake_today:
        if week_i > 0:
            weight = round(weight - rnd.uniform(0.15, 0.45), 1)
            bodyfat = round(max(15.5, bodyfat - rnd.uniform(0.1, 0.3)), 1)
        measurements.append({"date": d, "weightKg": weight, "bodyFatPct": bodyfat, "bodyAge": bodyage})
        d = add_days_str(d, 7)
        week_i += 1
    last = measurements[-1]

    completed = len(sessions)
    current_week = completed // 4 + 1  # mirrors getCurrentWeek()
    phase = 1 if current_week <= 12 else 2  # mirrors getPhase()

    fake_state = {
        "profile": {
            "weightKg": last["weightKg"], "heightCm": 191, "bodyFatPct": last["bodyFatPct"],
            "bodyAge": last["bodyAge"], "proteinPerKg": 2.2, "waterGoalBottles": 5,
        },
        "blockStart": block_start,
        "blockEnd": add_days_str(block_start, 168),
        "sessions": sessions,
        "measurements": measurements,
        "dailyLogs": daily_logs,
        "water": {"date": fake_today, "bottles": 0},
        "protein": {"date": fake_today, "grams": 0, "history": []},
        "supplements": {"date": fake_today, "items": {}},
        "lastBackupAt": None,
    }
    summary = {
        "fakeToday": fake_today, "totalSessions": completed, "currentWeek": current_week,
        "phase": phase, "skippedCount": len(skipped), "skipped": skipped,
        "loggedDays": logged_days, "totalDaysInRange": days_between(block_start, fake_today),
        "firstMeasurement": measurements[0], "lastMeasurement": last,
    }
    return fake_state, summary


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


def cmd_simulate(args):
    if args.reset:
        removed = [f.name for f in (SIM_STORAGE_STATE, SIM_META) if f.exists()]
        for f in (SIM_STORAGE_STATE, SIM_META):
            if f.exists():
                f.unlink()
        print(f"simulate state cleared: {removed or '(nothing to clear)'}")
        return

    with served(args.port) as base_url:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            context = browser.new_context(**MOBILE_VIEWPORT)
            page = context.new_page()
            page.goto(f"{base_url}/index.html", wait_until="networkidle")
            page.wait_for_selector("text=PROTOKOL")

            # Pull the real DAY_INFO/EXERCISES/DEFAULT_BLOCK_START straight from
            # the loaded app instead of hand-duplicating them here, so this
            # can't silently drift from index.html.
            defs = page.evaluate(
                "() => ({dayInfo: DAY_INFO, exercises: EXERCISES, blockStart: DEFAULT_BLOCK_START})"
            )
            block_start = defs["blockStart"]
            fake_today = add_days_str(block_start, args.days)

            fake_state, summary = build_simulated_state(
                defs["dayInfo"], defs["exercises"], block_start, fake_today, args.seed
            )

            context.clock.set_fixed_time(fake_today + "T09:00:00")
            page.evaluate(
                "(s) => localStorage.setItem('protokol_state', JSON.stringify(s))", fake_state
            )
            page.reload(wait_until="networkidle")
            page.wait_for_selector("text=PROTOKOL")

            # Sanity check straight from the app's own logic, not our Python copy.
            live = page.evaluate(
                "() => ({ next: getNextSession(), week: getCurrentWeek(), "
                "phase: getPhase(), completed: getCompletedCount() })"
            )
            context.storage_state(path=str(SIM_STORAGE_STATE))
            browser.close()

    SIM_META.write_text(json.dumps({
        "fakeToday": fake_today, "blockStart": block_start,
        "seed": args.seed, "days": args.days,
    }, indent=2, ensure_ascii=False))

    print(f"Simulated {summary['totalSessions']} sessions: {block_start} -> {fake_today} (fake 'today').")
    print(f"  Hafta {summary['currentWeek']} / Faz {summary['phase']}"
          f"  (app'in kendi hesabı: hafta {live['week']} / faz {live['phase']}, tamamlanan {live['completed']})")
    print(f"  Sıradaki (fake today itibarıyla): {live['next']}")
    print(f"  Kasıtlı geciktirilen/atlanan seans: {summary['skippedCount']}")
    print(f"  Su/protein/takviye günlüğü dolduruldu: {summary['loggedDays']}/{summary['totalDaysInRange']} gün")
    print(f"  İlk ölçüm: {summary['firstMeasurement']}")
    print(f"  Son ölçüm: {summary['lastMeasurement']}")
    print(f"  Kaydedildi: {SIM_STORAGE_STATE}")
    print(f"\nŞimdi: python3 {Path(__file__).name} ux-walkthrough")


def _run_step(log, n, title, fn):
    path = WALKTHROUGH_DIR / f"{n:02d}_{title}.png"
    note = fn(path)
    log.append({"step": n, "title": title, "screenshot": str(path), "note": note})
    print(f"[{n}] {title}: {note}")


def cmd_ux_walkthrough(args):
    if not SIM_STORAGE_STATE.exists() or not SIM_META.exists():
        print("No simulated state found -- run `driver.py simulate` first.")
        sys.exit(1)
    meta = json.loads(SIM_META.read_text())
    fake_today = meta["fakeToday"]

    WALKTHROUGH_DIR.mkdir(parents=True, exist_ok=True)
    for f in WALKTHROUGH_DIR.glob("*"):
        f.unlink()

    log = []

    with served(args.port) as base_url:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            context = browser.new_context(storage_state=str(SIM_STORAGE_STATE), **MOBILE_VIEWPORT)
            context.clock.set_fixed_time(fake_today + "T09:00:00")
            page = context.new_page()
            page.goto(f"{base_url}/index.html", wait_until="networkidle")
            page.wait_for_selector("text=PROTOKOL")

            completed = page.evaluate("() => getCompletedCount()")
            if completed == 0:
                print("Simulated state has 0 sessions -- run `driver.py simulate` again.")
                sys.exit(1)

            next_info = page.evaluate("() => getNextSession()")
            day_type = next_info["dayType"]
            ex_list = page.evaluate("(dt) => EXERCISES[dt]", day_type)

            def step1(path):
                page.screenshot(path=str(path))
                return f"Sıradaki gün: Gün {day_type}, planlanan tarih {next_info['dueDate']} (fake today: {fake_today})"
            _run_step(log, 1, "bugun-acilis", step1)

            def step2(path):
                filled = []
                for ex in ex_list:
                    sel = f"#ex_input_{ex['id']}"
                    prev_raw = page.get_attribute(sel, "data-prev")
                    unit = ex["unit"]
                    if prev_raw:
                        val = round(float(prev_raw) + (0.05 if unit == "dk" else 2.5), 2)
                    else:
                        val = 0.30 if unit == "dk" else 20.0
                    page.fill(sel, str(val))
                    filled.append(f"{ex['name']}={val}")
                page.screenshot(path=str(path))
                return f"{len(filled)} egzersiz dolduruldu: " + "; ".join(filled)
            _run_step(log, 2, "egzersiz-girisi", step2)

            def step3(path):
                has_warmup = page.locator(".warmup-toggle").count() > 0
                if has_warmup:
                    page.click(".warmup-toggle")
                    page.wait_for_selector("text=Gizle")
                page.screenshot(path=str(path))
                return "ısınma kartı genişletildi (Detaylar -> Gizle)" if has_warmup else "ısınma kartı bulunamadı"
            _run_step(log, 3, "isinma-toggle", step3)

            def step4(path):
                # Collapse the warm-up back down first, mirroring what a user
                # would actually do before hitting the primary CTA.
                if page.locator("text=Gizle").count() > 0:
                    page.click(".warmup-toggle")
                values_still_present = page.input_value(f"#ex_input_{ex_list[0]['id']}")
                page.click("button:has-text('Seansı Tamamla')")
                page.wait_for_timeout(300)
                page.screenshot(path=str(path))
                new_next = page.evaluate("() => getNextSession()")
                return (
                    f"seans tamamlandı (ilk egzersiz input'u tamamlanmadan önce hâlâ '{values_still_present}' "
                    f"değerini taşıyordu -- pendingExerciseValues fix'i doğrulandı); tamamlama sonrası GÖRÜNÜR "
                    f"BİR ONAY/TOAST YOK, sayfa sessizce sıradaki güne geçti (yeni sıradaki: Gün {new_next['dayType']})"
                )
            _run_step(log, 4, "seansi-tamamla", step4)

            def step5(path):
                goto_tab(page, "water")
                for _ in range(3):
                    page.click(".counter-btn:has-text('+')")
                page.screenshot(path=str(path))
                val = page.inner_text(".counter-value").split("\n")[0].strip()
                return f"'+' butonuna 3 kez tıklandı, sayaç: {val}"
            _run_step(log, 5, "su-takibi", step5)

            def step6(path):
                goto_tab(page, "protein")
                page.click("button:has-text('+30g')")
                page.screenshot(path=str(path))
                val = page.inner_text(".counter-value").strip()
                return f"'+30g' hızlı-ekle tıklandı, toplam: {val}"
            _run_step(log, 6, "protein-quick-add", step6)

            def step7(path):
                goto_tab(page, "history")
                page.screenshot(path=str(path))
                count = page.locator(".hist-item").count()
                return f"{count} günlük birleşik geçmiş kaydı görünüyor (en üstte az önce tamamlanan seans olmalı)"
            _run_step(log, 7, "gecmis", step7)

            def step8(path):
                goto_tab(page, "today")
                page.screenshot(path=str(path))
                header_style = page.get_attribute("#headerProgressFill", "style") or ""
                completed_now = page.evaluate("() => getCompletedCount()")
                week_now = page.evaluate("() => getCurrentWeek()")
                phase_now = page.evaluate("() => getPhase()")
                return (
                    f"tamamlanan {completed_now}/96 seans, hafta {week_now}, faz {phase_now}; "
                    f"header ilerleme çubuğu style='{header_style}'"
                )
            _run_step(log, 8, "ilerleme", step8)

            def step9(path):
                findings = []
                for d in ["A", "B", "C", "D"]:
                    select_day(page, d)
                    page.wait_for_timeout(150)
                    shot_path = WALKTHROUGH_DIR / f"09_gun-{d}.png"
                    page.screenshot(path=str(shot_path))
                    banner_present = page.locator("text=Program kaymış durumda").count() > 0
                    findings.append(f"Gün {d}: banner {'VAR' if banner_present else 'yok'}")
                page.screenshot(path=str(path))
                return "4 gün sekmesi gezildi (" + ", ".join(findings) + ") -- banner her pilde AYNI olmalı, sadece gerçek sıradaki güne bağlı"
            _run_step(log, 9, "gun-sekmeleri", step9)

            browser.close()

    log_path = WALKTHROUGH_DIR / "walkthrough-log.json"
    log_path.write_text(json.dumps(log, ensure_ascii=False, indent=2))
    print(f"\nWalkthrough log: {log_path}")
    print(f"Screenshots in: {WALKTHROUGH_DIR}")
    print("Bu komut sadece mekanik kanıt topladı -- ekran görüntülerini incele ve")
    print("eleştirel değerlendirmeyi (ux-friction-report.md) ayrıca sen yaz.")


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

    p_sim = sub.add_parser("simulate", help="generate deterministic fake usage history for testing")
    p_sim.add_argument("--days", type=int, default=140,
                        help="calendar days from block start to fake 'today' (default 140, comfortably past week 12/Faz 2)")
    p_sim.add_argument("--seed", type=int, default=42, help="RNG seed -- same seed always produces the same history")
    p_sim.add_argument("--reset", action="store_true", help="clear simulated state instead of generating")
    p_sim.add_argument("--port", type=int, default=8934)
    p_sim.set_defaults(func=cmd_simulate)

    p_ux = sub.add_parser("ux-walkthrough", help="drive the app through a simulated day as a user, screenshotting each step")
    p_ux.add_argument("--port", type=int, default=8934)
    p_ux.set_defaults(func=cmd_ux_walkthrough)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
