# -*- coding: utf-8 -*-
"""Food database for the VamFit plan: name -> (cal, protein_g) per stated portion (approximate standard values).
Add new items here when a dish is swapped in; plan_library.py computes every day's totals from it."""
DB = {
 "Ragi ganji (30 g ragi + buttermilk)": (140, 4),
 "Greek yogurt, plain nonfat, 1 cup": (130, 23),
 "Greek yogurt 1/2 cup": (65, 11.5),
 "Whey, 1 scoop in water": (120, 24),
 "Boiled egg": (70, 6),
 "Egg white": (17, 3.6),
 "Sweet corn kernels, boiled, 1 cup": (135, 5),
 "Corn on the cob, roasted, 1 ear": (130, 5),
 "Steamed moong sprouts, 1 cup": (105, 7),
 "Roasted chana, 50 g": (185, 11),
 "Makhana, 30 g": (105, 3),
 "Chana sundal, 1 cup cooked": (270, 14.5),
 "Guava, 1 medium": (50, 2),
 "Apple, 1 medium": (95, 0.5),
 "Orange, 1 medium": (62, 1.2),
 "Soya chunks/granules, dry 30 g": (103, 15.6),
 "Soya chunks/granules, dry 75 g": (259, 39),
 "Soya chunks/granules, dry 100 g": (345, 52),
 "Tofu, firm, 100 g": (144, 17),
 "Air-fried tofu cubes, 100 g (1 tsp oil)": (150, 17),
 "Paneer, 150 g": (398, 27),
 "Chicken breast, cooked, 200 g": (330, 62),
 "Dal (toor/moong), cooked, 1 cup": (200, 14),
 "Rice, cooked, 1 cup": (200, 4),
 "Rice, cooked, 1.25 cup": (250, 5),
 "Millet (foxtail), cooked, 1 cup": (175, 6),
 "Jowar roti, 1": (110, 3),
 "Ragi sangati ball, 1": (150, 4),
 "Veg curry/palya, 1 cup (1 tsp oil)": (100, 3),
 "Sambar, 1 cup": (130, 7),
 "Sambar, 1.5 cup": (195, 10.5),
 "Oil/ghee, 1 tsp": (40, 0),
 "Cashews, 8": (45, 1.6),
 "Gravy base (onion-tomato-spice, 1 tsp oil)": (90, 2),
 "Cashew-methi gravy": (110, 4),
 "Gongura gravy": (80, 2),
}


def tot(items):
    c = p = 0.0
    for k, n in items:
        c += DB[k][0] * n
        p += DB[k][1] * n
    return c, p
