# -*- coding: utf-8 -*-
"""Plain-text calendar descriptions (the iPhone calendar shows event notes as plain text, so tables live on the
VamFit Gym Card page; every event's first line is a one-tap link to that day's table view)."""
import sys, os, datetime as dt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from plan_library import MEALS, meal_totals, day_plan, YOGA
from start_weights import start_for

CARD = "https://vamfit-gym.netlify.app"   # his own Netlify site (2026-10-23: must not depend on a Claude membership)
_D = list(MEALS)
NEXT = {d: _D[(i + 1) % 7] for i, d in enumerate(_D)}


def link(d):
    return f"📱 GYM CARD (tap): {CARD}/#d{d:%Y%m%d}"


def dark(d):
    return d.month in (11, 12, 1, 2) or (d.month == 3 and d.day < 8)


def gym_text(d, wk, extra=None):
    day = d.strftime("%A")
    title, secs = day_plan(day, wk)
    cyc = (wk - 1) % 4 + 1
    L = [link(d), "", f"💪 {title}", f"Week {wk} · cycle {cyc}/4" + (" · DELOAD (1 set fewer, ~20% lighter)" if cyc == 4 else ""),
         "Leave 4:15 · gym 4:30-5:45 · whey 5:45 · dinner 6:10", "BP ≥160/100 → walk + stretch only · ≥180/120 → stop"]
    L += extra or []
    n = 0
    for sec, moves in secs:
        L += ["", sec.upper()]
        for m in moves:
            n += 1
            tag = " ⚓" if m["tag"] == "Anchor" else (" 🆕" if m["tag"] == "New" and cyc in (2, 3) else "")
            w = start_for(m["name"])
            if cyc == 4 and m["tag"] in ("Anchor", "New") and w[:1].isdigit():
                w += " (−20%)"
            rest = "" if m["rest"] in ("-", "") else f" · rest {m['rest']}"
            L.append(f"{n}. {m['name']}{tag} — {m['sets']} @ {w}{rest}")
    L += ["", "Rule: 2-3 reps left each set · breathe out on the push · top of range every set → +5 lb upper / +10 lb legs"]
    return "\n".join(L)


def meal_text(d, notes=None):
    day = d.strftime("%A")
    m, t = MEALS[day], meal_totals(day)
    weekend = day in ("Saturday", "Sunday")
    L = [link(d), "", f"🍽️ {m['type']} day · total ≈ {t['cal']:,.0f} kcal / {t['pro']:.0f} g protein"]
    if day == "Friday":
        L.append("5:10 AM — ⚖️ optional weigh-in")
    if day in YOGA:
        L.append(f"5:05 AM — 🧘 yoga: {YOGA[day][0]} {YOGA[day][1]}")
    L += [f"5:40 AM — ragi ganji + saunf water (140 kcal / 4 g)",
          f"3:30 PM — snack: {m['snack'][0]} ({t['snack'][0]:.0f} / {t['snack'][1]:.0f} g)",
          f"{'5:15' if weekend else '5:45'} PM — whey 1 scoop (120 / 24 g)",
          f"6:10 PM — dinner (family): {m['dish']} ({t['dinner'][0]:.0f} / {t['dinner'][1]:.0f} g)",
          f"         your plate: {m['plate']}",
          "6:45 PM — walk 20-25 min" + (" (dark: lit route + reflective vest/LED)" if dark(d) else ""),
          "9:30 PM — sleep",
          "", f"Prep tonight for {NEXT[day]}: {MEALS[NEXT[day]]['prep'].split(': ', 1)[-1]}"]
    L += notes or []
    return "\n".join(L)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    d = dt.date.fromisoformat(sys.argv[2])
    print(gym_text(d, int(sys.argv[3])) if sys.argv[1] == "gym" else meal_text(d))


# ---- SHORT versions (Vamshi 2026-10-22: long notes are "a mess" on the phone; the Gym Card holds the detail) ----
def gym_short(d, wk, extra=None):
    day = d.strftime("%A")
    title, secs = day_plan(day, wk)
    cyc = (wk - 1) % 4 + 1
    moves = [m for _, ms in secs for m in ms]
    anchors = " · ".join(f"{m['name']} {start_for(m['name'])}" for m in moves if m["tag"] == "Anchor")
    L = [link(d), f"💪 {title.split(' - ')[0].title()} · Week {wk} · {len(moves)} exercises" + (" · DELOAD" if cyc == 4 else ""),
         f"⚓ {anchors}" if anchors else "", "Leave 4:15 · gym 4:30-5:45 · whey 5:45"]
    L += extra or []
    return "\n".join(x for x in L if x)


def meal_short(d, notes=None):
    day = d.strftime("%A")
    m, t = MEALS[day], meal_totals(day)
    L = [link(d), f"🍽️ Snack 3:30: {m['snack'][0].split(':')[0]}", f"🍛 Dinner 6:10: {m['dish']}",
         f"≈ {t['cal']:,.0f} kcal · {t['pro']:.0f} g protein"]
    L += notes or []
    return "\n".join(L)
