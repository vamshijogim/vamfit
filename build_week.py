# -*- coding: utf-8 -*-
"""Insert one new week on top of Diet Plan + Exercise Plan in Vamshi's Fitness Tracker (RESTART plan, 2026-10-22).

Usage (from this folder):  python build_week.py <week_no> "<Mon d, yyyy>" ["<trainer note>"]
  e.g.  python build_week.py 2 "Nov 2, 2026" "Oct 30 weigh-in 200.9 (Good pace). Normal progression."
Week 1 = WEEK OF Oct 26, 2026 (already in the sheet). Week n's Monday = Oct 26 + 7*(n-1) days.
Backs up the workbook to %TEMP%, inserts both blocks, recalcs with LibreOffice, verifies every day
(<= 2050 cal, >= 150 g protein) and copies the recalculated file back. Never edits older blocks.
"""
import sys, os, shutil, subprocess, tempfile, datetime
from copy import copy
import openpyxl
from openpyxl.formula.translate import Translator
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from plan_library import MEALS, DAYS, meal_totals, day_plan, YOGA, YOGA_RULES, SCHEDULE, WALL, YT

Q = r"C:\Users\vamsh\OneDrive\Personal\3. Reference\Personal\Health-Wellness\Vamshi Fitness Tracker\Vamshi - Fitness Tracker.xlsx"
SOFFICE = r"C:\Program Files\LibreOffice\program\soffice.exe"


def shift_down(ws, start, n):
    affected = [m for m in list(ws.merged_cells.ranges) if m.min_row >= start]
    coords = [(m.min_row, m.min_col, m.max_row, m.max_col) for m in affected]
    for m in affected:
        ws.unmerge_cells(str(m))
    maxc = ws.max_column
    for r in range(ws.max_row, start - 1, -1):
        for c in range(1, maxc + 1):
            s, d = ws.cell(r, c), ws.cell(r + n, c)
            v = s.value
            if isinstance(v, str) and v.startswith("="):
                v = Translator(v, origin=s.coordinate).translate_formula(d.coordinate)
            d.value, d._style = v, copy(s._style)
            d.hyperlink = s.hyperlink.target if s.hyperlink else None
            s.value, s.hyperlink = None, None
        ws.row_dimensions[r + n].height = ws.row_dimensions[r].height
        ws.row_dimensions[r].height = None
    for a, b, c2, d2 in coords:
        ws.merge_cells(start_row=a + n, start_column=b, end_row=c2 + n, end_column=d2)


def grab(ws, r, ncol):
    return [copy(ws.cell(r, c)._style) for c in range(1, ncol + 1)], ws.row_dimensions[r].height


def put(ws, r, style, values, links=None, height="keep"):
    styles, h = style
    for c, st in enumerate(styles, start=1):
        x = ws.cell(r, c)
        x._style, x.value, x.hyperlink = copy(st), None, None
    for c, v in enumerate(values, start=1):
        if v is not None:
            ws.cell(r, c).value = v
    for c, url in (links or {}).items():
        ws.cell(r, c).hyperlink = url
        ws.cell(r, c)._style = copy(styles[c - 1])
    ws.row_dimensions[r].height = h if height == "keep" else height


def find_row(ws, text, col=1):
    for r in range(1, ws.max_row + 1):
        v = ws.cell(r, col).value
        if isinstance(v, str) and v.startswith(text):
            return r
    raise ValueError(text)


