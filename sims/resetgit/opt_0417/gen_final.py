#!/usr/bin/env python3
"""Resetgit 04:17 final sets vs FULL (current talents, both modes). PREV = the 03:18 plan applied to today's gear
(crafted Farstrider's Reinforced Faulds instead of Cuisses + crafted bracers). SH = user's idea: catalyse Cuisses into
tier legs (Myth 334) + craft Farstrider's Brilliant Plumes 331. D-sets move Hunter's Ritual Stone from the bow (Gebbo's
Backup Blaster replaces the Sprigshot) onto the crafted shoulders, so the embellishment count stays 2."""
CB = "12214/13667/12497/13751/14004/8960/13836"
R1 = "finger1=,id=272149,bonus_id=6652/13668/12846,ilevel=321,enchant_id=7967"
R2 = "finger2=,id=268249,bonus_id=6652/13668/13334/12849,ilevel=334,enchant_id=7967"
SICK = "finger1=,id=252258,bonus_id=13440/6652/13668/12699/12846,ilevel=321,enchant_id=7967"
def gems(g, ring1=R1): return [f"{ring1},gem_id={g}", f"{R2},gem_id={g}"]
FAULDS = f"legs=,id=244582,bonus_id={CB},crafted_stats=32/36,crafting_quality=5,ilevel=331,enchant_id=8159"
TLEG = "legs=,id=271491,ilevel=334,enchant_id=8159"
def shoulder(st, emb=False): return f"shoulder=,id=244580,bonus_id={CB}{'/13771' if emb else ''},crafted_stats={st},crafting_quality=5,ilevel=331,enchant_id=8001"
def bracers(st): return f"wrist=,id=244584,bonus_id={CB},crafted_stats={st},crafting_quality=5,ilevel=331"
BOW_BR = "main_hand=,id=265337,bonus_id=12214/13667/12497/13751/14004/13771/8960/13836,crafted_stats=32/49,crafting_quality=5,ilevel=331,enchant_id=7983"
GEBBO = "main_hand=,id=268200,ilevel=334,enchant_id=7983"
RAID_CONS = ["flask=flask_of_the_blood_knights_2", "potion=draught_of_rampant_abandon_2"]
RA = RAID_CONS + gems(240890, SICK) + [BOW_BR]
RAID = {
 "PREV_faulds+bracers+DeadlyPeridot": [FAULDS, bracers("32/36")] + gems(240890),
 "R_A_cons+Sickening+DeadlyPeridot+Berserker": RA,
 "R_B_A+tierlegs+shoulderCH": RA + [TLEG, shoulder("32/36")],
 "R_C_B+bracersCH": RA + [TLEG, shoulder("32/36"), bracers("32/36")],
 "R_D_C+Gebbo+RitualStoneOnShoulder": RAID_CONS + gems(240890, SICK) + [GEBBO, TLEG, shoulder("32/36", True), bracers("32/36")],
}
MA = gems(240888)
MPLUS = {
 "PREV_faulds+bracersHM": [FAULDS, bracers("36/49")],
 "M_A_QuickPeridot": MA,
 "M_B_A+tierlegs+shoulderHM": MA + [TLEG, shoulder("36/49")],
 "M_C_B+bracersHM": MA + [TLEG, shoulder("36/49"), bracers("36/49")],
 "M_D_C+Gebbo+RitualStoneOnShoulder": MA + [GEBBO, TLEG, shoulder("36/49", True), bracers("36/49")],
 "M_C_shoulderCH": MA + [TLEG, shoulder("32/36"), bracers("36/49")],
}
for fs, it, V in (("Patchwerk", 10000, RAID), ("DungeonSlice", 6000, MPLUS)):
    L = ["threads=4", f"iterations={it}", "deterministic=1", f"fight_style={fs}", "input=char_full.simc",
         'profileset."Z_SANITY"+=trinket2=,id=250228,bonus_id=13440/6652/12699/12846,ilevel=321']
    for n, lines in V.items(): L += [f'profileset."{n}"+={l}' for l in lines]
    open(f"final_{fs}.simc", "w").write("\n".join(L) + "\n")
