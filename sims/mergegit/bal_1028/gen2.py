#!/usr/bin/env python3
"""Balance, 2 Arcanoweaves allowed (user-confirmed). Legal 2-embellishment layouts, all 6 belt stat pairs:
  W = wrist Arcanoweave + belt Arcanoweave, Lantern recrafted without the stone
  C = belt Arcanoweave + Lantern Hunter's Ritual Stone, wrist without Arcanoweave
Baseline = current (wrist Arcanoweave + Lantern stone, Whirling Dervish Sash 321). Export 2026-10-21 17:19."""
exec(open("gen.py").read().split("V = {")[0])
P6 = {"CH": "32/36", "HM": "36/49", "CM": "32/49", "HV": "36/40", "CV": "32/40", "MV": "49/40"}
V = {"Z_SANITY": ["trinket2=,id=270164,bonus_id=42/13334/12854,ilevel=334"]}
for k, st in P6.items():
    V[f"W_belt_{k}+wrist_arc+lantern_plain"] = [belt(st), LANT_PLAIN]
    V[f"C_belt_{k}+lantern_stone+wrist_plain"] = [belt(st), WRIST_PLAIN]
for fs, it, tal in (("Patchwerk", 10000, TAL), ("DungeonSlice", 6000, MS2)):
    L = ["threads=4", f"iterations={it}", "deterministic=1", f"fight_style={fs}", "input=../char_balance_2026-10-21.simc", f"talents={tal}"]
    for n, lines in V.items(): L += [f'profileset."{n}"+={l}' for l in lines]
    open(f"w_{fs}.simc", "w").write("\n".join(L) + "\n")
