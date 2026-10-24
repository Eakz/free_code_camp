#!/usr/bin/env python3
"""Raid sets rebuilt after the split test: Sickening alone (+1.53) beats every consumable/gem/enchant mix
(Sickening and Blood Knights flask do not stack; Draught and Berserker's Rage lower it). Current consumables,
gems and weapon enchant kept."""
exec(open("gen_final.py").read().split("RAID_CONS =")[0])
S = f"{SICK},gem_id=240898"
GEBBO_RH = "main_hand=,id=268200,ilevel=334,enchant_id=8689"
RAID = {"R_A_Sickening": [S], "R_B_A+tierlegs+shoulderCH": [S, TLEG, shoulder("32/36")],
        "R_C_B+bracersCH": [S, TLEG, shoulder("32/36"), bracers("32/36")],
        "R_D_C+Gebbo+RitualStoneOnShoulder": [S, GEBBO_RH, TLEG, shoulder("32/36", True), bracers("32/36")],
        "R_C_HexLoop_kept": [TLEG, shoulder("32/36"), bracers("32/36")]}
L = ["threads=4", "iterations=10000", "deterministic=1", "fight_style=Patchwerk", "input=char_full.simc",
     'profileset."Z_SANITY"+=trinket2=,id=250228,bonus_id=13440/6652/12699/12846,ilevel=321']
for n, lines in RAID.items(): L += [f'profileset."{n}"+={l}' for l in lines]
open("final2_Patchwerk.simc", "w").write("\n".join(L) + "\n")
