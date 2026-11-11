# -*- coding: utf-8 -*-
"""Builds gym_card.html: the phone page with TABLES for every day (workout + meals), linked from each calendar event.
Re-run + republish (Artifact, same file path) whenever plan_library.py / start_weights.py / meals.py change."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from plan_library import MEALS, meal_totals, day_plan, YOGA, YT
from start_weights import start_for

DAYS7 = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
GYM_DAY = dict(when="4:30–5:45 PM", job="TV off. No couch. Eat in the kitchen, gym clothes on, keys in hand at 4:15. TV is your reward after.")
SAT = dict(when="Yoga 5:05 AM · walk 8:00 AM", job="Late Friday? Do yoga whenever you get up. Missed a weekday workout? Do it today instead of the easy walk (tap that day above).")
SUN = dict(when="Yoga 5:05 AM", job="Slept through the alarm? Do the yoga whenever you get up. It still counts.")
META = dict(Monday=GYM_DAY, Tuesday=GYM_DAY, Wednesday=GYM_DAY, Thursday=GYM_DAY, Friday=GYM_DAY, Saturday=SAT, Sunday=SUN)
weeks = {}
for wk in range(1, 9):                      # two full 4-week cycles (cycle 2 = new anchors); later weeks repeat this pattern
    wd = {}
    for d in DAYS7:
        title, secs = day_plan(d, wk)
        wd[d] = {"title": title, **META[d], "sections": [
            {"name": sec, "moves": [{"n": m["name"], "s": m["sets"], "r": m["rest"], "w": ("-" if m["tag"] == "Home" else start_for(m["name"])) +
                                     (" (deload: ~20% less)" if (wk - 1) % 4 == 3 and m["tag"] in ("Anchor", "New") and start_for(m["name"])[:1].isdigit() else ""),
                                     "t": m["tag"], "l": m["link"]} for m in moves]} for sec, moves in secs]}
    weeks[wk] = wd
meals = {}
for d, m in MEALS.items():
    t = meal_totals(d)
    meals[d] = {"type": m["type"], "snack": m["snack"][0], "snackKcal": round(t["snack"][0]), "snackP": round(t["snack"][1]),
                "whey": m["whey"], "dish": m["dish"], "plate": m["plate"], "recipe": YT(m["recipe"]),
                "dinKcal": round(t["dinner"][0]), "dinP": round(t["dinner"][1]), "kcal": round(t["cal"]), "p": round(t["pro"]),
                "prep": m["prep"].split(": ", 1)[-1]}
yoga = {d: {"name": v[0], "url": v[1]} for d, v in YOGA.items()}
data = json.dumps({"weeks": weeks, "meals": meals, "yoga": yoga}, ensure_ascii=False, separators=(",", ":"))
tpl = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "gym_card_template.html"), encoding="utf-8").read()
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "gym_card.html")
open(out, "w", encoding="utf-8").write(tpl.replace("/*__DATA__*/null", data))
print("wrote", out, len(data), "bytes of data")
