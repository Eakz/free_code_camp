#!/usr/bin/env python3
"""Feral phase 2: weapon stat pairs (Pikestaff vs Blood Knight's Impetus) + M+ gear sweep (owned at cap vs murlok
top-50 Feral M+ projected items). Raid drops (Venomous Abyss) at Myth 6/6 334, dungeon 321, crafted 331 Q5."""
CB = "12214/13667/12497/13751/14004/8960/13836"
EMB = {"HRS":13771,"SigilHunt":12693,"Iris":13453}
def wep(iid, stats, emb):
    return f"main_hand=,id={iid},bonus_id={CB}/{EMB[emb]},crafted_stats={stats},crafting_quality=5,ilevel=331,enchant_id=7983"
TH = "hands=,id=271529,ilevel=321"
W = []
for e in ("HRS","SigilHunt","Iris"):
    for st, sn in (("49/32","MastCrit"),("36/40","HasteVers"),("32/40","CritVers"),("32/36","CritHaste")):
        W.append((f"W_Pike_{e}_{sn}", [wep(245771, st, e)]))
for e in ("HRS","SigilHunt"):
    for st, sn in (("49/32","MastCrit"),("36/40","HasteVers"),("32/40","CritVers")):
        W.append((f"W_Impetus_{e}_{sn}", [wep(237847, st, e)]))
G = [  # owned, at cap
 ("O_NE_Yoke", ["neck=,id=251173,ilevel=321,gem_id=240983"]),
 ("O_NE_Graft", ["neck=,id=251234,ilevel=321,gem_id=240983"]),
 ("O_BA_Pyrewalker", ["back=,id=272225,ilevel=321"]),
 ("O_SH_Miststalker+TH", ["shoulder=,id=272244,ilevel=321,enchant_id=8001", TH]),
 ("O_CH_Invader+TH", ["chest=,id=193764,ilevel=321,enchant_id=7987", TH]),
 ("O_HA_Subjugator", ["hands=,id=193758,ilevel=321"]),
 ("O_HA_TierGauntlets", [TH]),
 ("O_WA_Slitherscale308", ["waist=,id=271436,bonus_id=41/13696/13662/13333/10844/12838,crafted_stats=40/36,crafting_quality=5,ilevel=308"]),
 ("O_FE_Miststalker", ["feet=,id=272240,ilevel=321,enchant_id=7963"]),
 ("O_R1_Amani", ["finger1=,id=273792,ilevel=321,enchant_id=8025,gem_id=240916"]),
 ("O_R1_Sandstone", ["finger1=,id=158366,ilevel=321,enchant_id=8025,gem_id=240916"]),
 ("O_R1_Sickening", ["finger1=,id=252258,ilevel=321,enchant_id=8025,gem_id=240916"]),
 ("O_R2_Amani", ["finger2=,id=273792,ilevel=321,enchant_id=8025,gem_id=240916"]),
 ("O_T2_Gebbo", ["trinket2=,id=270164,ilevel=334"]),
 ("O_T2_VileVial", ["trinket2=,id=273796,ilevel=321"]),
 ("O_T2_Tumor", ["trinket2=,id=250245,ilevel=321"]),
 ("O_MH_TwinStrike", ["main_hand=,id=158370,ilevel=321,enchant_id=7983"]),
 # murlok projected (raid Myth 334; rings simmed without a gem: socket not verified)
 ("P_T2_ZuljinsGuillotine334", ["trinket2=,id=270173,ilevel=334"]),
 ("P_T1_ZuljinsGuillotine334", ["trinket1=,id=270173,ilevel=334"]),
 ("P_MH_Bardiche334", ["main_hand=,id=268215,ilevel=334,enchant_id=7983"]),
 ("P_R1_VileAlchemist334", ["finger1=,id=268249,ilevel=334,enchant_id=8025"]),
 ("P_R1_ApexBrute334", ["finger1=,id=268252,ilevel=334,enchant_id=8025"]),
 ("P_BA_SilkenVoodoo334", ["back=,id=268253,ilevel=334"]),
 ("P_BA_Bloodthorn321", ["back=,id=251190,ilevel=321"]),
 ("P_BA_AdherentShroud331_MastCrit", ["back=,id=239656,bonus_id=" + CB + ",crafted_stats=49/32,crafting_quality=5,ilevel=331"]),
 ("P_FE_AgentSneakers331_MastCrit", ["feet=,id=244569,bonus_id=" + CB + ",crafted_stats=49/32,crafting_quality=5,ilevel=331,enchant_id=7963"]),
]
for tag, V in (("w", W), ("g", G)):
    L = ["name=A_current", "copy=Z_SANITY,A_current", "trinket2=,id=270165,bonus_id=6652/13334/12854,ilevel=334"]
    for n, lines in V: L += [f"copy={n},A_current"] + lines
    open(f"{tag}_variants.simc", "w").write("\n".join(L) + "\n")
    for fs, it in (("Patchwerk", 6000), ("DungeonSlice", 4000)):
        open(f"run_{tag}_{fs}.simc", "w").write(f"threads=4\niterations={it}\ndeterministic=1\nfight_style={fs}\n"
            f"input=../char_feral_2026-10-14.simc\ninput={tag}_variants.simc\n")
print(len(W), len(G))
