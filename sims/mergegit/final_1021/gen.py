#!/usr/bin/env python3
"""2026-10-22 combination runs (sets, not single swaps) for the Mergegit report.
Balance: copy= variants in one raid (Patchwerk, current talents). Bear: single actor, pull model (5 heroic dummies).
BOTH_* = one shared armour/jewellery/trinket set worn by both specs; only weapons differ (Balance Jan'thrazet+Lantern,
bear Bardiche). Exports: Balance 2026-10-21 17:19, Guardian 17:31. SimC midnight 7bc1071, data 12.1.5.70448."""
import re
exp_b = open("../export_balance_2026-10-21_1719.txt").read()
exp_g = open("../export_guardian_2026-10-21_1731.txt").read()
TAL_B = re.search(r"^talents=(\S+)", exp_b, re.M).group(1)
TAL_RIO = re.search(r"Saved Loadout: Raider.IO Build\n# talents=(\S+)", exp_b).group(1)
TAL_G = re.search(r"^talents=(\S+)", exp_g, re.M).group(1)
NECK = "neck=,id=268265,bonus_id=6652/13668/13334/13987/12854,ilevel=334"
SW = lambda e, g: f"finger1=,id=281029,ilevel=334,enchant_id={e},gem_id={g}"
RB = lambda e, g: f"finger2=,id=159459,bonus_id=13440/6652/13668/12699/12846,ilevel=321,enchant_id={e},gem_id={g}"
LEGS = lambda e: f"legs=,id=271527,bonus_id=6652/13440/13693/13698/12846,redirected_base_stats=159313,ilevel=321,enchant_id={e}"
CINCH = "waist=,id=272245,ilevel=321"
GEBBO1 = "trinket1=,id=270164,bonus_id=42/13334/12854,ilevel=334"
KEEP2 = "trinket2=,id=270165,bonus_id=6652/13334/12854,ilevel=334"
VIAL2 = "trinket2=,id=273796,ilevel=321"
def both(ring_ench, legs_ench, t2, gem=240916):
    return [CINCH, SW(ring_ench, gem), RB(ring_ench, gem), LEGS(legs_ench), f"{NECK},gem_id=240983/{gem}", GEBBO1, t2]
BOTH = {
 "BOTH_A_alacrity_agikit_keeper": both(8025, 8159, KEEP2),
 "BOTH_B_eagle_agikit_keeper": both(7967, 8159, KEEP2),
 "BOTH_C_alacrity_intkit_keeper": both(8025, 7935, KEEP2),
 "BOTH_D_alacrity_agikit_vial": both(8025, 8159, VIAL2),
 "BOTH_E_eagle_intkit_vial": both(7967, 7935, VIAL2),
}
# ---- Balance raid
BR = {
 "BR1_swarmcaller": [SW(7967, 240900)],
 "BR2_swarm+fevered+mperidot": [f"finger1=,id=281029,ilevel=334,enchant_id=7967,gem_id=240892",
     "finger2=,id=252258,bonus_id=13440/40/13668/12699/12846,ilevel=321,enchant_id=7967,gem_id=240892",
     f"{NECK},gem_id=240983/240892", "hands=,id=251124,ilevel=321"],
}
L = [f"talents={TAL_B}", "name=A_current", "copy=Z_SANITY,A_current", "trinket2=,id=270164,bonus_id=42/13334/12854,ilevel=334"]
for n, l in {**BR, **BOTH}.items(): L += [f"copy={n},A_current"] + l
L += ["copy=BR3_swarm+fevered+mperidot_RIO,BR2_swarm+fevered+mperidot", f"talents={TAL_RIO}"]
open("bal_raid_variants.simc", "w").write("\n".join(L) + "\n")
open("run_bal_raid.simc", "w").write("threads=4\niterations=6000\ndeterministic=1\nfight_style=Patchwerk\n"
    "input=../char_balance_2026-10-21.simc\ninput=bal_raid_variants.simc\n")
# ---- bear pull, single actor
ENEMY = "".join(f"tank_dummy=Mob{i}\ntank_dummy_type=heroic\n" for i in range(1, 6))
CB = "12214/13667/12497/13751/14004/8960/13836"
G = {"A_base": [], "Z_SANITY": [KEEP2],
     "G2_pikestaff": [f"main_hand=,id=245771,bonus_id={CB}/13771,crafted_stats=49/32,crafting_quality=5,ilevel=331,enchant_id=7983"],
     "G3_craftbelt_HV": [f"waist=,id=244573,bonus_id={CB}/13771,crafted_stats=36/40,crafting_quality=5,ilevel=331"],
     "G4_craftbelt_HV+swarm": [f"waist=,id=244573,bonus_id={CB}/13771,crafted_stats=36/40,crafting_quality=5,ilevel=331", SW(8025, 240916)],
     **BOTH}
for n, l in G.items():
    open(f"bear/{n}.simc", "w").write("threads=4\niterations=5000\ndeterministic=1\nfight_style=Patchwerk\n" + ENEMY +
        f"input=../../char_guardian_2026-10-21.simc\ntalents={TAL_G}\nname={n}\n" + "".join(x + "\n" for x in l))
print("ok", len(G))
