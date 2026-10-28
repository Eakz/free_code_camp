#!/usr/bin/env python3
"""Follow-up 2026-10-28: Hunter's Ritual Stone can NOT go on a belt (Aln'hara weapons only). What is the Utility Belt worth with
Arcanoweave (bonus 12384, the only belt embellishment) or none, and what does the wrist Arcanoweave do for the bear?
Same provisional baseline, pull + boss, appended to runs_pull/runs_boss. SimC may or may not stack two Arcanoweave (checked in output)."""
import gen as g
ARC = "/12384"
WRIST = "wrist=,id=244576,bonus_id=12214/13667/12497/13751/14001/8960/12384/13836/13696,crafted_stats=40/32,crafting_quality=5,ilevel=331"
WRIST_PLAIN = WRIST.replace("/12384", "")
def belt(st, arc): return f"waist=,id=244573,bonus_id={g.CB}{ARC if arc else ''},crafted_stats={st},crafting_quality=5,ilevel=331"
V = {"E0_wrist_no_arcanoweave": [WRIST_PLAIN]}
for k in ("CV", "HV", "CH"):
    V[f"E1_belt_{k}_arc+wrist_arc"] = [belt(g.PAIRS[k], True)]
    V[f"E2_belt_{k}_arc_moved_from_wrist"] = [belt(g.PAIRS[k], True), WRIST_PLAIN]
for d, enemy, it in (("runs_pull", g.PULL, 5000), ("runs_boss", g.BOSS, 5000)):
    for n, lines in V.items():
        open(f"{d}/{n}.simc", "w").write(f"threads=4\niterations={it}\ndeterministic=1\nfight_style=Patchwerk\n{enemy}"
            f"input=../../char_guardian_2026-10-28.simc\ntalents={g.tal}\nname={n}\n" + "".join(l + "\n" for l in lines))
print(len(V))
