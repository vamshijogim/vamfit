# -*- coding: utf-8 -*-
"""Step 2 (2026-11-11): Settings panel. Adds a gear button, a Settings view saved in the browser
(localStorage "vamfitSettings") with Export/Import as a file, and makes the day view read its times,
the school run and the monthly office count from those settings. Run once; it refuses to run twice."""
import os
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gym_card_template.html")
s = open(P, encoding="utf-8").read()
assert "vamfitSettings" not in s, "already patched"


def rep(old, new):
    global s
    assert s.count(old) == 1, ("anchor not unique or missing", old[:60])
    s = s.replace(old, new)


# ---- CSS
rep(".card ul.plain {", """.run { display: grid; gap: 4px; background: var(--soft); border: 1px solid var(--line); border-radius: 10px; padding: 10px 12px; font-weight: 600 }
.run span { display: block }
.officeline { font-family: var(--mono); font-size: .8rem; color: var(--muted) }
.officeline b { color: var(--anchor) }
.set { display: grid; gap: 12px }
.set label { display: grid; gap: 4px; font-size: .9rem; color: var(--muted) }
.set input, .set select, .set textarea { font: inherit; color: var(--ink); background: var(--soft); border: 1px solid var(--line); border-radius: 8px; padding: 10px; width: 100%; min-height: 44px }
.set textarea { min-height: 88px; font-family: var(--mono); font-size: .8rem }
.set .grid2 { display: grid; grid-template-columns: 1fr 1fr; gap: 10px }
.set .wk { display: flex; flex-wrap: wrap; gap: 6px }
.set .wk label { display: flex; align-items: center; gap: 4px; color: var(--ink); min-height: 44px; padding: 0 8px; border: 1px solid var(--line); border-radius: 8px }
.set .wk input { width: auto; min-height: 0 }
.btnrow { display: flex; flex-wrap: wrap; gap: 8px }
.btnrow button, .btnrow label.btn { min-height: 44px; padding: 0 14px; display: inline-flex; align-items: center; border: 1px solid var(--line); border-radius: 10px; background: var(--panel); color: var(--ink); font-weight: 600; cursor: pointer }
.btnrow .primary { background: var(--accent); color: var(--accent-ink); border-color: var(--accent) }
.saved { color: var(--accent); font-weight: 700; min-height: 1.2em }
.card ul.plain {""")

# ---- gear button in the header
rep("""      <button class="nav" id="next" aria-label="Next day">›</button>""",
    """      <button class="nav" id="next" aria-label="Next day">›</button>
      <button class="nav" id="gear" aria-label="Settings">⚙</button>""")

