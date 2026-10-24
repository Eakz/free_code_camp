#!/usr/bin/env python3
"""2026-10-24 follow-up: Sentinel's Vitriolic Chain (Myth 318 -> 334, socket bonus 13668) vs Flowform Choker 321,
both with Indecipherable, inside the best M+ (M4) and raid (R4) sets. 340 = optional Venomstone (Myth 334 -> 340)."""
exec(open("gen_final.py").read().split("for fs, it, V in")[0])
FLOW = NECK
S334, S340 = SENT, "neck=,id=268250,ilevel=340,gem_id=240983"
def sw(lines, neck): return [l for l in lines if not l.startswith("neck=")] + [neck]
V = {"Patchwerk": {"R4_flowform": sw(RAID["R4_myth+craft_legs+wrist"], FLOW), "R4_sentinel334": sw(RAID["R4_myth+craft_legs+wrist"], S334),
                   "R4_sentinel340_venomstone": sw(RAID["R4_myth+craft_legs+wrist"], S340)},
     "DungeonSlice": {"M4_flowform": MPLUS["M4_vile+craftlegs+wrist"], "M4_sentinel334": sw(MPLUS["M4_vile+craftlegs+wrist"], S334),
                      "M4_sentinel340_venomstone": sw(MPLUS["M4_vile+craftlegs+wrist"], S340)}}
for fs, it in (("Patchwerk", 10000), ("DungeonSlice", 8000)):
    L = ["threads=4", f"iterations={it}", "deterministic=1", f"fight_style={fs}", "input=../char_bm_2026-10-24.simc"]
    for n, lines in V[fs].items(): L += [f'profileset."{n}"+={l}' for l in lines]
    open(f"neck_{fs}.simc", "w").write("\n".join(L) + "\n")
