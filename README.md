# VamFit app: how it works and how to change it

**Live page:** https://vamshijogim.github.io/vamfit/ (GitHub Pages, published from the `docs` folder of this repo on every push; free).
The old https://vamfit-gym.netlify.app stays up and will redirect here once Netlify's credits reset.
**This folder is the master copy of the code (since 2026-11-11).** The old copy in `C:\Users\vamsh\.claude\scheduled-tasks\weekly-fitness-tracker-update\` is history only.

## What each file does
| File | Change it when you want to change... |
|---|---|
| `plan_library.py` | Meals (7-day menu), exercises, the 4-week rotation, yoga videos, daily schedule |
| `meals.py` | Calories and protein per food item |
| `start_weights.py` | Starting weight shown for each exercise |
| `gym_card_template.html` | How the page looks and behaves: layout, ticks, score, motivation lines, Waking up / After office, rules |
| `build_card.py` | Joins the data into the page; also holds the time and "job" line shown for each day |
| `build_site.py` | Builds the `docs\` folder (page + offline mode + home-screen icon) |
| `docs\` | The finished website, the only folder GitHub Pages publishes |
| `*_ab_days_2026_27.py` (private, not in the repo) | Kid 1's A/B school days, no-school days, and the 12-office-days check |
| `make_recurring.py`, `cal_text.py` | Wording of the Google Calendar gym events (event IDs are inside) |
| `build_week.py` | Optional: adds a week block to the Fitness Tracker spreadsheet |

## Change something, then publish
1. Edit the file. For a time or a meal, it's usually `plan_library.py` or `build_card.py`.
2. Build: `python build_site.py docs` (run in this folder).
3. Look at it: open `docs\index.html` in a browser.
4. Publish: commit and push (or edit the file on github.com). GitHub Pages republishes `docs` within a minute. Old Netlify route, no longer used:
   - The first time only: `npx netlify-cli login`, then `npx netlify-cli link --name vamfit-gym`. This needs Node.js, which is already installed.
   - Every time: `npx netlify-cli deploy --prod --dir docs`.
5. Phones keep an offline copy. If a change doesn't show, refresh once. After a big change, raise the version in `build_site.py` (`const C = "vamfit-vN"`) so phones pick it up.

## Decisions (Vamshi, 2026-11-11)
- **Privacy:** the public page holds only generic defaults. Personal settings (family, school, office) live in your browser plus an Export file kept in OneDrive, never in the published files. Never put phone, passport or account numbers, or the kids' names and schools, into `docs\`.
- **Google Calendar sync = option (b):** change a setting, then ask Claude to update the calendar. The page does not write to Google Calendar by itself.
- Must work on phone and laptop, and keep working without a Claude membership.

## Settings (step 2, built 2026-11-11)
- The ⚙ button in the page header opens Settings: kid 1 school run (A/B dates, drop/pickup times, college start date), kid 2 (school hours, activities), office (minimum days, which days, arrive/leave), routines (times), and Backup (Export / Import / Reset).
- Settings are saved in each browser. The published page ships only "Kid 1 / Kid 2" placeholders.
- **Your private settings file:** `my-settings\vamfit-settings.json`. Rebuild it with `python make_my_settings.py` after changing the A/B days file or a time in it. On each device, open Settings → Backup → Import and pick this file from OneDrive.
- `patch_settings_step2.py` is the one-time patch that added Settings; `gym_card_template.before-step2.html` is the copy from before it.

## Preview site
- New versions go to **https://vamfit-gym-preview.netlify.app** first (Netlify site `vamfit-gym-preview`). Publish to the live `vamfit-gym` only after Vamshi says yes.
- Self-publish to preview: `npx netlify-cli deploy --prod --dir docs --site vamfit-gym-preview`

## Planned next (from the 11/11 plan, one fresh chat per step)
2. ✅ Settings panel. Live since 2026-11-11, with only the date bar pinned at the top.
3. ✅ Month calendar (📅 button), plus "Did I go to the gym?" at the top of every day and a Deadlines list in Settings, built 2026-11-11. The patch is `patch_calendar_step3.py`; `gym_card_template.before-step3.html` is the copy from before it. Gym taps are saved per day in the browser (`gymYYYYMMDD`).
4. ✅ Hour-by-hour guide (built 2026-11-11). It's at the top of each day and folds away; your choice is remembered.
   - Fixed commitments come first, routines fill around them, and deadlines show on their day.
   - Live weather from Open-Meteo: free, no key, city-level location set in Settings, cached 1 hour, forecast covers the next 16 days.
   - The walk line adapts to dark, rain, heat and cold.
   - The patch is `patch_guide_step4.py`; `gym_card_template.before-step4.html` is the copy from before it.
5. Test at phone and desktop width, deploy as a preview first, and switch the live page only after your yes.