# ---- settings model + helpers (before scoreHtml)
rep("function scoreHtml(monday) {", r'''// ---------------- Settings (saved in this browser; Export/Import as a file). The public page ships generic defaults only.
const SETTINGS_KEY = "vamfitSettings";
const DEFAULTS = {
  v: 1,
  kid1: { name: "Kid 1", dropTime: "", pickupTime: "15:00", aDays: [], bDays: [], collegeStart: "" },
  kid2: { name: "Kid 2", schoolStart: "09:00", schoolEnd: "16:30", activities: "" },
  office: { minDays: 12, rule: "pickup", weekdays: [], arrive: "", leave: "14:30" },
  routine: { wake: "05:00", yoga: "05:05", gymStart: "16:30", gymEnd: "17:45", snack: "15:30", dinner: "18:10",
             walk: "18:45", walkMin: 10, screensOff: "21:00", bed: "21:30" }
};
const merge = (d, s) => { const o = {}; for (const k in d) o[k] = (d[k] && typeof d[k] === "object" && !Array.isArray(d[k])) ? merge(d[k], (s || {})[k]) : ((s || {})[k] ?? d[k]); return o; };
function loadSettings() { try { return merge(DEFAULTS, JSON.parse(localStorage.getItem(SETTINGS_KEY) || "{}")); } catch (e) { return merge(DEFAULTS, {}); } }
function saveSettings() { try { localStorage.setItem(SETTINGS_KEY, JSON.stringify(S)); } catch (e) {} }
let S = loadSettings(), view = "day";
const toMin = hm => { const m = /^(\d{1,2}):(\d{2})$/.exec(hm || ""); return m ? +m[1] * 60 + +m[2] : null; };
const t12 = mins => { if (mins == null) return ""; const h = Math.floor(mins / 60) % 24, m = mins % 60; return `${(h + 11) % 12 + 1}:${String(m).padStart(2, "0")} ${h < 12 ? "AM" : "PM"}`; };
const T = hm => t12(toMin(hm));
const iso = t => { const d = new Date(t); return `${d.getUTCFullYear()}-${String(d.getUTCMonth() + 1).padStart(2, "0")}-${String(d.getUTCDate()).padStart(2, "0")}`; };
function schoolDay(t) {
  const k = S.kid1, d = iso(t);
  if (k.collegeStart && d >= k.collegeStart) return null;
  return k.aDays.includes(d) ? "A" : (k.bDays.includes(d) ? "B" : null);
}
function schoolRange() { const all = [...S.kid1.aDays, ...S.kid1.bDays].sort(); return all.length ? [all[0], all[all.length - 1]] : null; }
function isOfficeDay(t) {
  if (dow(t) > 4) return false;
  if (S.office.rule === "weekdays") return S.office.weekdays.includes(dow(t));
  return schoolDay(t) === "A";
}
function noSchoolWeekday(t) { const r = schoolRange(), d = iso(t); return !!r && dow(t) < 5 && d >= r[0] && d <= r[1] && !schoolDay(t) && !(S.kid1.collegeStart && d >= S.kid1.collegeStart); }
function officeMonthHtml(t) {
  if (S.office.rule === "pickup" && !schoolRange()) return "";
  const d0 = new Date(t), y = d0.getUTCFullYear(), m = d0.getUTCMonth();
  let planned = 0; const topups = [];
  for (let day = 1; day <= 31; day++) {
    const x = Date.UTC(y, m, day); if (new Date(x).getUTCMonth() !== m) break;
    if (isOfficeDay(x)) planned++; else if (noSchoolWeekday(x)) topups.push(fmt(x, { month: "short", day: "numeric" }));
  }
  const need = Math.max(0, S.office.minDays - planned);
  return `<p class="officeline">Office this month: ${planned} planned, need ${S.office.minDays}${need ? ` · <b>short ${need}</b>${topups.length ? ` · no-school weekdays to add: ${topups.join(", ")} (skip company holidays)` : " · use drop days, going in late"}` : " ✓"}</p>`;
}
function runHtml(t) {
  const k1 = S.kid1, k2 = S.kid2, sd = schoolDay(t), lines = [];
  if (sd === "A") lines.push(`🏢 Office${S.office.arrive ? ` from ${T(S.office.arrive)}` : ""} · leave ${T(S.office.leave)} · 🚗 pick up ${esc(k1.name)} by ${T(k1.pickupTime)}`);
  else if (sd === "B") lines.push(`🚗 Drop ${esc(k1.name)} ${k1.dropTime ? `at ${T(k1.dropTime)}` : "early"} · 🏠 work from home`);
  else if (noSchoolWeekday(t)) lines.push(`🏫 No school for ${esc(k1.name)} · can be an office day`);
  if (dow(t) < 5 && k2.name !== DEFAULTS.kid2.name && (sd || !schoolRange())) lines.push(`🎒 ${esc(k2.name)}: school ${T(k2.schoolStart)}–${T(k2.schoolEnd)}`);
  const ab = SHORT3[dow(t)];
  for (const line of String(k2.activities || "").split("\n")) if (line.trim().toLowerCase().startsWith(ab)) lines.push(`🎵 ${esc(k2.name)}: ${esc(line.trim().slice(3).trim())}`);
  return lines.length ? `<div class="run">${lines.map(l => `<span>${l}</span>`).join("")}</div>` : "";
}
const SHORT3 = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"];

function settingsHtml() {
  const v = p => esc(p.split(".").reduce((o, k) => o[k], S));
  const time = (p, label) => `<label>${label}<input type="time" data-p="${p}" value="${v(p)}"></label>`;
  const text = (p, label, ph = "") => `<label>${label}<input type="text" data-p="${p}" value="${v(p)}" placeholder="${ph}"></label>`;
  const dates = (p, label) => `<label>${label}<textarea data-p="${p}" data-kind="dates" placeholder="2026-11-10, 2026-11-12, …">${esc(p.split(".").reduce((o, k) => o[k], S).join(", "))}</textarea></label>`;
  const wd = S.office.weekdays;
  return `<section class="card set"><h2>Settings</h2>
    <p class="note">Saved on this device only. Use Export to back up, and Import on your other device. Changing settings updates this app. To update the Google Calendar reminders, ask Claude.</p>
    <p class="saved" id="saved"></p>
    <details open><summary>${esc(S.kid1.name)}: school run</summary><div class="set">
      ${text("kid1.name", "Name")}
      <div class="grid2">${time("kid1.dropTime", "Drop time (B days, blank = early)")}${time("kid1.pickupTime", "Pickup by (A days)")}</div>
      ${dates("kid1.aDays", "A days (office + pickup)")}
      ${dates("kid1.bDays", "B days (drop + work from home)")}
      <label>College starts (school-run rules switch off from this date)<input type="date" data-p="kid1.collegeStart" value="${v("kid1.collegeStart")}"></label>
    </div></details>
    <details><summary>${esc(S.kid2.name)}</summary><div class="set">
      ${text("kid2.name", "Name")}
      <div class="grid2">${time("kid2.schoolStart", "School starts")}${time("kid2.schoolEnd", "School ends")}</div>
      <label>Activities, one per line, starting with the day<textarea data-p="kid2.activities" placeholder="Tue 4:30–6:00 PM dance">${v("kid2.activities")}</textarea></label>
    </div></details>
    <details><summary>Office</summary><div class="set">
      <label>Minimum office days a month<input type="number" min="0" max="23" data-p="office.minDays" value="${v("office.minDays")}"></label>
      <label>Office days are<select data-p="office.rule"><option value="pickup"${S.office.rule === "pickup" ? " selected" : ""}>Pickup (A) days</option><option value="weekdays"${S.office.rule === "weekdays" ? " selected" : ""}>Fixed weekdays</option></select></label>
      <div class="wk">${["Mon", "Tue", "Wed", "Thu", "Fri"].map((d, i) => `<label><input type="checkbox" data-wd="${i}"${wd.includes(i) ? " checked" : ""}>${d}</label>`).join("")}</div>
      <div class="grid2">${time("office.arrive", "Arrive")}${time("office.leave", "Leave")}</div>
    </div></details>
    <details><summary>Routines</summary><div class="set">
      <p class="note">The workouts themselves stay Mon–Fri and yoga stays Tue/Thu/Sat/Sun. Change their times here.</p>
      <div class="grid2">${time("routine.wake", "Wake")}${time("routine.yoga", "Yoga")}</div>
      <div class="grid2">${time("routine.gymStart", "Gym starts")}${time("routine.gymEnd", "Gym ends")}</div>
      <div class="grid2">${time("routine.snack", "Snack")}${time("routine.dinner", "Dinner")}</div>
      <div class="grid2">${time("routine.walk", "Walk")}<label>Walk minutes<input type="number" min="5" max="90" data-p="routine.walkMin" value="${v("routine.walkMin")}"></label></div>
      <div class="grid2">${time("routine.screensOff", "TV and screens off")}${time("routine.bed", "Bed")}</div>
    </div></details>
    <details><summary>Backup</summary><div class="set">
      <div class="btnrow"><button type="button" id="exportS">Export file</button>
        <label class="btn" for="importS">Import file</label><input type="file" id="importS" accept=".json,application/json" hidden>
        <button type="button" id="resetS">Reset to defaults</button></div>
    </div></details>
    <div class="btnrow"><button type="button" class="primary" id="doneS">Done</button></div></section>`;
}
function setPath(p, val) { const ks = p.split("."), last = ks.pop(); ks.reduce((o, k) => o[k], S)[last] = val; }
function flashSaved(msg) { const el = document.getElementById("saved"); if (el) { el.textContent = msg; setTimeout(() => { if (el.textContent === msg) el.textContent = ""; }, 2500); } }

function scoreHtml(monday) {''')

