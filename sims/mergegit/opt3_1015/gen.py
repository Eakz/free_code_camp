#!/usr/bin/env python3
"""2026-10-15: optimise Balance (owned gear) + consumables for Balance, cat and bear on their M+ builds.
SimC midnight 3dcabb9, live data 12.1.5.70391. Balance baseline = export 2026-10-15 10:58. Pikestaff = as crafted (Mastery/Crit, export 49/32)."""
CB = "12214/13667/12497/13751/14004/8960/13836"
PIKE_HV = f"main_hand=,id=245771,bonus_id={CB}/13771,crafted_stats=49/32,crafting_quality=5,ilevel=331,enchant_id=7983"
TH = "hands=,id=271529,ilevel=321"
BEAR_SET = [PIKE_HV, "waist=,id=272245,ilevel=321", "hands=,id=193758,ilevel=321", "trinket1=,id=270164,ilevel=334"]
CAT_SET = [PIKE_HV, "finger1=,id=158366,ilevel=321,enchant_id=8025,gem_id=240916", "finger2=,id=273792,ilevel=321,enchant_id=8025,gem_id=240916",
           "hands=,id=193758,ilevel=321", "trinket2=,id=270164,ilevel=334"]
# ---- Balance owned sweep
BAL = {
 "NE_Yoke":["neck=,id=251173,ilevel=321,gem_id=240983"], "NE_Graft":["neck=,id=251234,ilevel=321,gem_id=240983"],
 "NE_Strand":["neck=,id=273781,ilevel=321,gem_id=240983"], "BA_Pyrewalker":["back=,id=272225,ilevel=321"],
 "HA_MiststalkerGrips":["hands=,id=272241,ilevel=321"], "HA_TierGauntlets":[TH],
 "WA_Cinch":["waist=,id=272245,ilevel=321"], "WA_Slitherscale308":["waist=,id=271436,bonus_id=41/13696/13662/13333/10844/12838,crafted_stats=40/36,crafting_quality=5,ilevel=308"],
 "FE_Miststalker":["feet=,id=272240,ilevel=321,enchant_id=7963"],
 "SH_Miststalker+TH":["shoulder=,id=272244,ilevel=321,enchant_id=8001",TH], "CH_Invader+TH":["chest=,id=193764,ilevel=321,enchant_id=7987",TH],
 "T1_Voracious":["trinket1=,id=270175,ilevel=334"], "T2_Voracious":["trinket2=,id=270175,ilevel=334"],
 "WP_Cane331":["main_hand=,id=245770,enchant_id=8689,bonus_id="+CB+"/13771,crafted_stats=32/36,crafting_quality=5,ilevel=331","off_hand="],
 "WP_Spiritcudgel334":["main_hand=,id=268210,ilevel=334,enchant_id=8689"],
 "TAL_oct7_2124":["talents=CYGADBD3hSPCL9Y9gz68WcKvMAAAAAAAAAAAAAAAAAWoMbNjxMD8AmlZmZmBDGjZWmZzMzYjlZWGjZGLYYAGbbzMYMLjATAAAAWMzMzMYzAjZAAMzADA"],
 "TAL_mplus_s2":["talents=CYGADBD3hSPCL9Y9gz68WcKvMAAAAAAAAAAAAAAAAAWAziZMmZAmlZmZmZhBjZZmlZWYmxGLzsMmZM2wwAM22mZwY2GADAAAALMzMzgNDjxAAwMDWGA"],
 "TAL_ra_s2":["talents=CYGADBD3hSPCL9Y9gz68WcKvMAAAAAAAAAAAAAAAAAWAzmZMmZgHwsMzMzMYwYMzyMbmZGbsMzyYMzYBDDwYbbmBjZZAMAAAAsYmZmZwmBGzAAYmBGA"],
 "TAL_s2_ra2":["talents=CYGADBD3hSPCL9Y9gz68WcKvMAAAAAAAAAAAAAAAAAWAzmZMmZgHwsMzMzMY8AGzyMLjlhZsZWmZZMzMshhBYA22GbYMzsMAAAAYjZmZGsZgxMAmZAgBA"],
 "TAL_blitz_st":["talents=CYGADBD3hSPCL9Y9gz68WcKvMAAAAAAAAAAAAAAAAAWAziZMmZAmtZmZmZzMgZZsMzyMmZMzyMLzMzgNMAYstYstNzmlZMzsMDAAAAbmZegxgNjZMGAmZwMDMA"],
 "TAL_blitz_aoe":["talents=CYGADBD3hSPCL9Y9gz68WcKvMAAAAAAAAAAAAAAAAAWAziZMmZAmtZmZmZzMgZZsMzyMmZMzyMmZmZYDDAGbLGbbzsZZGzMLzAAAAwmZmHYMYzYGjBgZGMzADA"],
}
for n, iid in (("Bubbleband",268266),("RitualBinder",159459),("Amani",273792),("Bloodmark",277897)):
    BAL[f"R1_{n}"] = [f"finger1=,id={iid},ilevel=321,enchant_id=7967,gem_id=240900"]
    BAL[f"R2_{n}"] = [f"finger2=,id={iid},ilevel=321,enchant_id=7967,gem_id=240907"]
