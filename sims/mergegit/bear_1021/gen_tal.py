#!/usr/bin/env python3
"""2026-10-21: rank Guardian loadouts (export 17:29). Single actor Patchwerk (CLAUDE.md s5), 1 and 5 targets.
Baseline char_guardian_2026-10-21.simc = export 17:31 (user tank loadout) at cap."""
import re
lines = open("../export_guardian_2026-10-21_1729.txt").read().splitlines()
T = {"cur": next(l.split("=",1)[1] for l in lines if l.startswith("talents="))}
for i, l in enumerate(lines):
    m = re.match(r"# Saved Loadout: (.+)", l)
    if m: T[re.sub(r"\W+","_",m.group(1)).strip("_")] = lines[i+1].split("talents=",1)[1]
for tg in (1, 5):
    for n, t in T.items():
        name = ("A_" if n == "cur" else "TAL_") + n
        open(f"runs/tal{tg}_{name}.simc","w").write(f"threads=4\niterations=8000\ndeterministic=1\nfight_style=Patchwerk\ndesired_targets={tg}\n"
            f"input=../../char_guardian_2026-10-21.simc\ntalents={t}\nname={name}\n")
    open(f"runs/tal{tg}_Z_SANITY.simc","w").write(f"threads=4\niterations=8000\ndeterministic=1\nfight_style=Patchwerk\ndesired_targets={tg}\n"
        f"input=../../char_guardian_2026-10-21.simc\nname=Z_SANITY\ntrinket2=,id=270165,bonus_id=6652/13334/12854,ilevel=334\n")
print(list(T))
