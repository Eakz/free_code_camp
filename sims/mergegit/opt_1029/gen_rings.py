#!/usr/bin/env python3
"""Shared-set ring grid: all 15 ring pairs x 2 ring enchants (Alacrity 8025 / Eyes of the Eagle 7967), both specs.
Common lines for the grid (the 'shared' slots decided so far): Lunar Raiment 334 redirect 281236 + Worldsoul 7987, Miststalker's Grips 334,
Agility & Stamina leg kit 8159 on the tier leggings. Gem Flawless Quick Lapis in both rings. Bear = single actor pull (3000 it);
Balance = profilesets raid (equipped talents, 6000 it) and M+ ('m+ s2', 3500 it)."""
import itertools, re, os, sys
sys.path.insert(0, ".")
import gen_bear as gb
R = {"Bubble": ("268266", "6652/13668/13334/12846", 321), "RB": ("159459", "13440/6652/13668/12699/12846", 321),
     "Sandstone": ("158366", "13440/6652/13668/12699/12846", 321), "Amani": ("273792", "13440/6652/13668/12699/12846", 321),
     "Swarm": ("281029", "6652/13668/13334/12854", 334), "Sickening": ("252258", "13440/40/13668/12699/12846", 321)}
CHEST = "chest=,id=271531,bonus_id=13334/6652/14049/13690/13698/12854,redirected_base_stats=281236,ilevel=334,enchant_id=7987"
HANDS = "hands=,id=272241,bonus_id=13662/12854,ilevel=334"
LEGS = "legs=,id=271527,bonus_id=6652/13440/13693/13698/12846,redirected_base_stats=159313,ilevel=321,enchant_id=8159"
COMMON = [CHEST, HANDS, LEGS]
def ring(slot, n, e): iid, b, il = R[n]; return f"{slot}=,id={iid},bonus_id={b},ilevel={il},enchant_id={e},gem_id=240916"
V = {}
for (a, b), (en, e) in itertools.product(itertools.combinations(R, 2), (("Alac", 8025), ("Eyes", 7967))):
    V[f"RG_{a}+{b}_{en}"] = [ring("finger1", a, e), ring("finger2", b, e)]
V["RG_base_common_only"] = []
os.makedirs("runs_ring", exist_ok=True)
for n, lines in V.items():
    open(f"runs_ring/{n}.simc", "w").write(f"threads=4\niterations=3000\ndeterministic=1\nfight_style=Patchwerk\n{gb.PULL}"
        f"input=../../char_guardian_2026-10-29.simc\ntalents={gb.TAL}\nname={n}\n" + "".join(l + "\n" for l in COMMON + lines))
print(len(V))
