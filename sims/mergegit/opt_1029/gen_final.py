#!/usr/bin/env python3
"""Final sets, export 2026-10-29. G = Guardian optimum, B = Balance optimum, S = shared set (belt/trinkets/weapons per spec).
Each set is also simmed on the OTHER spec to price the sharing. Bear: single-actor pull + boss (8000 it) incl. max HP.
Balance: profilesets, raid on equipped talents (10000 it) / M+ on 'm+ s2' (6000 it) + the same sets on Raider.IO (raid) / ra s2 (M+) talents."""
import os, sys
sys.path.insert(0, ".")
import gen_bear as gb, gen_bal as gbal, gen_rings as gr
CHEST, HANDS, LEGS_AGI = gr.CHEST, gr.HANDS, gr.LEGS
def ring(slot, n, e, gem): iid, b, il = gr.R[n]; return f"{slot}=,id={iid},bonus_id={b},ilevel={il},enchant_id={e},gem_id={gem}"
LEGS_INT = "legs=,id=271527,bonus_id=13334/13693/6652/13698/12846,ilevel=321,enchant_id=7935"
CINCH = "waist=,id=272245,bonus_id=6652/13696/13662/12846,ilevel=321"
WHIRL = "waist=,id=159317,bonus_id=13440/6652/13696/13662/12699/12846,ilevel=321"
QL, MG = 240916, 240908
# ---- bear (worn: Bubble f1 + RB f2 Alacrity QL, Agi kit, Mist 334, crafted Arcanoweave belt)
BEAR = {
 "A_base": [], "Z_SANITY": ["trinket2=,id=270165,bonus_id=6652/13334/12854,ilevel=334"],
 "G_guardian_optimum": [CHEST],
 "S_shared": [CHEST, ring("finger1", "Amani", 8025, QL)],
 "S_shared_noBeltSwap(Cinch)": [CHEST, ring("finger1", "Amani", 8025, QL), CINCH],
 "B_balance_set_on_bear": [CHEST, LEGS_INT, WHIRL, ring("finger1", "Swarm", 7967, MG), ring("finger2", "Sandstone", 7967, MG)],
}
for d, enemy in (("runs_pull", gb.PULL), ("runs_boss", gb.BOSS)):
    os.makedirs(d, exist_ok=True)
    for n, lines in BEAR.items():
        open(f"{d}/F_{n}.simc", "w").write(f"threads=4\niterations=8000\ndeterministic=1\nfight_style=Patchwerk\n{enemy}"
            f"input=../../char_guardian_2026-10-29.simc\ntalents={gb.TAL}\nname=F_{n}\n" + "".join(l + "\n" for l in lines))
# ---- Balance (worn: Swarm f1 + Sickening f2 Eyes, Int kit, Subjugator's hands, Whirling belt, chest 334 no enchant)
BAL = {
 "Z_SANITY": ["trinket2=,id=270164,bonus_id=42/13334/12854,ilevel=334"],
 "B_balance_optimum": [CHEST, HANDS, ring("finger2", "Sandstone", 7967, MG)],
 "G_guardian_set_on_balance": [CHEST, HANDS, LEGS_AGI, ring("finger1", "Bubble", 8025, QL), ring("finger2", "RB", 8025, QL)],
 "S_shared": [CHEST, HANDS, LEGS_AGI, ring("finger1", "Amani", 8025, QL), ring("finger2", "RB", 8025, QL)],
 "S_shared_Eyes_variant": [CHEST, HANDS, LEGS_AGI, ring("finger1", "Amani", 7967, QL), ring("finger2", "RB", 7967, QL)],
}
TALS = {"raid": ("equipped", gbal.TAL, "Raider.IO", gbal.LOADOUTS["Raider_IO_Build"]), "mplus": ("m+ s2", gbal.LOADOUTS["m_s2"], "ra s2", gbal.LOADOUTS["ra_s2"])}
for mode, fs, it in (("raid", "Patchwerk", 10000), ("mplus", "DungeonSlice", 6000)):
    n0, t0, n1, t1 = TALS[mode]
    L = ["threads=4", f"iterations={it}", "deterministic=1", f"fight_style={fs}", "input=../char_balance_2026-10-29.simc", f"talents={t0}"]
    V = dict(BAL)
    V["WORN_alt_talents"] = [f"talents={t1}"]
    for k in ("B_balance_optimum", "S_shared"): V[f"{k}+alt_talents"] = BAL[k] + [f"talents={t1}"]
    for n, lines in V.items(): L += [f'profileset."{n}"+={l}' for l in lines]
    open(f"final_bal_{mode}.simc", "w").write("\n".join(L) + "\n")
print("ok")
