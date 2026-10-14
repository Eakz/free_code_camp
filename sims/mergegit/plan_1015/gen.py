#!/usr/bin/env python3
"""2026-10-15 plan: bear (priority) + feral M+ builds from owned gear with the crafted weapon, and projected BiS
incl. 12.1.5 Kith'ix raid items. Raid items at Myth 6/6 334; crafted 331; dungeon 321. Bear: Patchwerk single actor.
Feral: DungeonSlice (M+) + Patchwerk, one raid run."""
CB = "12214/13667/12497/13751/14004/8960/13836"
def pike(st): return f"main_hand=,id=245771,bonus_id={CB}/13771,crafted_stats={st},crafting_quality=5,ilevel=331,enchant_id=7983"
TH = "hands=,id=271529,ilevel=321"
CINCH = "waist=,id=272245,ilevel=321"; SUBJ = "hands=,id=193758,ilevel=321"
GEBBO2 = "trinket2=,id=270164,ilevel=334"; GEBBO1 = "trinket1=,id=270164,ilevel=334"
PROJ = {
 "P_CH_Chestwrap+TH": ["chest=,id=281236,ilevel=334,enchant_id=7987", TH],
 "P_HE_GazeCoiled+TH": ["head=,id=271875,ilevel=334,enchant_id=8017", TH],
 "P_WA_SashForlorn": ["waist=,id=268256,ilevel=334"],
 "P_R1_Swarmcaller": ["finger1=,id=281029,ilevel=334,enchant_id=8025"],
 "P_R2_Swarmcaller": ["finger2=,id=281029,ilevel=334,enchant_id=8025"],
 "P_R1_VileAlchemist": ["finger1=,id=268249,ilevel=334,enchant_id=8025"],
 "P_R1_ApexBrute": ["finger1=,id=268252,ilevel=334,enchant_id=8025"],
 "P_R1_MasterworkSindorei_CV": ["finger1=,id=240949,bonus_id=" + CB + ",crafted_stats=32/40,crafting_quality=5,ilevel=331,enchant_id=8025"],
 "P_T1_TwistedTendril": ["trinket1=,id=281215,ilevel=334"], "P_T2_TwistedTendril": ["trinket2=,id=281215,ilevel=334"],
 "P_T2_ZuljinsGuillotine": ["trinket2=,id=270173,ilevel=334"],
 "P_T2_FontVenomousRage": ["trinket2=,id=270168,ilevel=334"],
 "P_BA_SilkenVoodoo": ["back=,id=268253,ilevel=334"],
 "P_MH_Bardiche": ["main_hand=,id=268215,ilevel=334,enchant_id=7983"],
}
BEAR_EXTRA = {"P_T1_LightbearerShield": ["trinket1=,id=280617,ilevel=334"], "P_T2_LightbearerShield": ["trinket2=,id=280617,ilevel=334"]}
BEAR_COMBO = {
 "B1_Cinch+Subj": [CINCH, SUBJ],
 "B2_Cinch+Subj+GebboT2": [CINCH, SUBJ, GEBBO2],
 "B3_Cinch+Subj+GebboT1": [CINCH, SUBJ, GEBBO1],
 "B2_HV_weapon": [CINCH, SUBJ, GEBBO2, pike("36/40")],
}
def bear(n, lines):
    open(f"bear_runs/{n}.simc", "w").write("threads=4\niterations=8000\ndeterministic=1\nfight_style=Patchwerk\ndesired_targets=1\n"
        "input=../../char_guardian_2026-10-14.simc\n" + pike("32/40") + f"\nname={n}\n" + "".join(x + "\n" for x in lines))
bear("A_base_PikeCV", []); bear("Z_SANITY", ["trinket2=,id=270165,bonus_id=6652/13334/12854,ilevel=334"])
for d in (BEAR_COMBO, PROJ, BEAR_EXTRA):
    for n, l in d.items(): bear(n, l)
# feral
FERAL_OWN = ["finger1=,id=158366,ilevel=321,enchant_id=8025,gem_id=240916", "finger2=,id=273792,ilevel=321,enchant_id=8025,gem_id=240916", SUBJ, GEBBO2]
L = ["name=A_base_PikeCV", pike("32/40"), "copy=Z_SANITY,A_base_PikeCV", "trinket2=,id=270165,bonus_id=6652/13334/12854,ilevel=334",
     "copy=F1_owned_PikeCV,A_base_PikeCV"] + FERAL_OWN + ["copy=F2_owned_PikeHV,F1_owned_PikeCV", pike("36/40"),
     "copy=F3_owned+Cinch_PikeCV,F1_owned_PikeCV", CINCH]
for n, l in PROJ.items(): L += [f"copy={n},F1_owned_PikeCV"] + l
open("feral_variants.simc", "w").write("\n".join(L) + "\n")
for fs, it in (("DungeonSlice", 4000), ("Patchwerk", 6000)):
    open(f"run_feral_{fs}.simc", "w").write(f"threads=4\niterations={it}\ndeterministic=1\nfight_style={fs}\n"
        f"input=../char_feral_2026-10-14.simc\ninput=feral_variants.simc\n")
