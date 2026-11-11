# -*- coding: utf-8 -*-
"""Step 3 (2026-11-11): month calendar view + "Did I go to the gym?" toggle + private deadlines list.
- 📅 button in the date bar switches between the day view and a month grid (colored dots per type, ✓ = went to gym).
- One big toggle at the top of every day: tap = "I went to the gym" (localStorage "gymYYYYMMDD"); it counts in the score.
- Settings gets a Deadlines box ("YYYY-MM-DD text" per line), shown on the day and in the month view.
Run once; it refuses to run twice."""
import os
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gym_card_template.html")
s = open(P, encoding="utf-8").read()
assert "gymTog" not in s, "already patched"


def rep(old, new):
    global s
    assert s.count(old) == 1, ("anchor not unique or missing", old[:60])
    s = s.replace(old, new)


rep(".card ul.plain {", """.gymtog { width: 100%; min-height: 58px; font-size: 1.08rem; font-weight: 700; border-radius: 14px; border: 2px dashed var(--line); background: var(--panel) }
.gymtog.on { border: 2px solid var(--accent); background: var(--accent-soft); color: var(--ink) }
.mhead { display: flex; align-items: center; gap: 8px }
.mhead h2 { flex: 1; text-align: center }
.mgrid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 4px }
.mgrid .wd { font-family: var(--mono); font-size: .7rem; color: var(--muted); text-align: center }
.mc { position: relative; min-height: 56px; padding: 5px 2px; display: grid; align-content: start; justify-items: center; gap: 4px; border-radius: 8px }
.mc.out { opacity: .35 }
.mc.today { border: 2px solid var(--accent) }
.mc b { font-family: var(--display); font-size: 1.05rem }
.dots { display: flex; gap: 3px; flex-wrap: wrap; justify-content: center }
.d { width: 8px; height: 8px; border-radius: 50%; display: inline-block }
.d.work { background: #4a7fd6 } .d.family { background: #b36ad1 } .d.fit { background: var(--accent) } .d.dl { background: #e08a2e }
.went { position: absolute; top: 2px; right: 4px; font-style: normal; color: var(--accent); font-size: .8rem; font-weight: 800 }
.legend { display: flex; flex-wrap: wrap; gap: 6px 12px; font-size: .82rem; color: var(--muted) }
.legend span { display: inline-flex; align-items: center; gap: 5px }
.mlist { margin: 0; padding-left: 18px; display: grid; gap: 4px; font-size: .92rem }
.card ul.plain {""")

rep("""    <button class="nav" id="gear" aria-label="Settings">⚙</button>""",
    """    <button class="nav" id="cal" aria-label="Month calendar">📅</button>
    <button class="nav" id="gear" aria-label="Settings">⚙</button>""")

# gym toggle storage; it counts as moving and as a workout day
rep("const moved = t => loadDone(t).length > 0;",
    """const loadGym = t => { try { return localStorage.getItem("gym" + key(t)) === "1"; } catch (e) { return false; } };
const saveGym = (t, on) => { try { if (on) localStorage.setItem("gym" + key(t), "1"); else localStorage.removeItem("gym" + key(t)); } catch (e) {} };
const moved = t => loadDone(t).length > 0 || loadGym(t);""")
rep("const workoutDone = t => { const walk",
    "const workoutDone = t => { if (loadGym(t)) return true; const walk")

# deadlines in settings
rep("""  routine: { wake: "05:00",""", """  deadlines: "",
  routine: { wake: "05:00",""")
