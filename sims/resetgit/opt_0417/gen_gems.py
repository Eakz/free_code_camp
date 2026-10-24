#!/usr/bin/env python3
"""Gems inside the final set (tier legs 334, crafted shoulders C/H + bracers C/H; raid also Sickening Signet).
Same Flawless (rank 2) gem in both rings; neck = Eversong Diamond choice. Baseline gems: Deadly Amethyst x2, Indecipherable."""
exec(open("gen_final.py").read().split("RAID_CONS =")[0])
SET = [TLEG, shoulder("32/36"), bracers("32/36")]
NECK = "neck=,id=268250,bonus_id=6652/13668/13334/12849,ilevel=334"
GEMS = {240888: "QuickPeridot", 240890: "DeadlyPeridot", 240892: "MasterfulPeridot", 240894: "VersatilePeridot",
        240896: "MasterfulAmethyst", 240898: "DeadlyAmethyst", 240900: "QuickAmethyst", 240902: "VersatileAmethyst",
        240904: "DeadlyGarnet", 240906: "QuickGarnet", 240908: "MasterfulGarnet", 240910: "VersatileGarnet",
        240912: "VersatileLapis", 240914: "DeadlyLapis", 240916: "QuickLapis", 240918: "MasterfulLapis"}
for fs, it, ring1 in (("Patchwerk", 6000, SICK), ("DungeonSlice", 3000, R1)):
    base = SET + ([f"{SICK},gem_id=240898"] if ring1 == SICK else [])
    L = ["threads=4", f"iterations={it}", "deterministic=1", f"fight_style={fs}", "input=char_full.simc"]
    L += [f'profileset."SET_DeadlyAmethyst_Indecipherable"+={l}' for l in base]
    for gid, n in GEMS.items():
        for l in SET + [f"{ring1},gem_id={gid}", f"{R2},gem_id={gid}"]: L.append(f'profileset."RING_{n}"+={l}')
    for gid, n in ((240967, "Powerful"), (240971, "Stoic"), (240969, "Telluric")):
        for l in base + [f"{NECK},gem_id={gid}"]: L.append(f'profileset."NECK_{n}"+={l}')
    open(f"gems_{fs}.simc", "w").write("\n".join(L) + "\n")
