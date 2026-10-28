#!/usr/bin/env python3
"""Stage 2 (case 7, best combined set). Built from stage-1 winners. 'T' = attainable at 321 caps; 'H' = hypothetical 334 vendor
items (Miststalker's Grips / Pledgebearer's Pall at 334 are NOT verified to exist). Appends to runs_pull / runs_boss."""
import gen as g
B = lambda k: g.belt(g.PAIRS[k], True)
S = {
 "S_T1_CVbelt+mist321+pall321": [B("CV"), g.mist(321), g.cloak(272230, 321)],
 "S_T2_CVbelt+swarm+bubble": [B("CV"), g.SW("finger1"), g.BB("finger2")],
 "S_H1_CVbelt+mist334+pall334": [B("CV"), g.mist(334), g.cloak(272230, 334)],
 "S_H2_HVbelt+mist334+pall334": [B("HV"), g.mist(334), g.cloak(272230, 334)],
 "S_H3_CHbelt+mist334+pall334": [B("CH"), g.mist(334), g.cloak(272230, 334)],
 "S_H4_CVbelt+mist334+pall334+swarm+bubble": [B("CV"), g.mist(334), g.cloak(272230, 334), g.SW("finger1"), g.BB("finger2")],
 "S_H5_CVgloves+pall334": [g.gloves(g.PAIRS["CV"], True), g.cloak(272230, 334)],
}
for d, enemy, it in (("runs_pull", g.PULL, 5000), ("runs_boss", g.BOSS, 5000)):
    for n, lines in S.items():
        open(f"{d}/{n}.simc", "w").write(f"threads=4\niterations={it}\ndeterministic=1\nfight_style=Patchwerk\n{enemy}"
            f"input=../../char_guardian_2026-10-28.simc\ntalents={g.tal}\nname={n}\n" + "".join(l + "\n" for l in lines))
print(len(S))
