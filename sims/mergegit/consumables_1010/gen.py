#!/usr/bin/env python3
"""M+ consumables, 2026-10-10, fresh SimC. Balance: DungeonSlice, one raid run (profile 2026-10-07 21:24 = newest
Balance export). Guardian: Patchwerk single actor per run, DPS + DTPS (profile 2026-10-08 14:25 = newest Guardian export)."""
import os
FOODS = "amani_cornucopia arcano_cutlets bloodthistlewrapped_cutlets bloom_skewers blooming_feast braised_blood_hunter buttered_root_crab champions_bento crimson_calamari eversong_pudding farstrider_rations feast_of_knowledge felkissed_filet felberry_figs flora_frenzy foragers_medley fried_bloomtail glitter_skewers harandar_celebration hearthflame_supper impossibly_royal_roast loas_gathering manainfused_stew null_and_void_plate puffer_plate queldorei_medley royal_roast silvermoon_parade silvermoon_standard spellfire_filet spiced_biscuits sunseared_lumifin sunwell_delight sweetandsour_skewers tasty_smoked_tetra twilight_anglers_medley venomspiced_cutlets voidkissed_fish_rolls warped_wise_wings wise_tails".split()
FLASKS = "flask_of_the_magisters_2 flask_of_the_shattered_sun_2 flask_of_the_blood_knights_2 flask_of_thalassian_resistance_2".split()
POTS = "lights_potential_2 draught_of_rampant_abandon_2 potion_of_recklessness_2 liquid_luster_2 potion_of_zealotry_2 alluring_nostrum_2".split()
def variants(base_flask, base_pot, base_food):
    V = [("Z_SANITY", ["trinket2=,id=270164,bonus_id=42/13334/12854,ilevel=334"])]
    V += [(f"FL_{f}", [f"flask={f}"]) for f in FLASKS if f != base_flask]
    V += [(f"PO_{p}", [f"potion={p}"]) for p in POTS if p != base_pot]
    V += [(f"FO_{f}", [f"food={f}"]) for f in FOODS if f != base_food]
    V += [("OIL_oil_of_dawn_2", ["temporary_enchant=main_hand:oil_of_dawn_2"]), ("RUNE_none", ["augmentation=disabled"])]
    return V
# Balance
B = ["name=A_current", "potion=lights_potential_2"]
for n, l in variants("flask_of_the_magisters_2", "lights_potential_2", "harandar_celebration"):
    B += [f"copy={n},A_current"] + l
open("b_variants.simc", "w").write("\n".join(B) + "\n")
open("run_b_DungeonSlice.simc", "w").write("threads=4\niterations=6000\ndeterministic=1\nfight_style=DungeonSlice\n"
    "input=../char_2026-10-07_2124.simc\ninput=b_variants.simc\n")
# Guardian
os.makedirs("g_runs", exist_ok=True)
for n, l in [("A_current", [])] + variants("flask_of_the_blood_knights_2", "lights_potential_2", "harandar_celebration"):
    open(f"g_runs/{n}.simc", "w").write("threads=4\niterations=5000\ndeterministic=1\nfight_style=Patchwerk\ndesired_targets=1\n"
        "input=../../char_guardian_2026-10-08.simc\n" + f"name={n}\n" + "".join(x + "\n" for x in l))
print("ok", len(os.listdir("g_runs")))
