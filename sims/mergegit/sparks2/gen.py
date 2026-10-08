#!/usr/bin/env python3
"""2026-10-08 re-run on fresh SimC (midnight branch, live data 69933).
Verified today: armour craft = 2 Sparks of Tides, 2H = 4; 331 = Q5 + 80 Myth Mistcrest (3446; player has 83).
Player has 2 sparks -> exactly one armour craft. Embellishment cap 2: Balance uses 2 (wrist Arcanoweave + Lantern
Hunter's Ritual Stone); Guardian uses 1 (wrist), so a bear-only craft may carry Adorned Fang (13767, S2 LW)."""
import os
CB = "12214/13667/12497/13751/14001/8960/13836"
def cr(slot, iid, stats="36/40", extra="", emb=""):
    b = CB + (f"/{emb}" if emb else "")
    return f"{slot}=,id={iid},bonus_id={b},crafted_stats={stats},crafting_quality=5,ilevel=331{extra}"
TH = "hands=,id=271529,ilevel=321"
AF = "13767"
PIKE_RS = "main_hand=,id=245771,bonus_id=12214/13667/12497/13751/14004/13771/8960/13836,crafted_stats=36/40,crafting_quality=5,ilevel=331,enchant_id=7983"
def armour(legs_ench, emb=""):
    sfx = "+AF" if emb else ""
    return {
     f"CR_Belt{sfx}": [cr("waist", 244573, emb=emb)],
     f"CR_Hands{sfx}": [cr("hands", 244575, emb=emb)],
     f"CR_Feet{sfx}": [cr("feet", 244569, extra=",enchant_id=7963", emb=emb)],
     f"CR_Head+TierHands{sfx}": [cr("head", 244571, extra=",enchant_id=8017", emb=emb), TH],
     f"CR_Shoulder+TierHands{sfx}": [cr("shoulder", 244572, extra=",enchant_id=8001", emb=emb), TH],
     f"CR_Chest+TierHands{sfx}": [cr("chest", 244570, extra=",enchant_id=7987", emb=emb), TH],
     f"CR_Legs+TierHands{sfx}": [cr("legs", 244574, extra=f",enchant_id={legs_ench}", emb=emb), TH],
    }
G = {"A_current": [], "Z_SANITY": ["trinket2=,id=270164,bonus_id=42/13334/12854,ilevel=334"]}
G.update(armour(8159)); G.update(armour(8159, AF))
G.update({"REF4_Pikestaff+RitualStone": [PIKE_RS],
          "FREE_AmaniWarlord_ring1": ["finger1=,id=273792,ilevel=321,enchant_id=7967,gem_id=240907"]})
os.makedirs("g_runs", exist_ok=True)
for n, lines in G.items():
    open(f"g_runs/{n}.simc", "w").write("threads=4\niterations=8000\ndeterministic=1\nfight_style=Patchwerk\ndesired_targets=1\n"
        "input=../../char_guardian_2026-10-08.simc\n" + f"name={n}\n" + "".join(l + "\n" for l in lines))
B = armour(7935)
for st, n in (("32/49","CritMast"),("32/36","CritHaste"),("36/49","HasteMast"),("32/40","CritVers"),("49/40","MastVers")):
    B[f"CR_Hands_{n}"] = [cr("hands", 244575, stats=st)]
L = ["name=A_current", "copy=Z_SANITY,A_current", "trinket2=,id=270164,bonus_id=42/13334/12854,ilevel=334"]
for n, lines in B.items(): L += [f"copy={n},A_current"] + lines
open("b_variants.simc", "w").write("\n".join(L) + "\n")
for fs, it in (("Patchwerk", 8000), ("DungeonSlice", 5000)):
    open(f"run_b_{fs}.simc", "w").write(f"threads=4\niterations={it}\ndeterministic=1\nfight_style={fs}\ndesired_targets=1\n"
        "input=../char_2026-10-07_2124.simc\ninput=b_variants.simc\n")
print(len(G), "guardian runs,", len(B), "balance variants")
