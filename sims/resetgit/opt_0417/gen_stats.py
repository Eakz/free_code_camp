#!/usr/bin/env python3
"""Crafted stat grid: Farstrider's Brilliant Plumes (shoulder) x Farstrider's Plated Bracers, all 6 secondary pairs each,
inside the planned set (tier legs 334 from catalysed Cuisses; raid also Sickening Signet). No embellishment on either."""
exec(open("gen_final.py").read().split("RAID_CONS =")[0])
P = {"CH": "32/36", "CM": "32/49", "CV": "32/40", "HM": "36/49", "HV": "36/40", "MV": "49/40"}
S = f"{SICK},gem_id=240898"
for fs, it, extra in (("Patchwerk", 6000, [S]), ("DungeonSlice", 3000, [])):
    L = ["threads=4", f"iterations={it}", "deterministic=1", f"fight_style={fs}", "input=char_full.simc"]
    for a, sa in P.items():
        for b, sb in P.items():
            for l in extra + [TLEG, shoulder(sa), bracers(sb)]: L.append(f'profileset."SH_{a}+BR_{b}"+={l}')
    open(f"stats_{fs}.simc", "w").write("\n".join(L) + "\n")
