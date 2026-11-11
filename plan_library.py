# -*- coding: utf-8 -*-
"""RESTART plan (2026-10-22) - single source for tracker block, calendar text and SKILL.md."""
from urllib.parse import quote_plus
from meals import DB, tot  # same folder

YT = lambda s: "https://www.youtube.com/results?search_query=" + quote_plus(s)
GYM = "LA Fitness, 6345 Custer Bridges Rd, Frisco, TX 75035"

# ---------------------------------------------------------------- MEALS
DB.update({
    "Apple, 1 medium": (95, 0.5),
    "Orange, 1 medium": (62, 1.2),
})
G = "Greek yogurt, plain nonfat, 1 cup"
GAN = ("Ragi ganji (30 g ragi + buttermilk)", 1)
WHEY = ("Whey, 1 scoop in water", 1)

# day -> type, snack(text, items), dinner(dish, plate, items), prep
MEALS = {
 "Sunday": dict(type="Non-veg (Chicken + Egg)",
   snack=("Egg-corn chaat: 2 boiled eggs + 1 cup boiled corn + 1 cup Greek yogurt + 1 apple, lemon + chaat masala",
          [("Boiled egg", 2), ("Sweet corn kernels, boiled, 1 cup", 1), (G, 1), ("Apple, 1 medium", 1)]),
   whey="5:15 PM (rest day)",
   dish="Raju Gari Kodi Pulao (chicken pulao) + onion raita + dal",
   plate="200 g chicken, 1.25 cup pulao rice, 8 cashews, 1 cup Greek-yogurt raita, 1 cup dal",
   items=[("Chicken breast, cooked, 200 g", 1), ("Rice, cooked, 1.25 cup", 1), ("Oil/ghee, 1 tsp", 1), ("Cashews, 8", 1),
          (G, 1), ("Dal (toor/moong), cooked, 1 cup", 1)],
   prep="Same morning: soak rice 20 min, grind green paste (chilli-coriander-mint). Boil 2 eggs + corn for the snack.",
   recipe="Raju gari kodi pulao telugu"),
 "Monday": dict(type="Veg",
   snack=("Corn-sprouts chaat: 1 cup corn + 1 cup steamed moong sprouts + 1 cup Greek yogurt + 1 apple, lemon",
          [("Sweet corn kernels, boiled, 1 cup", 1), ("Steamed moong sprouts, 1 cup", 1), (G, 1), ("Apple, 1 medium", 1)]),
   whey="5:45 PM (after gym)",
   dish="Veg Kheema Biryani (soya kheema) + raita",
   plate="100 g dry soya granules cooked into the biryani, 1.25 cup biryani rice, 1 cup veg, 1 cup raita, 1/2 cup dal",
   items=[("Soya chunks/granules, dry 100 g", 1), ("Rice, cooked, 1.25 cup", 1), ("Veg curry/palya, 1 cup (1 tsp oil)", 1),
          ("Oil/ghee, 1 tsp", 2), (G, 1), ("Dal (toor/moong), cooked, 1 cup", 0.5)],
   prep="Sunday night: soak soya granules 10 min in hot water + squeeze, chop veg fine, hang curd for raita, sprout moong.",
   recipe="veg kheema biryani soya telugu"),
 "Tuesday": dict(type="Veg (Paneer)",
   snack=("Chana-yogurt bowl: 50 g roasted chana (putnalu) + 1.5 cup Greek yogurt + 1 guava",
          [("Roasted chana, 50 g", 1), (G, 1.5), ("Guava, 1 medium", 1)]),
   whey="5:45 PM (after gym)",
   dish="Methi ka Chaman (paneer-methi) + jowar roti + dal",
   plate="150 g paneer in the gravy, 2 jowar roti, 1 cup dal, 1.5 cup Greek-yogurt raita",
   items=[("Paneer, 150 g", 1), ("Cashew-methi gravy", 1), ("Jowar roti, 1", 2), ("Dal (toor/moong), cooked, 1 cup", 1), (G, 1.5)],
   prep="Monday night: pick methi leaves, salt + squeeze them, soak cashews for the paste, soak dal.",
   recipe="methi chaman paneer recipe"),
 "Wednesday": dict(type="Non-veg (Egg)",
   snack=("Corn-egg bhurji: 1 egg + 3 whites scrambled with onion + 1 cup corn + 1 cup Greek yogurt + 1 apple",
          [("Boiled egg", 1), ("Egg white", 3), ("Sweet corn kernels, boiled, 1 cup", 1), (G, 1), ("Apple, 1 medium", 1)]),
   whey="5:45 PM (after gym)",
   dish="Andhra Kodi Guddu Pulusu (egg curry) + rice + dal",
   plate="3 eggs + 5 egg whites in the pulusu, 1.25 cup rice, 1 cup dal, 1 cup veg, 1 cup Greek-yogurt raita",
   items=[("Boiled egg", 3), ("Egg white", 5), ("Gravy base (onion-tomato-spice, 1 tsp oil)", 1), ("Rice, cooked, 1.25 cup", 1),
          ("Dal (toor/moong), cooked, 1 cup", 1), ("Veg curry/palya, 1 cup (1 tsp oil)", 1), (G, 1)],
   prep="Tuesday night: boil eggs, soak tamarind, soak dal.",
   recipe="kodi guddu pulusu andhra telugu"),
 "Thursday": dict(type="Veg",
   snack=("Soya-makhana chaat: 30 g dry soya chunks (boiled, squeezed) + 30 g roasted makhana + 1 cup Greek yogurt + 1 orange",
          [("Soya chunks/granules, dry 30 g", 1), ("Makhana, 30 g", 1), (G, 1), ("Orange, 1 medium", 1)]),
   whey="5:45 PM (after gym)",
   dish="Gongura Soya Chunks curry + rice + jowar roti + dal",
   plate="75 g dry soya chunks in gongura gravy, 1.25 cup rice, 1 jowar roti, 1 cup dal, 1 cup Greek-yogurt raita",
   items=[("Soya chunks/granules, dry 75 g", 1), ("Gongura gravy", 1), ("Oil/ghee, 1 tsp", 1), ("Rice, cooked, 1.25 cup", 1),
          ("Jowar roti, 1", 1), ("Dal (toor/moong), cooked, 1 cup", 1), (G, 1)],
   prep="Wednesday night: wash + dry gongura, soak soya chunks, soak dal.",
   recipe="gongura soya chunks curry telugu"),
 "Friday": dict(type="Non-veg (Chicken)",
   snack=("Corn-tofu bites: 1 roasted corn on the cob + 100 g air-fried tofu cubes + 1 cup Greek yogurt + 1 guava",
          [("Corn on the cob, roasted, 1 ear", 1), ("Air-fried tofu cubes, 100 g (1 tsp oil)", 1), (G, 1), ("Guava, 1 medium", 1)]),
   whey="5:45 PM (after gym)",
   dish="Andhra Kodi Kura (chicken curry) + sambar + rice",
   plate="200 g skinless chicken curry, 1 cup sambar, 1.25 cup rice, 1 cup veg, 1/2 cup Greek-yogurt raita, 1/2 cup dal",
   items=[("Chicken breast, cooked, 200 g", 1), ("Gravy base (onion-tomato-spice, 1 tsp oil)", 1), ("Sambar, 1 cup", 1), ("Rice, cooked, 1.25 cup", 1),
          ("Veg curry/palya, 1 cup (1 tsp oil)", 1), ("Greek yogurt 1/2 cup", 1), ("Dal (toor/moong), cooked, 1 cup", 0.5)],
   prep="Thursday night: cut + marinate chicken (curd, turmeric, chilli), soak toor dal, press tofu.",
   recipe="andhra chicken curry telugu"),
 "Saturday": dict(type="Veg",
   snack=("Chana sundal (1 cup) + 1 cup Greek yogurt + 1 orange",
          [("Chana sundal, 1 cup cooked", 1), (G, 1), ("Orange, 1 medium", 1)]),
   whey="5:15 PM (rest day)",
   dish="Tofu Pepper Fry + sambar + foxtail millet (korralu)",
   plate="300 g tofu pepper fry, 1.5 cup sambar, 1 cup foxtail millet, 1 cup veg, 1 cup Greek-yogurt raita",
   items=[("Tofu, firm, 100 g", 3), ("Oil/ghee, 1 tsp", 1), ("Sambar, 1.5 cup", 1), ("Millet (foxtail), cooked, 1 cup", 1),
          ("Veg curry/palya, 1 cup (1 tsp oil)", 1), (G, 1)],
   prep="Friday night: soak kabuli chana for sundal, press + cube tofu, soak toor dal, wash millet.",
   recipe="tofu pepper fry indian"),
}
DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

