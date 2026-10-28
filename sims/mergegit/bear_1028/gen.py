#!/usr/bin/env python3
"""Guardian 2026-10-28 stage 1 (cases 1-6). Single-actor Patchwerk runs (CLAUDE.md s5), two models:
  pull = 5 heroic tank dummies all attacking; boss = one default (Mythic) dummy.
Baseline char_guardian_2026-10-28.simc = PROVISIONAL (10-21 17:31 tank export + chest Lunar Raiment 334 redirect 281236,
Bardiche 341); no 10-28 export was available. Every variant changes only what its name says.

    python3 gen.py            -> runs_pull/*.simc, runs_boss/*.simc"""
import os
tal = open("../char_guardian_2026-10-28.simc").read().split("\ntalents=")[1].split("\n")[0]
PULL = "".join(f"tank_dummy=Mob{i}\ntank_dummy_type=heroic\n" for i in range(1, 6))
BOSS = "desired_targets=1\n"
CB = "12214/13667/12497/13751/14004/8960/13836"          # crafted base bonus ids (same as the worn crafted wrist/Pikestaff)
STONE = "/13771"                                        # Hunter's Ritual Stone (2nd embellishment: wrist Arcanoweave is the 1st)
PAIRS = {"HV": "36/40", "CH": "32/36", "MV": "49/40", "HM": "36/49", "CV": "32/40"}
def belt(st, stone): return f"waist=,id=244573,bonus_id={CB}{STONE if stone else ''},crafted_stats={st},crafting_quality=5,ilevel=331"
def gloves(st, stone): return f"hands=,id=244575,bonus_id={CB}{STONE if stone else ''},crafted_stats={st},crafting_quality=5,ilevel=331"
def mist(il, ench=False):
    b = "6652/13696/13662/" + ("12846" if il == 321 else "12854")
    return f"hands=,id=272241,bonus_id={b},content_tuning=6015,ilevel={il}" + (",enchant_id=8730" if ench else "")
SUBJ = "hands=,id=193758,enchant_id=8730,bonus_id=13440/6652/13662/12699/12846,ilevel=321"   # worn gloves
CHEST_OLD = "chest=,id=271531,enchant_id=7987,bonus_id=6652/13440/13690/13698/12846,redirected_base_stats=239048,ilevel=321"
def chest(red, il):
    b = "6652/13440/13690/13698/12846" if il == 321 else "6652/13690/13698/13334/12854"
    return f"chest=,id=271531,enchant_id=7987,bonus_id={b},redirected_base_stats={red},ilevel={il}"
def cloak(iid, il): return f"back=,id={iid},bonus_id=6652/13662/{'12846' if il == 321 else '12854'},content_tuning=6015,ilevel={il}"
RING = lambda slot, iid, il, b: f"{slot}=,id={iid},enchant_id=8025,gem_id=240916,bonus_id={b},ilevel={il}"
SW = lambda s: RING(s, 281029, 334, "6652/13668/13334/12849")
BB = lambda s: RING(s, 268266, 321, "6652/13668/13334/12846")
RB = lambda s: RING(s, 159459, 321, "13440/6652/13668/12699/12846")
AM = lambda s: RING(s, 273792, 321, "13440/6652/13668/12699/12846")
V = {"A_base": [], "Z_SANITY": ["trinket2=,id=270165,bonus_id=6652/13334/12854,ilevel=334"],
     "Z2_rings_swapped": [BB("finger2"), RB("finger1")]}
# case 1: Utility Belt pairs x Ritual Stone
for k, st in PAIRS.items():
    for stone in (True, False):
        V[f"C1_belt_{k}_{'stone' if stone else 'nostone'}"] = [belt(st, stone)]
# case 2: vendor grips vs worn gloves; crafted gloves
V["C2_mist321"] = [mist(321)]
V["C2_mist334"] = [mist(334)]
V["C2_mist321_with8730"] = [mist(321, True)]
V["C2_noEnchant_on_worn_gloves"] = [SUBJ.replace(",enchant_id=8730", "")]
for k in ("HV", "CH", "CV"):
    for stone in (True, False):
        V[f"C2_craftgloves_{k}_{'stone' if stone else 'nostone'}"] = [gloves(PAIRS[k], stone)]
# case 3: plan
V["C3_plan_CHbelt_stone+mist321"] = [belt(PAIRS["CH"], True), mist(321)]
V["C3_plan_CHbelt_stone+mist334"] = [belt(PAIRS["CH"], True), mist(334)]
V["C3_plan_CHbelt_nostone+mist321"] = [belt(PAIRS["CH"], False), mist(321)]
# case 4: chest redirect
V["C4_chest_old239048_321"] = [CHEST_OLD]
V["C4_chest_281236_321"] = [chest(281236, 321)]
V["C4_chest_239048_334"] = [chest(239048, 334)]
# case 5: cloaks
for n, iid in (("Pledgebearer", 272230), ("Pyrewalker", 272225)):
    V[f"C5_{n}_321"] = [cloak(iid, 321)]
    V[f"C5_{n}_334"] = [cloak(iid, 334)]
# case 6: rings (baseline = Bubbleband f1 + Ritual Binder f2)
V["C6_Swarm+Bubble"] = [SW("finger1"), BB("finger2")]
V["C6_Swarm+RitualBinder"] = [SW("finger1"), RB("finger2")]
V["C6_Swarm+Amani"] = [SW("finger1"), AM("finger2")]
V["C6_Bubble+Amani"] = [BB("finger1"), AM("finger2")]
if __name__ == "__main__":
    for d, enemy, it in (("runs_pull", PULL, 5000), ("runs_boss", BOSS, 5000)):
        os.makedirs(d, exist_ok=True)
        for n, lines in V.items():
            open(f"{d}/{n}.simc", "w").write(f"threads=4\niterations={it}\ndeterministic=1\nfight_style=Patchwerk\n{enemy}"
                f"input=../../char_guardian_2026-10-28.simc\ntalents={tal}\nname={n}\n" + "".join(l + "\n" for l in lines))
    print(len(V), "variants x 2 models")
