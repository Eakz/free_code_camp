#!/usr/bin/env python3
"""2026-10-22 Balance M+ sets (DungeonSlice). A_current = current talents; options on the 'm+ s2' loadout (+2.95% in
bal_1021 talent run). Shared F-sets use per-spec trinkets (see gen_f.py)."""
import re
exec(open("gen_f.py").read().split("L = [")[0])
TAL_MS2 = re.search(r"Saved Loadout: m\+ s2\n# talents=(\S+)", exp_b).group(1)
M = {
 "M1_talents_ms2": [],
 "M2_ms2+swarmcaller": [SW(7967, 240900)],
 "M3_ms2+swarm+mperidot+shroud": [SW(7967, 240892),
     "finger2=,id=252258,bonus_id=13440/40/13668/12699/12846,ilevel=321,enchant_id=7967,gem_id=240892",
     f"{NECK},gem_id=240983/240892", "back=,id=272226,ilevel=321"],
 "F1_swarm+binder_eagle_agikit": F["F1_swarm+binder_eagle_agikit"],
 "F3_bubble+binder_eagle_agikit": F["F3_bubble+binder_eagle_agikit"],
 "F4_bubble+binder_alacrity_agikit": F["F4_bubble+binder_alacrity_agikit"],
 "F5_swarm+sickening_eagle_intkit": F["F5_swarm+sickening_eagle_intkit"],
}
L = [f"talents={TAL_B}", "name=A_current", "copy=Z_SANITY,A_current", "trinket2=,id=270164,bonus_id=42/13334/12854,ilevel=334"]
for n, l in M.items(): L += [f"copy={n},A_current", f"talents={TAL_MS2}"] + l
open("m_variants.simc", "w").write("\n".join(L) + "\n")
open("run_m.simc", "w").write("threads=4\niterations=4000\ndeterministic=1\nfight_style=DungeonSlice\n"
    "input=../char_balance_2026-10-21.simc\ninput=m_variants.simc\n")
print(len(M))
