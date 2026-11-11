# -*- coding: utf-8 -*-
"""Step 4 (2026-11-11): hour-by-hour guide for any date, with live weather (Open-Meteo, free, no key, city-level).
Fixed commitments first (office/home, school run, kid 2 school, gym), routines fill around them, rules on the right lines,
deadlines on their day. Weather is fetched in the browser at most once an hour; no Claude involved. Run once."""
import os
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gym_card_template.html")
s = open(P, encoding="utf-8").read()
assert 'id="guide"' not in s, "already patched"


def rep(old, new):
    global s
    assert s.count(old) == 1, ("anchor not unique or missing", old[:60])
    s = s.replace(old, new)


rep(".card ul.plain {", """#guide summary small { font-family: var(--mono); font-size: .75rem; font-weight: 500; color: var(--muted); text-transform: none }
.wx { font-family: var(--mono); font-size: .8rem; color: var(--muted); margin: 6px 0 0 }
ol.guide { list-style: none; margin: 8px 0 0; padding: 0; display: grid; gap: 4px }
ol.guide li { display: grid; grid-template-columns: 72px 1fr; gap: 8px; padding: 7px 8px; border-left: 4px solid var(--line); background: var(--soft); border-radius: 6px; font-size: .93rem; line-height: 1.25 }
ol.guide .gt { font-family: var(--mono); font-size: .8rem; color: var(--muted); padding-top: 1px }
ol.guide li.t-work { border-left-color: #4a7fd6 } ol.guide li.t-family { border-left-color: #b36ad1 }
ol.guide li.t-fit { border-left-color: var(--accent) } ol.guide li.t-food { border-left-color: #c9a227 }
ol.guide li.t-rest { border-left-color: var(--muted) } ol.guide li.t-dl { border-left-color: #e08a2e }
ol.guide li.now { outline: 2px solid var(--accent) }
ol.guide small { display: block; color: var(--muted); font-size: .82rem }
.card ul.plain {""")

# settings: leave-home time + weather location (city-level)
rep("""  routine: { wake: "05:00",""", """  location: { label: "Dallas area", lat: 32.78, lon: -96.8 },
  routine: { leaveHome: "06:30", wake: "05:00",""")
rep("""      <div class="grid2">${time("routine.wake", "Wake")}${time("routine.yoga", "Yoga")}</div>""",
    """      <div class="grid2">${time("routine.wake", "Wake")}${time("routine.yoga", "Yoga")}</div>
      ${time("routine.leaveHome", "Leave home for the office")}""")
rep("""    <details><summary>Deadlines</summary>""", """    <details><summary>Weather location</summary><div class="set">
      <p class="note">City-level only, used for sunrise, sunset, rain and temperature.</p>
      ${text("location.label", "Place name")}
      <div class="grid2"><label>Latitude<input type="number" step="any" data-kind="float" data-p="location.lat" value="${v("location.lat")}"></label><label>Longitude<input type="number" step="any" data-kind="float" data-p="location.lon" value="${v("location.lon")}"></label></div>
    </div></details>
    <details><summary>Deadlines</summary>""")
rep("""    else if (el.type === "number") val = Math.max(0, parseInt(val, 10) || 0);""",
    """    else if (el.dataset.kind === "float") val = parseFloat(val) || 0;
    else if (el.type === "number") val = Math.max(0, parseInt(val, 10) || 0);""")

