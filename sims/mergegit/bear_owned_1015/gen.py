#!/usr/bin/env python3
"""Bear M+ build from owned gear WITH the crafted weapon (Aln'hara Pikestaff 331 Q5, Hunter's Ritual Stone).
Profile: Guardian 2026-10-14 23:01 (gear identical to Feral 23:43 export). Patchwerk single actor (CLAUDE.md s5)."""
import sys
CB = "12214/13667/12497/13751/14004/8960/13836"
def pike(st): return f"main_hand=,id=245771,bonus_id={CB}/13771,crafted_stats={st},crafting_quality=5,ilevel=331,enchant_id=7983"
BASEW = pike("32/40")   # Crit/Vers: best bear pair from the 2026-10-14 sweep
TH = "hands=,id=271529,ilevel=321"
V = {"A_base_PikeCV": [], "Z_SANITY": ["trinket2=,id=270165,bonus_id=6652/13334/12854,ilevel=334"],
     "W_PikeHV": [pike("36/40")], "W_PikeMC": [pike("49/32")]}
OWN = {
 "NE_Yoke": "neck=,id=251173,ilevel=321,gem_id=240983", "NE_Graft": "neck=,id=251234,ilevel=321,gem_id=240983",
 "NE_Strand": "neck=,id=273781,ilevel=321,gem_id=240983",
 "BA_Pyrewalker": "back=,id=272225,ilevel=321",
 "HA_Subjugator": "hands=,id=193758,ilevel=321", "HA_TierGauntlets": TH,
 "WA_Slitherscale308": "waist=,id=271436,bonus_id=41/13696/13662/13333/10844/12838,crafted_stats=40/36,crafting_quality=5,ilevel=308",
 "WA_MiststalkerCinch": "waist=,id=272245,ilevel=321",
 "FE_Miststalker": "feet=,id=272240,ilevel=321,enchant_id=7963",
 "WR_FuryFletched": "wrist=,id=251135,ilevel=321",
}
for k, l in OWN.items(): V[k] = [l]
V["SH_Miststalker+TH"] = ["shoulder=,id=272244,ilevel=321,enchant_id=8001", TH]
V["CH_Invader+TH"] = ["chest=,id=193764,ilevel=321,enchant_id=7987", TH]
for n, iid in (("Amani",273792),("Sandstone",158366),("Sickening",252258)):
    V[f"R1_{n}"] = [f"finger1=,id={iid},ilevel=321,enchant_id=8025,gem_id=240916"]
    V[f"R2_{n}"] = [f"finger2=,id={iid},ilevel=321,enchant_id=8025,gem_id=240916"]
for n, l in (("Gebbo","id=270164,ilevel=334"),("VileVial","id=273796,ilevel=321"),("Tumor","id=250245,ilevel=321")):
    V[f"T1_{n}"] = [f"trinket1=,{l}"]; V[f"T2_{n}"] = [f"trinket2=,{l}"]
for n, lines in V.items():
    open(f"runs/{n}.simc","w").write("threads=4\niterations=8000\ndeterministic=1\nfight_style=Patchwerk\ndesired_targets=1\n"
        "input=../../char_guardian_2026-10-14.simc\n" + BASEW + "\n" + f"name={n}\n" + "".join(x+"\n" for x in lines))
print(len(V))