def meal_totals(day):
    m = MEALS[day]
    g = tot([GAN]); w = tot([WHEY]); s = tot(m["snack"][1]); d = tot(m["items"])
    return dict(ganji=g, whey=w, snack=s, dinner=d,
                cal=g[0] + w[0] + s[0] + d[0], pro=g[1] + w[1] + s[1] + d[1])

# ---------------------------------------------------------------- EXERCISE
# move = (name, sets, rest, cue, search, tag)  tag: Anchor / New
def M(name, sets, rest, cue, q=None, tag="New"):
    return dict(name=name, sets=sets, rest=rest, cue=cue, link=YT(q or (name + " proper form")), tag=tag)

WARM = M("Bike warm-up + arm circles", "5 min easy", "-", "Easy pace, just get warm; 10 arm circles each way.", "5 minute gym warm up beginner", "Fixed")
WALL = M("Wall Squat (BP protocol)", "4 x 2 min", "2 min",
         "Back flat on the wall, slide down until it feels like 5-6 out of 10 effort (you can still talk). "
         "Breathe normally the WHOLE time - never hold your breath. Stand up and rest 2 min between holds. "
         "Too hard? Slide up higher. Skip if resting BP >= 160/100 that day.", "isometric wall squat blood pressure", "Fixed")
INCL = M("Incline Treadmill Walk", "10 min", "-", "Incline 6-10, 2.8-3.2 mph, conversational pace (fat burn, BP-friendly).",
         "incline treadmill walk beginner form", "Fixed")