L = ["name=A_current", "copy=Z_SANITY,A_current", "trinket2=,id=270164,bonus_id=42/13334/12854,ilevel=334"]
for n, l in BAL.items(): L += [f"copy={n},A_current"] + l
open("bal_variants.simc","w").write("\n".join(L)+"\n")
for fs, it in (("DungeonSlice",4000),("Patchwerk",6000)):
    open(f"run_bal_{fs}.simc","w").write(f"threads=4\niterations={it}\ndeterministic=1\nfight_style={fs}\ninput=../char_balance_2026-10-15.simc\ninput=bal_variants.simc\n")
# ---- consumables
FL = "flask_of_the_magisters_2 flask_of_the_shattered_sun_2 flask_of_the_blood_knights_2 flask_of_thalassian_resistance_2".split()
PO = "draught_of_rampant_abandon_2 lights_potential_2 potion_of_recklessness_2 liquid_luster_2 potion_of_zealotry_2".split()
FO = "harandar_celebration silvermoon_parade royal_roast impossibly_royal_roast twilight_anglers_medley loas_gathering amani_cornucopia".split()
def cons(base_flask):
    V = [("FL_"+f, ["flask="+f]) for f in FL if f != base_flask]
    V += [("PO_"+p, ["potion="+p]) for p in PO if p != "draught_of_rampant_abandon_2"]
    V += [("FO_"+f, ["food="+f]) for f in FO if f != "harandar_celebration"]
    V += [("OIL_oil_of_dawn_2", ["temporary_enchant=main_hand:oil_of_dawn_2"]), ("RUNE_none", ["augmentation=disabled"])]
    return V
BASECONS = lambda fl: [f"flask={fl}", "potion=draught_of_rampant_abandon_2", "food=harandar_celebration",
                       "augmentation=void_touched", "temporary_enchant=main_hand:thalassian_phoenix_oil_2"]
for tag, prof, setl, fl in (("bal","../char_balance_2026-10-15.simc",[], "flask_of_the_magisters_2"),
                            ("cat","../char_feral_2026-10-14.simc",CAT_SET,"flask_of_the_magisters_2")):
    L = ["name=A_current"] + setl + BASECONS(fl) + ["copy=Z_SANITY,A_current", "trinket2=,id=270164,bonus_id=42/13334/12854,ilevel=334"]
    for n, l in cons(fl): L += [f"copy={n},A_current"] + l
    open(f"cons_{tag}_variants.simc","w").write("\n".join(L)+"\n")
    for fs, it in (("DungeonSlice",4000),("Patchwerk",6000)):
        open(f"run_cons_{tag}_{fs}.simc","w").write(f"threads=4\niterations={it}\ndeterministic=1\nfight_style={fs}\ninput={prof}\ninput=cons_{tag}_variants.simc\n")
fl = "flask_of_thalassian_resistance_2"
for n, l in [("A_current", []), ("Z_SANITY", ["trinket2=,id=270165,bonus_id=6652/13334/12854,ilevel=334"])] + cons(fl):
    open(f"bear_runs/{n}.simc","w").write("threads=4\niterations=6000\ndeterministic=1\nfight_style=Patchwerk\ndesired_targets=1\n"
        "input=../../char_guardian_2026-10-14.simc\n" + "".join(x+"\n" for x in BEAR_SET + BASECONS(fl)) + f"name={n}\n" + "".join(x+"\n" for x in l))
print("ok")
