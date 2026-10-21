#!/usr/bin/env python3
"""2026-10-21 stage 1: rank all 9 Balance loadouts from export 2026-10-21 17:19 on current (capped) gear."""
import re
T = {}
lines = open("../export_balance_2026-10-21_1719.txt").read().splitlines()
T["cur"] = next(l.split("=",1)[1] for l in lines if l.startswith("talents="))
for i, l in enumerate(lines):
    m = re.match(r"# Saved Loadout: (.+)", l)
    if m: T[re.sub(r"\W+","_",m.group(1)).strip("_")] = lines[i+1].split("talents=",1)[1]
L = ["name=A_current", "copy=Z_SANITY,A_current", "trinket2=,id=270164,bonus_id=42/13334/12854,ilevel=334"]
for n, t in T.items():
    if n != "cur": L += [f"copy=TAL_{n},A_current", f"talents={t}"]
open("tal_variants.simc","w").write("\n".join(L)+"\n")
for fs, it in (("DungeonSlice",6000),("Patchwerk",10000)):
    open(f"run_tal_{fs}.simc","w").write(f"threads=4\niterations={it}\ndeterministic=1\nfight_style={fs}\n"
        "input=../char_balance_2026-10-21.simc\ninput=tal_variants.simc\n")
print(list(T))
