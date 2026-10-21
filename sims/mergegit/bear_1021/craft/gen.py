#!/usr/bin/env python3
"""2026-10-21 user question: Band of the Swarmcaller (Myth 334, Silvermoon's Alacrity, Flawless Quick Lapis) instead of
Alluring Bubbleband, then next week craft belt / gloves / cloak 331 with an embellishment. Bear tank loadout (export 17:31),
pull model (5 heroic dummies, CLAUDE.md s5), 5000 it. Bardiche carries no embellishment, wrist = Arcanoweave, so the bear
can take one more. Hunter's Ritual Stone (13771) as on the Pikestaff/Lantern; Arcanoweave is already on the wrist."""
import os
tal = open("../../export_guardian_2026-10-21_1731.txt").read().split("\ntalents=")[1].split("\n")[0]
ENEMY = "".join(f"tank_dummy=Mob{i}\ntank_dummy_type=heroic\n" for i in range(1, 6))
CB = "12214/13667/12497/13751/14004/8960/13836"
SW = "finger1=,id=281029,ilevel=334,enchant_id=8025,gem_id=240916"
def cr(slot, iid, st, emb=True): return f"{slot}=,id={iid},bonus_id={CB}{'/13771' if emb else ''},crafted_stats={st},crafting_quality=5,ilevel=331"
ST = {"HV": "36/40", "CV": "32/40", "VM": "40/49", "HM": "36/49"}
V = {"A_base": [], "Z_SANITY": ["trinket2=,id=270165,bonus_id=6652/13334/12854,ilevel=334"], "SW": [SW]}
for k, st in ST.items():
    V[f"SW+Belt_{k}"] = [SW, cr("waist", 244573, st)]
    V[f"Belt_{k}"] = [cr("waist", 244573, st)]
for k in ("HV", "CV", "VM"):
    V[f"SW+Hands_{k}"] = [SW, cr("hands", 244575, st=ST[k])]
    V[f"SW+Cloak_{k}"] = [SW, cr("back", 239674, st=ST[k])]
V["SW+Belt_HV_noEmb"] = [SW, cr("waist", 244573, "36/40", emb=False)]
for n, lines in V.items():
    open(f"{n}.simc", "w").write("threads=4\niterations=5000\ndeterministic=1\nfight_style=Patchwerk\n" + ENEMY +
        f"input=../../char_guardian_2026-10-21.simc\ntalents={tal}\nname={n}\n" + "".join(l + "\n" for l in lines))
print(len(V))