# ---- day view reads settings
rep("""  const parts = w.title.split(" - "), head = parts[0], focus = parts.slice(1).join(" - ");""",
    """  const parts = w.title.split(" - "), head = parts[0], focus = parts.slice(1).join(" - ");
  const R = S.routine, gs = toMin(R.gymStart);
  const job = isGym ? `TV off. No couch. Eat in the kitchen, gym clothes on, keys in hand at ${t12(gs - 15)}. TV is your reward after.` : w.job;
  const when = isGym ? `${T(R.gymStart)}–${T(R.gymEnd)}` : w.when.replace("5:05 AM", T(R.yoga));""")
rep("""${alarmHtml(t)}<div class="job">${esc(w.job)}</div>""", """${alarmHtml(t)}${runHtml(t)}<div class="job">${esc(job)}</div>""")
rep("""<span class="chip">${esc(w.when)}</span>""", """<span class="chip">${esc(when)}</span>""")
rep("""    <tr><td>3:30 PM</td><td><b>Snack:</b> ${esc(m.snack)}</td></tr>
    <tr><td>${isGym ? "5:45" : "5:15"} PM</td><td>Whey, 1 scoop</td></tr>
    <tr><td>6:10 PM</td><td>""", """    <tr><td>${T(S.routine.snack)}</td><td><b>Snack:</b> ${esc(m.snack)}</td></tr>
    <tr><td>${isGym ? T(S.routine.gymEnd) : "5:15 PM"}</td><td>Whey, 1 scoop</td></tr>
    <tr><td>${T(S.routine.dinner)}</td><td>""")
