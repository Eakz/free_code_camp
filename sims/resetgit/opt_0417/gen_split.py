#!/usr/bin/env python3
"""Decompose R_A (raid): which of Sickening / Blood Knights flask / Draught / Deadly Peridot / Berserker's Rage stack."""
exec(open("gen_final.py").read().split("RAID_CONS =")[0])
BK, DR = "flask=flask_of_the_blood_knights_2", "potion=draught_of_rampant_abandon_2"
V = {"S1_sickening": [f"{SICK},gem_id=240898"], "S2_BKflask": [BK], "S3_sick+BK": [f"{SICK},gem_id=240898", BK],
     "S4_sick+BK+draught": [f"{SICK},gem_id=240898", BK, DR], "S5_S4+DeadlyPeridot": [BK, DR] + gems(240890, SICK),
     "S6_S5+Berserker": [BK, DR, BOW_BR] + gems(240890, SICK), "S7_sick+draught+DP+Berserker_noBK": [DR, BOW_BR] + gems(240890, SICK),
     "S8_BK+draught+DP+Berserker_HexLoop": [BK, DR, BOW_BR] + gems(240890)}
L = ["threads=4", "iterations=10000", "deterministic=1", "fight_style=Patchwerk", "input=char_full.simc"]
for n, lines in V.items(): L += [f'profileset."{n}"+={l}' for l in lines]
open("split_Patchwerk.simc", "w").write("\n".join(L) + "\n")
