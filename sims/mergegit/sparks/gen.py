#!/usr/bin/env python3
"""2 sparks: which crafts (331, q5, Haste/Vers per the user's assumption) help Guardian and Balance.
Armour is shared between specs; only the weapon differs. Balance already has 2 embellishments
(wrist Arcanoweave + Lantern Ritual Stone); Guardian has 1 (wrist), so a bear weapon may carry one."""
import os
CB = "12214/13667/12497/13751/14001/8960/13836"          # crafted armour, no embellishment, no stat setter
def cr(slot, iid, extra=""):
    return f"{slot}=,id={iid},bonus_id={CB},crafted_stats=36/40,crafting_quality=5,ilevel=331{extra}"
TH = "hands=,id=271529,ilevel=321"
PIKE_RS = "main_hand=,id=245771,bonus_id=12214/13667/12497/13751/14004/13771/8960/13836,crafted_stats=36/40,crafting_quality=5,ilevel=331,enchant_id=7983"
PIKE = "main_hand=,id=245771,bonus_id=12214/13667/12497/13751/14004/8960/13836,crafted_stats=36/40,crafting_quality=5,ilevel=331,enchant_id=7983"
def armour(legs_ench):
    return {
     "CR_Waist_UtilityBelt": [cr("waist", 244573)],
     "CR_Hands_Handwraps": [cr("hands", 244575)],
     "CR_Feet_Sneakers": [cr("feet", 244569, ",enchant_id=7963")],
     "CR_Legs+TierHands": [cr("legs", 244574, f",enchant_id={legs_ench}"), TH],
     "CR_Head+TierHands": [cr("head", 244571, ",enchant_id=8017"), TH],
     "CR_Shoulder+TierHands": [cr("shoulder", 244572, ",enchant_id=8001"), TH],
     "CR_Chest+TierHands": [cr("chest", 244570, ",enchant_id=7987"), TH],
     "CR2_Waist+Hands": [cr("waist", 244573), cr("hands", 244575)],
    }
# Guardian: one actor per run (CLAUDE.md s5)
G = {"A_current": [], "Z_SANITY": ["trinket2=,id=270164,bonus_id=42/13334/12854,ilevel=334"]}
G.update(armour(8159))
G.update({
 "CR_Pikestaff+RitualStone": [PIKE_RS],
 "CR_Pikestaff_noEmb": [PIKE],
 "CR2_Pikestaff+RitualStone+Waist": [PIKE_RS, cr("waist", 244573)],
 "CR2_Pikestaff+RitualStone+Hands": [PIKE_RS, cr("hands", 244575)],
 "OWN_AmaniWarlord_ring1": ["finger1=,id=273792,ilevel=321,enchant_id=7967,gem_id=240907"],
})
os.makedirs("g_runs", exist_ok=True)
for n, lines in G.items():
    open(f"g_runs/{n}.simc", "w").write("threads=4\niterations=8000\ndeterministic=1\nfight_style=Patchwerk\ndesired_targets=1\n"
        "input=../../char_guardian_2026-10-08.simc\n" + f"name={n}\n" + "".join(l + "\n" for l in lines))
# Balance: one raid run per fight style vs the 21:24 Balance profile
B = armour(7935)
L = ["name=A_current", "copy=Z_SANITY,A_current", "trinket2=,id=270164,bonus_id=42/13334/12854,ilevel=334"]
for n, lines in B.items(): L += [f"copy={n},A_current"] + lines
open("b_variants.simc", "w").write("\n".join(L) + "\n")
for fs, it in (("Patchwerk", 8000), ("DungeonSlice", 5000)):
    open(f"run_b_{fs}.simc", "w").write(f"threads=4\niterations={it}\ndeterministic=1\nfight_style={fs}\ndesired_targets=1\n"
        "input=../char_2026-10-07_2124.simc\ninput=b_variants.simc\n")
print(len(G), "guardian runs,", len(B), "balance variants")
