#!/usr/bin/env python3
"""2026-10-21: rank Guardian loadouts. Single actor Patchwerk (CLAUDE.md s5).
tal1 = M+ boss: default tank dummy (Mythic-raid strength), 1 target.
tal5 = M+ pull: 5 tank dummies of type heroic, ALL attacking. desired_targets=5 is wrong for tanks: only the first enemy
attacks, while Ursoc's Fury absorbs scale with damage dealt to all 5, so DTPS collapses to ~0 (tested 2026-10-21).
Baseline char_guardian_2026-10-21.simc = export 17:31 (user tank loadout) at cap."""
import re
lines = open("../export_guardian_2026-10-21_1729.txt").read().splitlines()
T = {"cur": next(l.split("=",1)[1] for l in lines if l.startswith("talents="))}
for i, l in enumerate(lines):
    m = re.match(r"# Saved Loadout: (.+)", l)
    if m: T[re.sub(r"\W+","_",m.group(1)).strip("_")] = lines[i+1].split("talents=",1)[1]
ENEMY = {1: "desired_targets=1\n", 5: "".join(f"tank_dummy=Mob{i}\ntank_dummy_type=heroic\n" for i in range(1, 6))}
for tg in (1, 5):
    for n, t in T.items():
        name = ("A_" if n == "cur" else "TAL_") + n
        open(f"runs/tal{tg}_{name}.simc","w").write(f"threads=4\niterations={8000 if tg==1 else 5000}\ndeterministic=1\nfight_style=Patchwerk\n{ENEMY[tg]}"
            f"input=../../char_guardian_2026-10-21.simc\ntalents={t}\nname={name}\n")
    open(f"runs/tal{tg}_Z_SANITY.simc","w").write(f"threads=4\niterations={8000 if tg==1 else 5000}\ndeterministic=1\nfight_style=Patchwerk\n{ENEMY[tg]}"
        f"input=../../char_guardian_2026-10-21.simc\nname=Z_SANITY\ntrinket2=,id=270165,bonus_id=6652/13334/12854,ilevel=334\n")
print(list(T))
