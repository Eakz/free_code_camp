#!/usr/bin/env python3
"""Same ring grid for Balance (profilesets). Common lines identical to the bear grid (Lunar 334 + Worldsoul, Miststalker's 334, Agi kit)."""
import sys; sys.path.insert(0, ".")
import gen_bal as gb, gen_rings as gr
V = {"Z_SANITY": ["trinket2=,id=270164,bonus_id=42/13334/12854,ilevel=334"], "RG_common_only": gr.COMMON}
for n, lines in gr.V.items():
    if n != "RG_base_common_only": V[n] = gr.COMMON + lines
for fs, it, tal, f in (("Patchwerk", 6000, gb.TAL, "ring_raid"), ("DungeonSlice", 3500, gb.LOADOUTS["m_s2"], "ring_mplus")):
    L = ["threads=4", f"iterations={it}", "deterministic=1", f"fight_style={fs}", "input=../char_balance_2026-10-29.simc", f"talents={tal}"]
    for n, lines in V.items(): L += [f'profileset."{n}"+={l}' for l in lines]
    open(f + ".simc", "w").write("\n".join(L) + "\n")