rep("""const SHORT3 = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"];""",
    """const SHORT3 = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"];
function deadlinesOn(t) {
  const d = iso(t), out = [];
  for (const line of String(S.deadlines || "").split("\\n")) { const m = /^\\s*(\\d{4}-\\d{2}-\\d{2})\\s+(.+)$/.exec(line); if (m && m[1] === d) out.push(m[2].trim()); }
  return out;
}
function gymToggleHtml(t) {
  const on = loadGym(t);
  return `<button type="button" class="gymtog${on ? " on" : ""}" id="gymTog" aria-pressed="${on}">${on ? "✅ I went to the gym" : "💪 Did I go to the gym? Tap if yes"}</button>`;
}
function monthHtml() {
  const c = new Date(cur), y = c.getUTCFullYear(), m = c.getUTCMonth(), first = Date.UTC(y, m, 1);
  let t = first - dow(first) * DAY, cells = "", went = 0;
  const dl = [];
  do {
    for (let i = 0; i < 7; i++, t += DAY) {
      const inM = new Date(t).getUTCMonth() === m, sd = schoolDay(t), g = loadGym(t) || workoutDone(t), dls = deadlinesOn(t);
      if (inM && g) went++;
      if (inM) for (const x of dls) dl.push(`<li><b>${fmt(t, { month: "short", day: "numeric" })}</b> ${esc(x)}</li>`);
      const dots = (isOfficeDay(t) ? '<i class="d work"></i>' : "") + (sd ? '<i class="d family"></i>' : "")
        + (dow(t) < 5 ? '<i class="d fit"></i>' : "") + (dls.length ? '<i class="d dl"></i>' : "");
      cells += `<button class="mc${inM ? "" : " out"}${t === TODAY ? " today" : ""}" data-t="${t}" aria-label="${fmt(t, { weekday: "long", month: "long", day: "numeric" })}"><b>${new Date(t).getUTCDate()}</b><span class="dots">${dots}</span>${g ? '<i class="went">✓</i>' : ""}</button>`;
    }
  } while (new Date(t).getUTCMonth() === m);
  return `<section class="card"><div class="mhead"><button class="nav" id="mPrev" aria-label="Previous month">‹</button><h2>${fmt(first, { month: "long", year: "numeric" })}</h2><button class="nav" id="mNext" aria-label="Next month">›</button></div>
    <div class="mgrid">${["M", "T", "W", "T", "F", "S", "S"].map(x => `<span class="wd">${x}</span>`).join("")}${cells}</div>
    <div class="legend"><span><i class="d work"></i>Office</span><span><i class="d family"></i>School run</span><span><i class="d fit"></i>Gym day</span><span><i class="d dl"></i>Deadline</span><span>✓ Went to gym</span></div>
    <p class="note">Went to the gym ${went} day${went === 1 ? "" : "s"} this month. Tap a day to open it.</p>
    ${officeMonthHtml(first)}${dl.length ? `<p class="sec">Deadlines this month</p><ul class="mlist">${dl.join("")}</ul>` : ""}</section>`;
}""")
rep("""  return lines.length ? `<div class="run">""", """  for (const x of deadlinesOn(t)) lines.push(`📌 ${esc(x)}`);
  return lines.length ? `<div class="run">""")
rep("""    <details><summary>Backup</summary>""", """    <details><summary>Deadlines</summary><div class="set">
      <label>One per line: date, space, what's due. Shown on that day and in the month view.<textarea data-p="deadlines" placeholder="2026-12-01 Scholarship application due">${v("deadlines")}</textarea></label>
    </div></details>
    <details><summary>Backup</summary>""")

# render: month view + gym toggle on top of the day
rep("""  if (view === "settings") { document.getElementById("main").innerHTML = settingsHtml(); return; }
  document.getElementById("main").innerHTML = sparkHtml(cur)""",
    """  if (view === "settings") { document.getElementById("main").innerHTML = settingsHtml(); return; }
  if (view === "month") { document.getElementById("main").innerHTML = monthHtml(); return; }
  document.getElementById("main").innerHTML = gymToggleHtml(cur) + sparkHtml(cur)""")

# events
rep("""document.getElementById("gear").addEventListener("click", """,
    """document.getElementById("cal").addEventListener("click", () => { view = view === "month" ? "day" : "month"; render(); window.scrollTo(0, 0); });
document.getElementById("main").addEventListener("click", e => {
  const tog = e.target.closest("#gymTog");
  if (tog) {
    const on = !loadGym(cur); saveGym(cur, on);
    tog.classList.toggle("on", on); tog.setAttribute("aria-pressed", on); tog.textContent = on ? "✅ I went to the gym" : "💪 Did I go to the gym? Tap if yes";
    const btn = document.querySelector(`#days button[data-t="${cur}"]`); if (btn) btn.classList.toggle("moved", moved(cur));
    document.getElementById("score").innerHTML = scoreHtml(cur - dow(cur) * DAY) + officeMonthHtml(cur);
    const al = document.querySelector(".alarm"); if (al && moved(cur)) al.remove();
    return;
  }
  if (e.target.closest("#mPrev, #mNext")) { const c = new Date(cur); cur = Date.UTC(c.getUTCFullYear(), c.getUTCMonth() + (e.target.closest("#mNext") ? 1 : -1), 1); render(); return; }
  const cell = e.target.closest(".mc[data-t]");
  if (cell) { cur = +cell.dataset.t; view = "day"; render(); window.scrollTo(0, 0); }
});
document.getElementById("gear").addEventListener("click", """)
open(P, "w", encoding="utf-8").write(s)
print("patched")