def main(week_no, monday, note=""):
    WEEK = f"WEEK OF {monday}"
    bk = os.path.join(tempfile.gettempdir(), f"Fitness_Tracker_backup_{datetime.datetime.now():%Y%m%d_%H%M%S}.xlsx")
    shutil.copy2(Q, bk)
    wb = openpyxl.load_workbook(Q)
    ex, dp = wb["Exercise Plan"], wb["Diet Plan"]
    if str(ex.cell(10, 1).value).startswith(WEEK) or str(dp.cell(4, 1).value).startswith(WEEK):
        print("SKIP: top block is already", WEEK); return
    # style rows come from the current top Exercise block (built 2026-10-22 layout)
    top = 10
    S_TITLE, S_SCHED_H, S_COLH, S_SCHED = grab(ex, top, 8), grab(ex, top + 1, 8), grab(ex, top + 2, 8), grab(ex, top + 3, 8)
    r_day = find_row(ex, "MONDAY - ")
    S_DAY, S_XHEAD, S_SEC, S_MOVE = grab(ex, r_day, 8), grab(ex, r_day + 1, 8), grab(ex, r_day + 2, 8), grab(ex, r_day + 3, 8)
    S_BLANK = grab(ex, r_day - 1, 8)
    S_NOTE = grab(ex, find_row(ex, "PROGRESSION:"), 8)

    cyc = (week_no - 1) % 4 + 1
    rows = []
    title = (f"TRAINER UPDATE - Week {week_no} (cycle week {cyc} of 4"
             + (", DELOAD: one set fewer, ~20% lighter" if cyc == 4 else ", anchors stay, every other move changes")
             + "). Times unchanged: gym 4:30-5:45 PM Mon-Fri, yoga 5:05 AM Tue/Thu/Sat/Sun, walk 6:45 PM. " + note)
    rows.append((S_TITLE, [WEEK, None, title], {}, 90, [(1, 2), (3, 8)]))
    rows.append((S_SCHED_H, ["Weekly Schedule"], {}, "keep", []))
    rows.append((S_COLH, ["Day", "Session", "Time", "Yoga / notes"], {}, "keep", []))
    for s in [("Sunday", "Rest + BP yoga", "5:05 - 5:35 AM", "Yoga for high BP at home. 8,000+ steps."),
              ("Monday", "UPPER A + abs (flexion) + wall squat", "4:30 - 5:45 PM", "No yoga."),
              ("Tuesday", "LOWER A + abs (anti-extension)", "4:30 - 5:45 PM", "Yoga 5:05 AM: hips + hamstrings."),
              ("Wednesday", "ATHLETIC: agility + circuit + abs + wall squat", "4:30 - 5:45 PM", "No yoga."),
              ("Thursday", "UPPER B + lower abs", "4:30 - 5:45 PM", "Yoga 5:05 AM: neck + shoulders + upper back."),
              ("Friday", "LOWER B + abs (rotation) + agility", "4:30 - 5:45 PM", "Weigh-in 5:10 AM. No yoga."),
              ("Saturday", "Active recovery", "8:00 - 9:00 AM", "Yoga 5:05 AM + 45-60 min walk + wall squat after the walk.")]:
        rows.append((S_SCHED, list(s), {}, "keep", []))
    rows.append((S_BLANK, [], {}, "keep", []))
    for d in ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday"):
        t, secs = day_plan(d, week_no)
        rows.append((S_DAY, [f"{d.upper()} - {t}  (4:30 - 5:45 PM)"], {}, "keep", []))
        rows.append((S_XHEAD, ["Exercise", "Sets x Reps", "Rest", "How to do it", "Demo video", "From", "Weight used (fill in)", "Reps hit (fill in)"], {}, "keep", []))
        for sec, moves in secs:
            rows.append((S_SEC, [sec], {}, "keep", []))
            for m in moves:
                rows.append((S_MOVE, [m["name"], m["sets"], m["rest"], m["cue"], "Watch demo", m["tag"]], {5: m["link"]}, "keep", []))
        rows.append((S_BLANK, [], {}, "keep", []))
    rows.append((S_DAY, ["SATURDAY + SUNDAY"], {}, "keep", []))
    rows.append((S_MOVE, ["Sat yoga 5:05 AM - " + YOGA["Saturday"][0], "30 min", "-", YOGA_RULES, "Watch video", "Fixed"], {5: YOGA["Saturday"][1]}, "keep", []))
    rows.append((S_MOVE, ["Sat easy walk", "45-60 min", "-", "8:00-9:00 AM, conversational pace.", "-", "Fixed"], {}, "keep", []))
    rows.append((S_MOVE, ["Sat " + WALL["name"], WALL["sets"], WALL["rest"], WALL["cue"], "Watch demo", "Fixed"], {5: WALL["link"]}, "keep", []))
    rows.append((S_MOVE, ["Sun yoga 5:05 AM - " + YOGA["Sunday"][0], "30 min", "-", YOGA_RULES, "Watch video", "Fixed"], {5: YOGA["Sunday"][1]}, "keep", []))
    rows.append((S_BLANK, [], {}, "keep", []))
    rows.append((S_NOTE, ["PROGRESSION + SAFETY: see the WEEK OF Oct 26, 2026 block (effort 7/10, beat anchors by 1 rep, breathe out on effort, "
                          "BP >= 160/100 -> walk + stretch only, >= 180/120 or chest pain -> stop and seek care)."], {}, 45, [(1, 8)]))
    rows.append((S_BLANK, [], {}, "keep", []))
    shift_down(ex, top, len(rows))
    for i, (st, vals, links, h, merges) in enumerate(rows):
        put(ex, top + i, st, vals, links, h)
        for a, b in merges:
            ex.merge_cells(start_row=top + i, start_column=a, end_row=top + i, end_column=b)

    # ---- Diet: same 7-day rotation, new title (swap dishes in plan_library.MEALS first if rotating) ----
    D_TITLE, D_HEAD, D_DAY, D_NOTE, D_LINK = grab(dp, 4, 18), grab(dp, 5, 18), grab(dp, 6, 18), grab(dp, 13, 18), grab(dp, 14, 18)
    head = [dp.cell(5, c).value for c in range(1, 19)]
    note_txt, links_row = dp.cell(13, 1).value, [(dp.cell(14, c).value, dp.cell(14, c).hyperlink.target if dp.cell(14, c).hyperlink else None) for c in range(1, 8)]
    shift_down(dp, 4, 11)
    lo = min(meal_totals(d)["cal"] for d in DAYS); hi = max(meal_totals(d)["cal"] for d in DAYS)
    put(dp, 4, D_TITLE, [WEEK, None, None, None, None, None,
        f"Week {week_no}: same day structure (snack ~3:30 PM, whey 5:45, HEAVY dinner 6:10, walk 6:45). Every day ~{lo:,.0f}-{hi:,.0f} cal, "
        f">=150 g protein. {note}"], height=45)
    dp.merge_cells("A4:F4"); dp.merge_cells("G4:R4")
    put(dp, 5, D_HEAD, head)
    for i, day in enumerate(DAYS):
        r = 6 + i
        m, t = MEALS[day], meal_totals(day)
        early = "Yoga 5:05 AM + saunf water" if day in YOGA else ("Weigh-in 5:10 AM + saunf water" if day == "Friday" else "Saunf water")
        put(dp, r, D_DAY, [day, m["type"], early, "Ragi Ganji (30 g ragi + buttermilk)", round(t["ganji"][0]), round(t["ganji"][1], 1),
                           m["snack"][0], round(t["snack"][0]), round(t["snack"][1], 1),
                           "Whey " + m["whey"], round(t["whey"][0]), round(t["whey"][1], 1),
                           f"{m['dish']}  |  Vamshi: {m['plate']}", round(t["dinner"][0]), round(t["dinner"][1], 1),
                           m["prep"], f"=E{r}+H{r}+K{r}+N{r}", f"=F{r}+I{r}+L{r}+O{r}"])
    put(dp, 13, D_NOTE, [note_txt], height=75); dp.merge_cells("A13:R13")
    put(dp, 14, D_LINK, [l[0] for l in links_row], {c: l[1] for c, l in enumerate(links_row, start=1) if l[1]})
    wb.save(Q)

    out = tempfile.mkdtemp()
    subprocess.run([SOFFICE, "--headless", "--calc", "--convert-to", "xlsx", "--outdir", out, Q], check=True, timeout=300)
    rec = os.path.join(out, os.path.basename(Q))
    v = openpyxl.load_workbook(rec, data_only=True)["Diet Plan"]
    bad = [(v.cell(r, 1).value, v.cell(r, 17).value, v.cell(r, 18).value) for r in range(6, 13)
           if not (v.cell(r, 17).value and v.cell(r, 17).value <= 2050 and v.cell(r, 18).value >= 150)]
    if bad:
        shutil.copy2(bk, Q)
        raise SystemExit(f"RESTORED backup - days out of limits: {bad}")
    shutil.copy2(rec, Q)
    print(f"OK: {WEEK} added (week {week_no}, cycle week {cyc}); backup {bk}")


if __name__ == "__main__":
    main(int(sys.argv[1]), sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "")