rep("""<li><b>Mon–Fri: TV only between my workout and 9:00 PM.</b>""", """<li><b>Mon–Fri: TV only between my workout and ${T(S.routine.screensOff)}.</b>""")

# ---- render: settings view + office line
rep("""  document.getElementById("score").innerHTML = scoreHtml(monday);
  document.getElementById("main").innerHTML = sparkHtml(cur)""", """  document.getElementById("score").innerHTML = scoreHtml(monday) + officeMonthHtml(cur);
  if (view === "settings") { document.getElementById("main").innerHTML = settingsHtml(); return; }
  document.getElementById("main").innerHTML = sparkHtml(cur)""")
rep("""  document.getElementById("score").innerHTML = scoreHtml(cur - dow(cur) * DAY);
  const al""", """  document.getElementById("score").innerHTML = scoreHtml(cur - dow(cur) * DAY) + officeMonthHtml(cur);
  const al""")

# ---- events
rep("""document.getElementById("main").addEventListener("change", e => {
  if (e.target.id !== "why") return;""", """document.getElementById("gear").addEventListener("click", () => { view = view === "settings" ? "day" : "settings"; render(); window.scrollTo(0, 0); });
document.getElementById("main").addEventListener("click", e => {
  const id = e.target.id;
  if (id === "doneS") { view = "day"; render(); window.scrollTo(0, 0); }
  else if (id === "exportS") {
    const a = document.createElement("a");
    a.href = URL.createObjectURL(new Blob([JSON.stringify(S, null, 2)], { type: "application/json" }));
    a.download = "vamfit-settings.json"; document.body.appendChild(a); a.click(); a.remove();
  } else if (id === "resetS" && confirm("Reset all settings to the defaults on this device?")) { S = merge(DEFAULTS, {}); saveSettings(); render(); flashSaved("Reset ✓"); }
});
document.getElementById("main").addEventListener("change", e => {
  const el = e.target;
  if (el.id === "importS" && el.files && el.files[0]) {
    el.files[0].text().then(txt => { const o = JSON.parse(txt); if (!o || typeof o !== "object" || !o.kid1) throw new Error("bad file"); S = merge(DEFAULTS, o); saveSettings(); render(); flashSaved("Imported ✓"); })
      .catch(() => flashSaved("That file isn't a VamFit settings file."));
    return;
  }
  if (el.dataset.wd !== undefined) {
    const i = +el.dataset.wd, set = new Set(S.office.weekdays); if (el.checked) set.add(i); else set.delete(i);
    S.office.weekdays = [...set].sort(); saveSettings(); flashSaved("Saved ✓"); document.getElementById("score").innerHTML = scoreHtml(cur - dow(cur) * DAY) + officeMonthHtml(cur); return;
  }
  if (el.dataset.p) {
    let val = el.value;
    if (el.dataset.kind === "dates") val = [...new Set((val.match(/\\d{4}-\\d{2}-\\d{2}/g) || []))].sort();
    else if (el.type === "number") val = Math.max(0, parseInt(val, 10) || 0);
    else if (el.type === "text") val = val.trim();
    setPath(el.dataset.p, val); saveSettings(); flashSaved("Saved ✓");
    document.getElementById("score").innerHTML = scoreHtml(cur - dow(cur) * DAY) + officeMonthHtml(cur);
    if (el.dataset.kind === "dates") el.value = val.join(", ");
    return;
  }
  if (el.id !== "why") return;""")
open(P, "w", encoding="utf-8").write(s)
print("patched")