STRETCH = M("Cool-down stretch", "3-5 min", "-", "Chest, lats, hips, hamstrings - 30 s each, slow breathing.", "post workout stretch 5 minutes", "Fixed")

# Each day: list of sections (title, [moves]).  ROT = slot variants for weeks 1-3 (week 4 = week 1 moves, deload).
def day_plan(day, wk):
    """Week wk of the plan (Week 1 = week of Oct 26, 2026). 4-week cycles: weeks 1-3 rotate every non-anchor
    move, week 4 = deload (week-1 moves, one set fewer). Odd cycles (weeks 5-8, 13-16, ...) use CYCLE2 anchors."""
    title, secs = _fixed_plan(day, wk)
    cycle2 = ((wk - 1) // 4) % 2 == 1
    deload = (wk - 1) % 4 == 3
    out = []
    for sec, moves in secs:
        new = []
        for m in moves:
            if cycle2 and m["tag"] == "Anchor" and m["name"] in CYCLE2:
                m = CYCLE2[m["name"]]
            if deload and m["tag"] in ("Anchor", "New") and m["sets"][:1].isdigit() and " x " in m["sets"]:
                n, rest = m["sets"].split(" x ", 1)
                if n.isdigit() and int(n) > 1:
                    m = dict(m, sets=f"{int(n) - 1} x {rest}", cue=m["cue"] + " DELOAD week: ~20% lighter.")
            new.append(m)
        out.append((sec, new))
    if deload:
        title += " - DELOAD WEEK"
    return title, out


CYCLE2 = {
    "Machine Chest Press": M("Plate-Loaded Chest Press (Hammer Strength)", "3 x 10-12", "90 s", "Handles at mid-chest, press out, 2-sec return. Exhale as you push.", tag="Anchor"),
    "Seated Cable Row": M("Chest-Supported Machine Row", "3 x 10-12", "90 s", "Chest on the pad, pull handles to ribs, squeeze shoulder blades.", tag="Anchor"),
    "Leg Press": M("Hack Squat Machine (light-moderate)", "3 x 10-12", "90 s", "Back flat on the pad, lower to ~90 deg knees, push through heels. Exhale up.", tag="Anchor"),
    "Goblet Squat to Bench": M("Smith Machine Box Squat (light)", "3 x 10", "90 s", "Bar on upper back, sit back to the bench, stand tall. Exhale up, never hold breath.", tag="Anchor"),
    "Machine Shoulder Press": M("Seated Dumbbell Shoulder Press", "3 x 10", "90 s", "Back supported, press DBs up from ear height, don't arch. Exhale up.", tag="Anchor"),
    "Assisted Pull-Up (machine)": M("Lat Pulldown (underhand grip)", "3 x 10-12", "90 s", "Palms facing you, shoulder width, pull to upper chest.", tag="Anchor"),
    "Dumbbell Romanian Deadlift": M("Dumbbell Sumo Deadlift (light)", "3 x 10", "90 s", "Wide stance, toes out, one DB between legs, hips back, stand tall. Exhale up.", tag="Anchor"),
    "Hip Thrust (bench)": M("Glute Bridge Machine / Barbell Glute Bridge", "3 x 12", "75 s", "Drive hips up to a straight line, squeeze 1 s, slow lower.", tag="Anchor"),
}


WALK = M("Walk after dinner", "10 min minimum", "-", "Straight out after dinner, shoes by the door. Stay out longer if you feel like it. Dark Nov-Feb: lit route + LED clip, or indoors.",
         "10 minute walk after eating blood sugar", "Home")


def _yoga(day):
    return dict(M("Yoga: " + YOGA[day][0], "30 min", "-", YOGA_RULES, tag="Home"), link=YOGA[day][1])


def _fixed_plan(day, wk):
    """The original 5-day split at the original times (Vamshi 2026-11-01: "at least 5 days a week", "keep the same time"),
    plus a 10-min walk as the last tick of every day. Sat/Sun stay recovery + yoga."""
    after = ("After dinner", [WALK])
    if day == "Saturday":
        return ("RECOVERY - yoga, easy walk, BP wall squat", [("5:05 AM", [_yoga(day)]),
                ("8:00 AM", [M("Easy walk", "45-60 min", "-", "Conversational pace.", "easy walking pace benefits", "Home"), WALL]), after])
    if day == "Sunday":
        return ("REST DAY - yoga + walk", [("5:05 AM", [_yoga(day)]), after])
    title, secs = _day_plan(day, wk)
    morning = [("5:05 AM (bonus)", [_yoga(day)])] if day in YOGA else []
    return title, morning + secs + [after]


def _day_plan(day, wk):
    """Move library: the original 5-day split. _fixed_plan picks from it."""
    w = (wk - 1) % 4          # 0,1,2,3
    v = 0 if w == 3 else w    # week 4 deload repeats week-1 moves
    pick = lambda opts: opts[v]
    if day == "Monday":
        return ("UPPER A - chest, back, shoulders, arms + ABS (flexion) + BP wall squat", [
          ("1) Warm-up (5 min)", [WARM]),
          ("2) Upper body (~40 min)", [
            M("Machine Chest Press", "3 x 10-12", "90 s", "Handles at mid-chest, press out, 2-sec return. Exhale as you push.", tag="Anchor"),
            M("Seated Cable Row", "3 x 10-12", "90 s", "Sit tall, pull handle to belly button, squeeze shoulder blades, no rocking.", tag="Anchor"),
            pick([M("Incline Dumbbell Press", "3 x 10", "75 s", "Bench at 30 deg, press over upper chest, control down."),
                  M("Incline Chest Press Machine", "3 x 10-12", "75 s", "Seat so handles start at upper chest, press up and out."),
                  M("Flat Dumbbell Press (neutral grip)", "3 x 10", "75 s", "Palms facing each other, elbows ~45 deg, slow lower.")]),
            pick([M("Lat Pulldown (neutral grip)", "3 x 10-12", "75 s", "V-handle, pull to upper chest, elbows down to ribs."),
                  M("Half-Kneeling Single-Arm Cable Pulldown", "3 x 10/arm", "60 s", "Kneel side-on, pull elbow down to your hip, stretch up."),
                  M("Wide-Grip Lat Pulldown", "3 x 10-12", "75 s", "Grip wider than shoulders, pull bar to collarbone, no leaning back.")]),
            pick([M("Dumbbell Lateral Raise", "2 x 12-15", "45 s", "Light weight, slight elbow bend, raise to shoulder height, 2-s lower."),
                  M("Single-Arm Cable Lateral Raise", "2 x 12/side", "45 s", "Cable at lowest setting, raise arm out to shoulder height, 2-s lower."),
                  M("Machine Lateral Raise", "2 x 12-15", "45 s", "Pads on outer arms, raise to shoulder height, slow return.")]),
            pick([M("Superset: DB Hammer Curl + Rope Pushdown", "2 x 12 each", "60 s", "Curl with palms facing in; then rope pushdown, elbows pinned."),
                  M("Superset: Cable Bar Curl + Overhead DB Triceps Ext.", "2 x 12 each", "60 s", "Elbows still on the curl; one DB overhead, lower behind head."),
                  M("Superset: Incline DB Curl + DB Kickback", "2 x 12 each", "60 s", "Lie back at 60 deg for curls; hinge, upper arm still for kickbacks.")]),
          ]),
          ("3) Abs - flexion (~8 min)", pick([
            [M("Bicycle Crunch (slow)", "3 x 12/side", "45 s", "Elbow toward opposite knee, shoulder blade off floor, exhale on each twist."),
             M("Reverse Crunch", "3 x 12", "45 s", "Knees bent 90 deg, curl hips off the floor toward ribs, lower slowly.")],
            [M("Stability-Ball Crunch", "3 x 12-15", "45 s", "Lower back on the ball, curl ribs toward hips a few inches, exhale up."),
             M("Toe-Touch Crunch", "3 x 12", "45 s", "Legs straight up, reach hands toward toes, exhale as you reach.")],
            [M("Tuck V-Up (bent knee)", "3 x 10", "45 s", "Sit on the floor, lean back, pull knees and chest together, exhale."),
             M("Heel Taps (obliques)", "3 x 12/side", "45 s", "Knees bent, shoulders up, reach side to side to touch heels.")],
          ])),
          ("4) BP finisher (14 min)", [WALL]),
          ("5) Cool-down", [STRETCH]),
        ])
    if day == "Tuesday":
        return ("LOWER A - quads, glutes, calves + ABS (anti-extension)", [
          ("1) Warm-up (7 min)", [WARM, pick([M("Banded Side Walks", "2 x 15 steps/side", "30 s", "Mini-band above knees, quarter squat, keep band tight."),
                                             M("Bodyweight Box Squat", "2 x 10", "30 s", "Sit back to a bench, stand up tall, slow and smooth."),
                                             M("Glute Bridge (bodyweight)", "2 x 12", "30 s", "Feet flat, drive hips up, squeeze glutes 1 s.")])]),
          ("2) Legs (~38 min)", [
            M("Leg Press", "3 x 10-12", "90 s", "Feet shoulder-width, lower to ~90 deg knees, push through heels. Exhale on the push - never hold breath.", tag="Anchor"),
            M("Goblet Squat to Bench", "3 x 10", "90 s", "Dumbbell at chest, sit back to touch the bench, stand tall.", tag="Anchor"),
            pick([M("Dumbbell Reverse Lunge", "2 x 10/leg", "60 s", "Step back, lower back knee toward the floor, push through front heel."),
                  M("Split Squat (static, bodyweight/light DB)", "2 x 10/leg", "60 s", "Long stance, drop straight down, hold a rail if needed."),
                  M("Walking Lunge (bodyweight)", "2 x 10/leg", "60 s", "Long steps, tall chest, soft knee touch-down.")]),
            pick([M("Leg Extension", "2 x 12-15", "60 s", "Pad on lower shin, straighten knees, 1-sec squeeze, 2-sec lower."),
                  M("Lateral Step-Down (low box)", "2 x 10/leg", "60 s", "Stand on a low step, slowly tap the other heel to the floor, knee over toes."),
                  M("Leg Extension (3-sec lower)", "2 x 12", "60 s", "Same machine, lighter weight, slow 3-second lowering.")]),
            pick([M("Hip Abduction Machine", "2 x 15", "45 s", "Sit tall, press knees out, 1-sec hold, slow return."),
                  M("Cable Hip Abduction", "2 x 12/side", "45 s", "Ankle strap, stand side-on, sweep leg out, don't lean."),
                  M("Side-Lying Band Abduction", "2 x 15/side", "45 s", "Band above knees, lie on side, lift top knee/leg slowly.")]),
            pick([M("Standing Calf Raise", "3 x 15", "45 s", "Rise onto the balls of your feet, pause, lower slowly."),
                  M("Leg-Press Calf Raise", "3 x 15", "45 s", "Balls of feet on the platform edge, push through toes, slow return."),
                  M("Single-Leg DB Calf Raise", "2 x 12/leg", "45 s", "Hold a rail + dumbbell, full range, slow.")]),
          ]),
          ("3) Abs - anti-extension (~8 min)", pick([
            [M("Kneeling Ab Rollout (wheel or ball)", "3 x 8", "60 s", "From knees, roll out only as far as your back stays flat, exhale coming back."),
             M("Dead Bug", "3 x 8/side", "45 s", "Low back pressed down, extend opposite arm + leg slowly, breathe out.")],
            [M("Stability-Ball Stir-the-Pot (from knees)", "3 x 6 circles/dir", "60 s", "Forearms on ball, small circles, hips still, keep breathing."),
             M("Hollow Tuck Hold", "3 x 20 s", "45 s", "Knees bent, low back down, arms by ears - breathe the whole time.")],
            [M("Long-Lever Plank", "3 x 20 s", "45 s", "Elbows a little ahead of shoulders, squeeze glutes, breathe."),
             M("Band Dead Bug", "3 x 8/side", "45 s", "Hold a band anchored behind you, arms straight, lower opposite leg slowly.")],
          ])),
          ("4) Finisher", [pick([INCL,
                                 M("Bike Intervals", "10 min", "-", "30 s brisk / 60 s easy x 6, then easy spin. Brisk = breathing hard but can talk.", "stationary bike interval beginner", "Fixed"),
                                 INCL])]),
          ("5) Cool-down", [STRETCH]),
        ])
    if day == "Wednesday":
        return ("ATHLETIC DAY - agility + full-body circuit + ABS (anti-rotation) + BP wall squat", [
          ("1) Warm-up (5 min)", [WARM]),
          ("2) Agility (~12 min, walk-jog pace)", pick([
            [M("Agility Ladder Lateral In-In-Out-Out", "3 x 1 min", "30 s", "Side-on to the ladder, both feet in, both out, move along. Walk it first."),
             M("5-10-5 Shuttle (walk-jog)", "3 rounds", "45 s", "Cones 5 yd apart: start middle, 5 right, 10 left, 5 back. Bend knees to turn."),
             M("Carioca (grapevine)", "3 x 20 s/dir", "30 s", "Sideways, trailing foot crosses behind then in front, hips rotate.")],
            [M("Agility Ladder Icky Shuffle", "3 x 1 min", "30 s", "In-in-out pattern moving diagonally down the ladder."),
             M("T-Drill (walk-jog)", "3 rounds", "45 s", "Forward 5 yd, shuffle left, shuffle right, shuffle back, backpedal."),
             M("Lateral Shuffle to Cone Touch", "3 x 20 s", "30 s", "Two cones 4 yd apart, shuffle and touch each cone, stay low.")],
            [M("Agility Ladder One-Foot Run", "3 x 1 min", "30 s", "One foot in each box, quick light steps, arms pumping."),
             M("Cone Box Drill", "3 rounds", "45 s", "4 cones in a 5-yd square: forward, shuffle, backpedal, shuffle."),
             M("Low-Impact Speed Skaters", "3 x 20 s", "30 s", "Step wide side to side, land soft, tap the other foot behind. Step, don't jump.")],
          ])),
          ("3) Full-body circuit (3 rounds, 60 s rest between rounds, ~15 min)", pick([
            [M("Incline Push-Up (bench)", "10", "-", "Hands on a bench, body straight, chest to bench, exhale up."),
             M("Cable Face Pull", "15", "-", "Rope at eye height, pull to forehead, elbows high."),
             M("Bodyweight Step-Up", "10/leg", "-", "Knee-height box, drive through front heel, step down slowly."),
             M("Farmer's Carry (light-moderate)", "30 s", "-", "Dumbbell in each hand, walk tall, keep breathing.")],
            [M("Standing Cable Chest Press", "12", "-", "Cables at chest height, staggered stance, press forward."),
             M("Band Pull-Apart", "15", "-", "Arms straight at chest height, pull the band to your chest."),
             M("Goblet Box Squat (light)", "10", "-", "Light DB, sit to the bench, stand tall."),
             M("Suitcase Carry", "30 s/side", "-", "One dumbbell, walk without leaning, breathe.")],
            [M("Push-Up (knees or bench)", "8-10", "-", "Body straight from knees/feet, chest down, exhale up."),
             M("Inverted Row (high Smith bar)", "8-10", "-", "Bar at waist height, body straight, pull chest to bar."),
             M("Reverse Lunge (bodyweight)", "8/leg", "-", "Step back, lower, push through the front heel."),
             M("Farmer's Carry (heavier)", "30 s", "-", "Slightly heavier than week 1, tall posture, keep breathing.")],
          ])),
          ("4) Abs - anti-rotation + side (~8 min)", pick([
            [M("Cable Pallof Press", "3 x 10/side", "45 s", "Side-on to a chest-height cable, press straight out, resist the twist, exhale."),
             M("Side Plank (knees or feet)", "2 x 25 s/side", "45 s", "Straight line, hips up, breathe."),
             M("Bird Dog", "2 x 8/side", "30 s", "Opposite arm + leg long, 2-s hold, hips level.")],
            [M("Half-Kneeling Cable Lift (low to high)", "3 x 10/side", "45 s", "Kneel side-on, pull rope from low hip to high across the body, hips still."),
             M("Side Plank with Reach-Through", "2 x 8/side", "45 s", "From side plank, thread top arm under and back up, slow."),
             M("Dead Bug", "2 x 8/side", "30 s", "Low back down, slow opposite arm + leg.")],
            [M("Pallof Press Walk-Out", "3 x 5 steps/side", "45 s", "Hold the press, step sideways away from the cable and back."),
             M("Suitcase March", "2 x 30 s/side", "45 s", "One DB at your side, march in place, don't lean."),
             M("Bird Dog Row", "2 x 8/side", "30 s", "On a bench, one hand on bench, row a light DB, keep hips square.")],
          ])),
          ("5) BP finisher (14 min)", [WALL]),
          ("6) Cool-down", [STRETCH]),
        ])
    if day == "Thursday":
        return ("UPPER B - shoulders, back, chest, arms + ABS (lower abs)", [
          ("1) Warm-up (5 min)", [WARM]),
          ("2) Upper body (~40 min)", [
            M("Machine Shoulder Press", "3 x 10-12", "90 s", "Handles at shoulder height, press up, don't arch lower back. Exhale up.", tag="Anchor"),
            M("Assisted Pull-Up (machine)", "3 x 6-8", "90 s", "Enough assist for clean reps, chin over bar, slow lower.", tag="Anchor"),
            pick([M("One-Arm Dumbbell Row", "3 x 10/arm", "60 s", "Hand + knee on bench, pull DB to hip, flat back."),
                  M("Chest-Supported Dumbbell Row", "3 x 10-12", "60 s", "Chest on a 30-45 deg bench, row DBs to hips."),
                  M("Single-Arm Cable Row", "3 x 10/arm", "60 s", "Low cable, pull elbow back past ribs, slight twist allowed.")]),
            pick([M("Machine Pec Fly", "2 x 12-15", "60 s", "Slight elbow bend, bring handles together, slow return."),
                  M("Cable Crossover (high to low)", "2 x 12-15", "60 s", "Pulleys high, sweep hands down and together."),
                  M("Cable Fly (low to high)", "2 x 12-15", "60 s", "Pulleys low, sweep up and together to chest height.")]),
            pick([M("Reverse Pec Deck (rear delts)", "2 x 15", "45 s", "Face the pad, arms out wide to a T, squeeze, slow return."),
                  M("Cable Rear Delt Fly", "2 x 12-15", "45 s", "Cables crossed at shoulder height, pull out wide."),
                  M("Cable Face Pull", "2 x 15", "45 s", "Rope to forehead, elbows high, squeeze.")]),
            pick([M("Superset: Cable Bar Curl + Overhead Cable Triceps Ext.", "2 x 12 each", "60 s", "Elbows pinned on curls; face away, rope overhead, straighten arms."),
                  M("Superset: Incline DB Curl + Close-Grip Bench Push-Up", "2 x 10-12 each", "60 s", "Arms hang straight on curls; hands close on a bench, elbows in."),
                  M("Superset: Preacher Curl Machine + Single-Arm Cable Pushdown", "2 x 12 each", "60 s", "Upper arm on pad; one arm at a time on the pushdown.")]),
          ]),
          ("3) Abs - lower abs (~8 min)", pick([
            [M("Captain's Chair Knee Raise", "3 x 10", "45 s", "Back on the pad, lift knees to hip height, slow down, no swinging."),
             M("Bent-Knee Leg Lowers", "2 x 10", "45 s", "On your back, knees bent, lower heels to tap the floor, low back down.")],
            [M("Bench Reverse Crunch", "3 x 12", "45 s", "Hold the bench behind your head, curl hips up, lower slowly."),
             M("Flutter Kicks (small)", "3 x 20 s", "30 s", "Low back pressed down, small fast kicks, breathe.")],
            [M("Captain's Chair Knee Raise with Twist", "3 x 8/side", "45 s", "Lift knees toward one shoulder, then the other."),
             M("Dead Bug Leg Lowers", "2 x 8/side", "45 s", "Arms up, lower one straight leg at a time, low back down.")],
          ])),
          ("4) Finisher", [INCL]),
          ("5) Cool-down", [STRETCH]),
        ])
    if day == "Friday":
        return ("LOWER B - hamstrings, glutes, calves + ABS (rotation + carry) + agility finisher", [
          ("1) Warm-up (7 min)", [WARM, M("Glute Bridge (bodyweight)", "2 x 12", "30 s", "Feet flat, drive hips up, squeeze 1 s.", tag="Fixed")]),
          ("2) Legs (~38 min)", [
            M("Dumbbell Romanian Deadlift", "3 x 10", "90 s", "Soft knees, push hips BACK, DBs to mid-shin, flat back. Exhale coming up.", tag="Anchor"),
            M("Hip Thrust (bench)", "3 x 12", "75 s", "Upper back on a bench, DB on hips (or none), drive up to a straight line, squeeze.", tag="Anchor"),
            pick([M("Seated Leg Curl", "3 x 10-12", "60 s", "Knee in line with the pivot, curl, pause, lower slowly."),
                  M("Lying Leg Curl", "3 x 10-12", "60 s", "Hips down on the pad, curl heels to glutes, slow lower."),
                  M("Stability-Ball Hamstring Curl", "3 x 10", "60 s", "Heels on ball, hips up, roll the ball in and out.")]),
            pick([M("Dumbbell Step-Up", "2 x 10/leg", "60 s", "Knee-height box, whole foot on box, drive through the heel."),
                  M("Bulgarian Split Squat (bodyweight)", "2 x 8/leg", "60 s", "Rear foot on a bench, drop straight down, hold a rail if needed."),
                  M("Single-Leg RDL (bodyweight, hold rail)", "2 x 8/side", "45 s", "Hinge on one leg, back leg long, hips square.")]),
            pick([M("Cable Pull-Through", "2 x 12", "60 s", "Face away from a low cable, hinge hips back, stand tall squeezing glutes."),
                  M("45-Degree Back Extension", "2 x 12", "60 s", "Hips on the pad, hinge down with flat back, rise to a straight line."),
                  M("Cable Glute Kickback", "2 x 12/side", "45 s", "Ankle strap, kick leg back without arching your back.")]),
            pick([M("Seated Calf Raise", "3 x 15", "45 s", "Pad on knees, full range, pause at the top."),
                  M("Standing Calf Raise", "3 x 15", "45 s", "Rise onto the balls of your feet, pause, lower slowly."),
                  M("Leg-Press Calf Raise", "3 x 15", "45 s", "Balls of feet on the platform edge, slow.")]),
          ]),
          ("3) Abs - rotation + carry (~7 min)", pick([
            [M("Cable Woodchop (high to low)", "2 x 10/side", "45 s", "Side-on to a high cable, pull diagonally down across the body, pivot back foot."),
             M("Plank Shoulder Taps (hands on bench)", "2 x 10/side", "45 s", "Hands on a bench, tap opposite shoulder, hips still.")],
            [M("Cable Woodchop (low to high)", "2 x 10/side", "45 s", "Low cable, pull up and across, exhale."),
             M("Suitcase Carry", "2 x 30 s/side", "45 s", "One DB, walk tall without leaning.")],
            [M("Half-Kneeling Pallof Press", "2 x 10/side", "45 s", "Kneel side-on, press out, resist the twist."),
             M("Side Plank Hip Dips", "2 x 8/side", "45 s", "From side plank, lower hip a few inches and lift.")],
          ])),
          ("4) Agility finisher (~8 min)", pick([
            [M("Low-Impact Speed Skaters", "3 x 20 s", "30 s", "Step wide side to side, land soft. Step, don't jump."),
             M("Lateral Shuffle", "3 x 20 s", "30 s", "Low athletic stance, quick side steps, don't cross feet.")],
            [M("Side-to-Side Line Hops (low)", "3 x 20 s", "30 s", "Tiny quick hops over a floor line, or step over if knees complain."),
             M("Agility Ladder Lateral Steps", "3 x 1 min", "30 s", "Sideways, both feet in each box.")],
            [M("Cone Weave (walk-jog)", "3 rounds", "30 s", "5 cones in a line, weave through forward, then backward slowly."),
             M("Backpedal + Sprint-Walk", "3 x 20 yd", "30 s", "Backpedal 10 yd, turn and brisk walk/jog back.")],
          ])),
          ("5) Cool-down", [STRETCH]),
        ])
    raise KeyError(day)

YOGA = {
    "Tuesday":  ("Hips + hamstrings (Boho Beautiful, 30 min)", "https://youtu.be/w2TfswY2_rg"),
    "Thursday": ("Neck + shoulders + upper back (Idan Kirshner, 30 min)", "https://youtu.be/1BvRgpLC2vU"),
    "Saturday": ("Full-body morning flow (Charlie Follows, 30 min)", "https://youtu.be/o347AwF9IDs"),
    "Sunday":   ("Yoga for high blood pressure (BodyWisdom, 30 min)", "https://youtu.be/F4u2AO60gzw"),
}
YOGA_RULES = ("Home, 5:05-5:35 AM. Finish with 3 min slow breathing (in 4 s, out 6 s). No headstand / shoulder stand / "
              "handstand, never hold the breath, come up from forward folds slowly. Spare core class: https://youtu.be/oMOgnSMcfM0")

SCHEDULE = [
    ("5:00 AM", "Wake"),
    ("5:05-5:35 AM", "Yoga at home (Tue, Thu, Sat, Sun). Fri 5:10 AM = weigh-in."),
    ("5:40 AM", "Ragi ganji + saunf water (black coffee OK)"),
    ("6:30 AM", "Leave for office"),
    ("3:00-3:30 PM", "Home -> snack within 10 min. Gym clothes on BEFORE you sit down."),
    ("4:15 PM", "Leave for gym"),
    ("4:30-5:45 PM", "Gym (Mon-Fri)"),
    ("5:45 PM", "Whey in water (weekends 5:15 PM)"),
    ("6:10 PM", "HEAVY early dinner - kitchen closed after"),
    ("6:45 PM", "Walk, 10 min minimum, every day (dark Nov-Feb: lit route + LED clip, or indoors)"),
    ("9:00 PM", "Screens off, wind down"),
    ("9:30 PM", "Sleep"),
]

if __name__ == "__main__":
    for d in DAYS:
        t = meal_totals(d)
        print(d, round(t["cal"]), round(t["pro"]), "snack", round(t["snack"][0]), round(t["snack"][1]), "dinner", round(t["dinner"][0]), round(t["dinner"][1]))
        assert t["cal"] <= 2050 and t["pro"] >= 150, d
    for wk in (1, 2, 3, 4):
        for d in ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"):
            title, secs = day_plan(d, wk)
            n = sum(len(m) for _, m in secs)
            print("W", wk, d, n, "moves")
