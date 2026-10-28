#!/usr/bin/env python3
"""2026-10-28 follow-up for Balance: what is Hunter's Ritual Stone on the Aln'hara Lantern worth, and what if the 2nd embellishment
slot goes to a crafted belt with Arcanoweave (wrist keeps Arcanoweave, Lantern recrafted without the stone)?
Balance export 2026-10-21 17:19 (gear not refreshed). Profilesets: raid = current talents Patchwerk; M+ = 'm+ s2' DungeonSlice.
Caveat: SimC allows two Arcanoweave; the game rule is unverified."""
import re
exp = open("../export_balance_2026-10-21_1719.txt").read()
TAL = re.search(r"^talents=(\S+)", exp, re.M).group(1)
MS2 = re.search(r"Saved Loadout: m\+ s2\n# talents=(\S+)", exp).group(1)
CB = "12214/13667/12497/13751/14004/8960/13836"
LANTERN = "off_hand=,id=245769,bonus_id=12214/13667/12497/13751/14001/13771/8960/13836,crafted_stats=49/36,crafting_quality=5,ilevel=331"
LANT_PLAIN = LANTERN.replace("/13771", "")
WRIST_PLAIN = "wrist=,id=244576,bonus_id=12214/13667/12497/13751/14001/8960/13836/13696,crafted_stats=40/32,crafting_quality=5,ilevel=331"
def belt(st): return f"waist=,id=244573,bonus_id={CB}/12384,crafted_stats={st},crafting_quality=5,ilevel=331"
P = {"CH": "32/36", "HM": "36/49", "CM": "32/49", "HV": "36/40"}
V = {"Z_SANITY": ["trinket2=,id=270164,bonus_id=42/13334/12854,ilevel=334"],
     "L1_lantern_no_stone": [LANT_PLAIN],
     "L0_wrist_no_arcanoweave": [WRIST_PLAIN],
     "L2_lantern_no_stone+wrist_no_arc": [LANT_PLAIN, WRIST_PLAIN]}
for k, st in P.items(): V[f"B_belt_{k}_arc+wrist_arc+lantern_no_stone"] = [belt(st), LANT_PLAIN]
for k, st in P.items(): V[f"B3_belt_{k}_arc+wrist_arc+lantern_STONE(3 emb, illegal)"] = [belt(st)]
for fs, it, tal in (("Patchwerk", 8000, TAL), ("DungeonSlice", 5000, MS2)):
    L = ["threads=4", f"iterations={it}", "deterministic=1", f"fight_style={fs}", "input=../char_balance_2026-10-21.simc", f"talents={tal}"]
    for n, lines in V.items(): L += [f'profileset."{n}"+={l}' for l in lines]
    open(f"{fs}.simc", "w").write("\n".join(L) + "\n")
