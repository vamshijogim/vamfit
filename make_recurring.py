# -*- coding: utf-8 -*-
"""FIXED WEEK calendar text (Vamshi 2026-11-01: "regularly irregular"). Prints what each recurring gym series should say.
The series already exist (created 2026-10-23, each RRULE:FREQ=WEEKLY;INTERVAL=8, weeks 3-10, never ending) and are UPDATED
in place by event id, never recreated: Mon-Fri = the 5-day split, 4:30-5:45 PM.
Re-run after a plan_library.py change, then update_event each id with notificationLevel NONE."""
import sys, os, datetime as dt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from plan_library import day_plan, WALK
from start_weights import start_for
from cal_text import CARD

LINK = f"📱 GYM CARD (tap): {CARD}"
W1 = dt.date(2026, 10, 26)
IDS = {  # week -> Mon, Tue, Wed, Thu, Fri series id
    3: "ulagrt8678l3a02ar6nmicmkuk bm6h43jf0mgn458r3b960u2lg0 nc942f6lkdvq7ohdo4lq7cnfmg uc4un494br32r3jmsmsk5sev5k 5f11nc1tqn2dpva6g4g943gmtc",
    4: "7ssaqnkceha2s6l9bar2adbt2k sm9ndr7b00477e6hb4orro67ps c75abbcdtdj2lt8vvilmenuusg r5f7t7lvefho0dufri8bm8dl7s et9fusfsc0tbbgkpt1o9a6eqn8",
    5: "hv5tt9iilk9p0gk6nqsr5da45s 2i8bbsojumk39pjbckev6434k4 roqj3rtjgetknia6a19ijajed4 6k0qld7o1mp3jmcbv5q246kh0s g4pkeiv00ibj9kujlr2s7vn8q0",
    6: "jmlig63i8d4fu5li0sufasemq0 ipblmhitbk2e5s7oed84nipv2s pu3lljfbf3tpot4oh218f5u3o0 djvv76q8ir1ag4rcdi28mrflfc tpktqu676v6hgkt6vkbiiita3o",
    7: "e9tmghtqhj2esc64seop47mpqs rufvt8d86qjdhbdt34mobkn95k giltvf1t5fa1pfcq16brjaa2cc 246bdpcni0l6tbgv6196fs6e24 obsslibsbbbhs4vr1mdlrddj5o",
    8: "rhv1gjemneb2s4bflp4oft47hs mciega4n2nmi6oku85mfpd0dug sjb4vokbpcus5tnjtknnbvlep4 k2erdnu40p7riv9ng89j85oodo 5o658aun07u0932htauulbi78g",
    9: "itbetreesfe11r99rqvaq3f1hg e9jv3ru4ce68b8ntcsek599gb0 jlqecotfse0vsgdv51ms16cddk rcjr9hbfqjiq1ekcguufic6or0 5iscphu4bo4gucj2q88je8pfb0",
    10: "aon2l3rrf6e6u7m6hamv1aaips ooi0mmc7kped8liu77hkqss2mk 759o76fn6omtvothqpji888ovo o7dgnjisje745cj8hf7odb2mfk gdgh7k52ja0978fdjhfu5k985s",
}
LEAVE = "Leave 4:15 · gym 4:30-5:45 · whey 5:45"
SHORT = {"Monday": "Upper A + abs + wall squat", "Tuesday": "Lower A + abs", "Wednesday": "Athletic day: agility + circuit + abs + wall squat",
         "Thursday": "Upper B + lower abs", "Friday": "Lower B + abs + agility"}


def gym(day, wk):
    """(title, description) for a gym day of week wk."""
    cyc, cycle_no = (wk - 1) % 4 + 1, (wk - 1) // 4 % 2 + 1
    title, secs = day_plan(day, wk)
    label = title.split(" - ")[0].title()
    moves = [m for sec, ms in secs for m in ms if m["name"] != WALK["name"] and not sec.startswith("5:05")]
    anchors = " · ".join(f"{m['name']} {start_for(m['name'])}" for m in moves if m["tag"] == "Anchor")
    tail = "DELOAD week" if cyc == 4 else ("🆕 new moves this week" if cyc in (2, 3) else "beat last time by 1 rep")
    desc = [LINK, f"💪 {label} · cycle {cycle_no} · week {cyc}/4 · {len(moves)} exercises" + (" · DELOAD: 1 set fewer, ~20% lighter" if cyc == 4 else ""),
            f"⚓ {anchors}" if anchors else "", LEAVE]
    return f"💪 {SHORT[day]} · 4:30 PM · {tail}", "\n".join(x for x in desc if x)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    for wk in sorted(IDS):
        for i, day in enumerate(SHORT):
            d = W1 + dt.timedelta(days=7 * (wk - 1) + i)
            t, desc = gym(day, wk)
            print("####", IDS[wk].split()[i], d, t)
            print(desc)
