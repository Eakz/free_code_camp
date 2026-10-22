#!/usr/bin/env python3
"""2026-10-22 shared-set round 2. BOTH_A-E showed trinkets cannot be shared (Keeper's is Agi/Str: Balance -5.7..-7%;
Vile Vial: bear +10..15% dmg taken). F-sets share armour, belt, rings, ring enchants, gems and the leg kit; trinkets and
weapons stay per spec (Balance Vile Vial+Gebbo / Jan'thrazet+Lantern, bear Gebbo+Keeper's / Bardiche)."""
import re
exec(open("gen.py").read().split("# ---- Balance raid")[0])
SICK = lambda e, g: f"finger2=,id=252258,bonus_id=13440/40/13668/12699/12846,ilevel=321,enchant_id={e},gem_id={g}"
BB = lambda e, g: f"finger1=,id=268266,bonus_id=6652/13668/13334/12846,ilevel=321,enchant_id={e},gem_id={g}"
def shared(r1, r2, e, legs, gem=240916):
    return [CINCH, r1(e, gem), r2(e, gem), LEGS(legs), f"{NECK},gem_id=240983/{gem}"]
F = {
 "F1_swarm+binder_eagle_agikit": shared(SW, RB, 7967, 8159),
 "F2_swarm+binder_eagle_intkit": shared(SW, RB, 7967, 7935),
 "F3_bubble+binder_eagle_agikit": shared(BB, RB, 7967, 8159),
 "F4_bubble+binder_alacrity_agikit": shared(BB, RB, 8025, 8159),
 "F5_swarm+sickening_eagle_intkit": shared(SW, SICK, 7967, 7935),
 "F6_swarm+binder_alacrity_agikit": shared(SW, RB, 8025, 8159),
}
L = [f"talents={TAL_B}", "name=A_current", "copy=Z_SANITY,A_current", "trinket2=,id=270164,bonus_id=42/13334/12854,ilevel=334"]
for n, l in F.items(): L += [f"copy={n},A_current"] + l
open("f_variants.simc", "w").write("\n".join(L) + "\n")
open("run_f_raid.simc", "w").write("threads=4\niterations=6000\ndeterministic=1\nfight_style=Patchwerk\n"
    "input=../char_balance_2026-10-21.simc\ninput=f_variants.simc\n")
ENEMY = "".join(f"tank_dummy=Mob{i}\ntank_dummy_type=heroic\n" for i in range(1, 6))
for n, l in F.items():
    open(f"bear/{n}.simc", "w").write("threads=4\niterations=5000\ndeterministic=1\nfight_style=Patchwerk\n" + ENEMY +
        f"input=../../char_guardian_2026-10-21.simc\ntalents={TAL_G}\nname={n}\n" + "".join(x + "\n" for x in l))
print(len(F))