# weather + guide
rep("""function gymToggleHtml(t) {""", r'''// ---------------- Weather (Open-Meteo, cached 1 hour in this browser)
let WX = null;
const wxKey = () => `${S.location.lat},${S.location.lon}`;
function loadWx() {
  try { const c = JSON.parse(localStorage.getItem("wxCache") || "null"); if (c && c.key === wxKey() && Date.now() - c.at < 3600e3) { WX = c.data; return; } } catch (e) {}
  const u = `https://api.open-meteo.com/v1/forecast?latitude=${S.location.lat}&longitude=${S.location.lon}&daily=sunrise,sunset,temperature_2m_max,temperature_2m_min,precipitation_probability_max&hourly=temperature_2m,precipitation_probability&temperature_unit=fahrenheit&timezone=America%2FChicago&forecast_days=16&past_days=1`;
  fetch(u).then(r => r.json()).then(d => {
    if (!d || !d.daily) return; WX = d;
    try { localStorage.setItem("wxCache", JSON.stringify({ key: wxKey(), at: Date.now(), data: d })); } catch (e) {}
    const g = document.getElementById("guide"); if (g && view === "day") g.outerHTML = guideHtml(cur);
  }).catch(() => {});
}
const hmOf = s => toMin(String(s).slice(11, 16));
function wxDay(t) {
  if (!WX) return null; const i = WX.daily.time.indexOf(iso(t)); if (i < 0) return null;
  return { rise: hmOf(WX.daily.sunrise[i]), set: hmOf(WX.daily.sunset[i]), hi: Math.round(WX.daily.temperature_2m_max[i]), lo: Math.round(WX.daily.temperature_2m_min[i]), rain: WX.daily.precipitation_probability_max[i] };
}
function wxAt(t, mins) {
  if (!WX) return null; const i = WX.hourly.time.indexOf(`${iso(t)}T${String(Math.floor(mins / 60)).padStart(2, "0")}:00`); if (i < 0) return null;
  return { temp: Math.round(WX.hourly.temperature_2m[i]), rain: WX.hourly.precipitation_probability[i] };
}
function walkAdvice(t, mins) {
  const d = wxDay(t), h = wxAt(t, mins), tips = [];
  if (d && mins > d.set + 15) tips.push(`dark after ${t12(d.set)}: lit route + LED clip, or indoors`);
  else if (!d && isDark(t)) tips.push("dark by then: lit route + LED clip, or indoors");
  if (h && h.rain >= 50) tips.push(`rain ${h.rain}%: walk indoors`);
  if (h && h.temp >= 95) tips.push(`${h.temp}°F: indoors or later`);
  else if (h && h.temp <= 35) tips.push(`${h.temp}°F: dress warm or walk indoors`);
  if (!tips.length && h) tips.push(`${h.temp}°F, good for outside`);
  return tips.join(" · ");
}
// ---------------- Hour-by-hour guide
function guideItems(t) {
  const R = S.routine, i = dow(t), d = DAYS[i], sd = schoolDay(t), k1 = S.kid1, k2 = S.kid2, items = [], m = DATA.meals[d];
  const w = dayData(t), title = w.title.split(" - ")[0];
  const add = (mins, label, type, note) => { if (mins != null && !isNaN(mins)) items.push({ m: mins, label, type, note }); };
  const at = hm => toMin(hm);
  add(at(R.wake), "Wake up · phone is across the room, stand up", "rest");
  if (i === 4) add(at(R.wake) + 10, "Optional weigh-in", "rest");
  if (DATA.yoga[d]) add(at(R.yoga), `Yoga: ${esc(DATA.yoga[d].name)}`, "fit", "End with 3 min slow breathing. Late start? Do it whenever you're up.");
  add(at(R.wake) + 40, "Ragi ganji + saunf water", "food");
  if (sd === "A") {
    add(at(R.leaveHome), "Leave for the office", "work");
    if (S.office.arrive) add(at(S.office.arrive), "At the office", "work");
    add(at(S.office.leave), "Leave the office", "work");
    add(at(k1.pickupTime), `Pick up ${esc(k1.name)}`, "family");
  } else if (sd === "B") {
    const dm = k1.dropTime ? at(k1.dropTime) : at("07:30");
    add(dm, `Drop ${esc(k1.name)} early`, "family", k1.dropTime ? "" : "Set the exact drop time in ⚙ Settings.");
    add(dm + 45, "Work from home", "work");
  } else if (i < 5 && isOfficeDay(t)) {
    add(at(R.leaveHome), "Leave for the office", "work"); add(at(S.office.leave), "Leave the office", "work");
  } else if (noSchoolWeekday(t)) add(at(R.leaveHome), "No school today: can be an office day", "work");
  if (i < 5 && k2.name !== DEFAULTS.kid2.name && (sd || !schoolRange())) {
    add(at(k2.schoolStart), `${esc(k2.name)}: school starts`, "family"); add(at(k2.schoolEnd), `${esc(k2.name)}: school ends`, "family");
  }
  for (const line of String(k2.activities || "").split("\n")) {
    if (!line.trim().toLowerCase().startsWith(SHORT3[i])) continue;
    const mm = /(\d{1,2})(?::(\d{2}))?\s*(am|pm)?/i.exec(line.slice(3));
    let mins = null; if (mm) { let h = +mm[1]; const ap = (mm[3] || "").toLowerCase(); if (ap === "pm" && h < 12) h += 12; if (!ap && h < 8) h += 12; mins = h * 60 + (+mm[2] || 0); }
    add(mins ?? at(k2.schoolEnd), `${esc(k2.name)}: ${esc(line.trim().slice(3).trim())}`, "family");
  }
  for (const x of deadlinesOn(t)) add(at(R.wake) + 1, `📌 Deadline: ${esc(x)}`, "dl");
  if (i < 5) {
    const gs = at(R.gymStart);
    add(at(R.snack), `Snack: ${esc(m.snack)}`, "food", "Eat it in the kitchen. TV stays off until the workout's done.");
    add(gs - 40, "Gym clothes on · don't sit down", "fit");
    add(gs - 15, "Keys in hand, leave for the gym", "fit");
    add(gs, `Gym: ${esc(title)} (${t12(gs)}–${T(R.gymEnd)})`, "fit", "Tired? Short version today: warm-up + the anchor moves counts.");
    add(at(R.gymEnd), "Whey, 1 scoop", "food");
  } else {
    if (i === 5) add(at("08:00"), "Easy walk 45–60 min, then the wall squat", "fit", "Missed a weekday workout? Do it now instead of the walk.");
    add(at(R.snack), `Snack: ${esc(m.snack)}`, "food");
    add(at("17:15"), "Whey, 1 scoop", "food");
  }
  add(at(R.dinner), `Dinner: ${esc(m.dish)}`, "food", `Today ≈ ${m.kcal.toLocaleString()} kcal / ${m.p} g protein · ${esc(m.type)} · low salt · kitchen closes after`);
  const wm = at(R.walk);
  add(wm, `Walk ${R.walkMin}+ min`, "fit", walkAdvice(t, wm));
  add(wm + (+R.walkMin || 10), i < 5 ? "Free time · TV is fine now if the workout's done" : "Free time with the family", "rest");
  add(at(R.screensOff), "Screens off · TV off", "rest");
  add(at(R.bed), "Bed", "rest");
  return items.sort((a, b) => a.m - b.m);
}
function guideHtml(t) {
  const items = guideItems(t), dw = wxDay(t);
  let open = true; try { open = localStorage.getItem("guideOpen") !== "0"; } catch (e) {}
  const nowM = t === TODAY ? (() => { const p = new Intl.DateTimeFormat("en-US", { timeZone: "America/Chicago", hour: "numeric", minute: "numeric", hourCycle: "h23" }).formatToParts(new Date()); return +p.find(x => x.type === "hour").value * 60 + +p.find(x => x.type === "minute").value; })() : -1;
  let nowIdx = -1; items.forEach((x, k) => { if (x.m <= nowM) nowIdx = k; });
  const wx = dw ? `☀ ${t12(dw.rise)} · 🌙 ${t12(dw.set)} · ${dw.hi}°/${dw.lo}°F · rain ${dw.rain}% · ${esc(S.location.label)}` : (WX ? "No forecast for this date (forecasts cover the next 16 days)." : "Weather loading…");
  return `<section class="card" id="guide"><details${open ? " open" : ""} id="guideD"><summary>Hour by hour <small>${fmt(t, { weekday: "short", month: "short", day: "numeric" })}</small></summary>
    <p class="wx">${wx}</p><ol class="guide">${items.map((x, k) => `<li class="t-${x.type}${k === nowIdx ? " now" : ""}"><span class="gt">${t12(x.m)}</span><span>${x.label}${x.note ? `<small>${x.note}</small>` : ""}</span></li>`).join("")}</ol></details></section>`;
}
function gymToggleHtml(t) {''')

rep("""  document.getElementById("main").innerHTML = gymToggleHtml(cur) + sparkHtml(cur)""",
    """  document.getElementById("main").innerHTML = gymToggleHtml(cur) + guideHtml(cur) + sparkHtml(cur)""")
rep("""window.addEventListener("hashchange",""", """document.getElementById("main").addEventListener("toggle", e => { if (e.target.id === "guideD") try { localStorage.setItem("guideOpen", e.target.open ? "1" : "0"); } catch (err) {} }, true);
loadWx();
window.addEventListener("hashchange",""")
open(P, "w", encoding="utf-8").write(s)
print("patched")
