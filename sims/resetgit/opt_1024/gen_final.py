#!/usr/bin/env python3
"""Resetgit BM 2026-10-24 final sets (profilesets). Raid sets on the 'solos' loadout (+2.33% raid, -27% M+);
M+ sets on the current talents (best M+). Built from sweep_* winners."""
import re
exp = open("../export_bm_2026-10-24_0318.txt").read()
SOLOS = re.search(r"Saved Loadout: solos\n# talents=(\S+)", exp).group(1)
NECK = "neck=,id=171720,bonus_id=8902/7756/13668/12699/12846,ilevel=321,gem_id=240983"
KIT = "legs=,id=272251,bonus_id=6652/13662/12838,ilevel=308,enchant_id=8159"
CB = "12214/13667/12497/13751/14004/8960/13836"
CLEGS = f"legs=,id=244582,bonus_id={CB},crafted_stats=32/36,crafting_quality=5,ilevel=331,enchant_id=8159"
CWRIST_CH = f"wrist=,id=244584,bonus_id={CB},crafted_stats=32/36,crafting_quality=5,ilevel=331"
CWRIST_HM = f"wrist=,id=244584,bonus_id={CB},crafted_stats=36/49,crafting_quality=5,ilevel=331"
SENT = "neck=,id=268250,ilevel=334,gem_id=240983"
VILE = "finger1=,id=268249,ilevel=334,enchant_id=7967,gem_id=240898"
DP = ["finger1=,id=272149,bonus_id=6652/13668/12846,ilevel=321,enchant_id=7967,gem_id=240890",
      "finger2=,id=252258,bonus_id=13440/6652/13668/12699/12846,ilevel=321,enchant_id=7967,gem_id=240890"]
VILE_DP = "finger1=,id=268249,ilevel=334,enchant_id=7967,gem_id=240890"
YOKE = "neck=,id=251173,ilevel=321,gem_id=240983"
AMANI = "finger1=,id=273792,ilevel=321,enchant_id=7967,gem_id=240890"
T = f"talents={SOLOS}"
RAID = {
 "R0_solos": [T],
 "R1_free": [T, KIT, NECK] + DP,
 "R2_hero_yoke+amani": [T, KIT, YOKE, DP[1], AMANI],
 "R3_myth_sentinel+vile": [T, KIT, SENT, DP[1], VILE_DP],
 "R4_myth+craft_legs+wrist": [T, CLEGS, SENT, DP[1], VILE_DP, CWRIST_CH],
}
MPLUS = {
 "M1_free": [KIT, NECK],
 "M2_vile": [KIT, NECK, VILE],
 "M3_vile+craftlegs": [CLEGS, NECK, VILE],
 "M4_vile+craftlegs+wrist": [CLEGS, NECK, VILE, CWRIST_HM],
}
for fs, it, V in (("Patchwerk", 10000, RAID), ("DungeonSlice", 5000, MPLUS)):
    L = ["threads=4", f"iterations={it}", "deterministic=1", f"fight_style={fs}", "input=../char_bm_2026-10-24.simc",
         'profileset."Z_SANITY"+=trinket2=,id=250228,bonus_id=13440/6652/12699/12846,ilevel=321']
    for n, lines in V.items(): L += [f'profileset."{n}"+={l}' for l in lines]
    open(f"final_{fs}.simc", "w").write("\n".join(L) + "\n")
print("ok")
