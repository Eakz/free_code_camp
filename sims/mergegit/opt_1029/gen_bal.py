#!/usr/bin/env python3
"""Balance 2026-10-29 screen (profilesets). Baseline = worn set at caps (export 02:03). Raid = Patchwerk on the equipped talents;
M+ = DungeonSlice on 'm+ s2' (talent run also sweeps all 10 loadouts in both).
Embellishment legality: wrist Arcanoweave (12384) + Lantern Ritual Stone (13771) = 2, so the crafted Utility Belt (12384) can only be
worn by dropping the Lantern (no plain Lantern/off-hand exists in the bags). The belt variant below shows that case.

    python3 gen_bal.py   -> bal_raid.simc, bal_mplus.simc"""
import re
exp = open("../export_balance_2026-10-29_0203.txt").read()
TAL = re.search(r"^talents=(\S+)", exp, re.M).group(1)
LOADOUTS = {re.sub(r"\W+", "_", m.group(1)).strip("_"): m.group(2) for m in re.finditer(r"# Saved Loadout: (.+)\n# talents=(\S+)", exp)}
W = {  # worn, no enchant/gem
 "head": "head=,id=271528,bonus_id=12846/13334/6652/13696/13692/13698/1574,redirected_base_stats=268219,ilevel=321",
 "neck": "neck=,id=268265,bonus_id=6652/13668/13334/13987/12856,ilevel=341",
 "shoulder": "shoulder=,id=271526,bonus_id=13334/13694/6652/13697/12846,ilevel=321",
 "chest": "chest=,id=271531,bonus_id=13334/6652/14049/13690/13698/12854,redirected_base_stats=281236,ilevel=334",
 "legs": "legs=,id=271527,bonus_id=13334/13693/6652/13698/12846,ilevel=321",
 "feet": "feet=,id=268247,bonus_id=6652/13662/13334/13696/12854,ilevel=334",
 "finger1": "finger1=,id=281029,bonus_id=6652/13668/13334/12854,ilevel=334",
 "finger2": "finger2=,id=252258,bonus_id=13440/40/13668/12699/12846,ilevel=321",
 "main_hand": "main_hand=,id=271092,bonus_id=6652/13334/12856,ilevel=341",
}
V = {"Z_SANITY": ["trinket2=,id=270164,bonus_id=42/13334/12854,ilevel=334"]}
for n, t in LOADOUTS.items(): V[f"TAL_{n}"] = [f"talents={t}"]
# items
V["HA_Miststalker334"] = ["hands=,id=272241,bonus_id=13662/12854,ilevel=334"]
V["WA_Cinch321"] = ["waist=,id=272245,bonus_id=6652/13696/13662/12846,ilevel=321"]
CB = "12214/13667/12497/13751/14001/8960/12384/13836/13696"
for k, st in (("VM", "40/49"),):
    V["WA_UtilityBelt331_VM+noOffhand(wrist+belt Arc)"] = [f"waist=,id=244573,bonus_id={CB},crafted_stats={st},crafting_quality=5,ilevel=331", "off_hand="]
V["NE_Yoke321"] = ["neck=,id=251173,bonus_id=13440/6652/13668/12699/12846,ilevel=321,gem_id=240983/240900"]
V["CH_Lunar321_redirect239048"] = ["chest=,id=271531,bonus_id=6652/13440/13690/13698/12846,redirected_base_stats=239048,ilevel=321,enchant_id=7987"]
V["LE_MiststalkerCuisses321"] = ["legs=,id=272243,bonus_id=12841/42/13662,ilevel=321,enchant_id=7935"]
RINGS = {"RitualBinder321": ("159459", "13440/6652/13668/12699/12846", 321), "Bubbleband321": ("268266", "6652/13668/13334/12846", 321),
         "Sandstone321": ("158366", "13440/6652/13668/12699/12846", 321), "Amani321": ("273792", "13440/6652/13668/12699/12846", 321),
         "Swarmcaller334": ("281029", "6652/13668/13334/12854", 334), "Sickening321": ("252258", "13440/40/13668/12699/12846", 321)}
for n, (iid, b, il) in RINGS.items():
    for slot, worn in (("finger1", "Swarmcaller334"), ("finger2", "Sickening321")):
        if n in ("Swarmcaller334", "Sickening321"): continue   # both already worn
        V[f"R{slot[-1]}_{n}"] = [f"{slot}=,id={iid},bonus_id={b},ilevel={il},enchant_id=7967,gem_id=240892"]
TR = {"Voracious334": "id=270175,bonus_id=42/13334/12854,ilevel=334", "Keeper334": "id=270165,bonus_id=6652/13334/12854,ilevel=334",
      "Fang321": "id=270161,bonus_id=6652/13334/12843,ilevel=321", "Bellowstone321": "id=250228,bonus_id=12843/13440/40/12699,ilevel=321",
      "Keepsake308": "id=251792,bonus_id=12834/6652,ilevel=308", "Whistle308": "id=274496,bonus_id=12834/6652,ilevel=308"}
for n, l in TR.items(): V[f"T1_{n}"] = [f"trinket1=,{l}"]; V[f"T2_{n}"] = [f"trinket2=,{l}"]
# enchants
E = {"head": [(8017, "Rune_of_Avoidance_worn"), (7991, "EmpBlessingOfSpeed"), (7961, "EmpHexOfLeeching")],
     "shoulder": [(7973, "AkilzonsSwiftness"), (7971, "FlightOfTheEagle"), (7999, "NaturesGrace")],
     "chest": [(7987, "MarkOfTheWorldsoul"), (8013, "MarkOfTheMagister"), (7985, "MarkOfTheRootwarden"), (7957, "MarkOfNalorakk")],
     "legs": [(7935, "IntKit_worn"), (7937, "IntMana"), (7939, "IntOnly"), (8159, "AgiStamKit"), (8163, "AgiArmorKit")],
     "feet": [(8019, "FarstridersHunt"), (7993, "ShaladrassilsRoots")],
     "main_hand": [(8689, "RiteHashey"), (7981, "JanalaisPrecision"), (7983, "BerserkersRage"), (8007, "WorldsoulCradle"), (8037, "FlamesOfTheSindorei"), (8039, "AcuityOfTheRendorei"), (8041, "ArcaneMastery")]}
for slot, opts in E.items():
    for eid, n in opts: V[f"EN_{slot[:2]}_{n}"] = [W[slot] + f",enchant_id={eid}"]
for eid, n in ((7965, "AmaniMastery"), (7969, "ZuljinsMastery"), (7995, "NaturesWrath"), (7997, "NaturesFury"), (8021, "ThalHaste"), (8023, "ThalVers"), (8025, "SilvermoonsAlacrity")):
    V[f"EN_rings_{n}"] = [W["finger1"] + f",enchant_id={eid},gem_id=240892", W["finger2"] + f",enchant_id={eid},gem_id=240907"]
V["EN_rings_Eyes_worn_gemsame"] = [W["finger1"] + ",enchant_id=7967,gem_id=240892", W["finger2"] + ",enchant_id=7967,gem_id=240892"]
GEMS = {240888: "QuickPeridot", 240890: "DeadlyPeridot", 240892: "MasterfulPeridot", 240894: "VersatilePeridot", 240896: "MasterfulAmethyst",
        240898: "DeadlyAmethyst", 240900: "QuickAmethyst", 240902: "VersatileAmethyst", 240904: "DeadlyGarnet", 240906: "QuickGarnet", 240908: "MasterfulGarnet",
        240910: "VersatileGarnet", 240912: "VersatileLapis", 240914: "DeadlyLapis", 240916: "QuickLapis", 240918: "MasterfulLapis"}
for gid, n in GEMS.items():
    V[f"GEM_rings_{n}"] = [W["finger1"] + f",enchant_id=7967,gem_id={gid}", W["finger2"] + f",enchant_id=7967,gem_id={gid}"]
    V[f"GEM_neck2_{n}"] = [W["neck"] + f",gem_id=240983/{gid}"]
for gid, n in ((240967, "Powerful"), (240971, "Stoic"), (240969, "Telluric")): V[f"GEM_neck1_{n}"] = [W["neck"] + f",gem_id={gid}/240900"]
if __name__ == "__main__":
    for fs, it, tal, f in (("Patchwerk", 6000, TAL, "bal_raid"), ("DungeonSlice", 3500, LOADOUTS["m_s2"], "bal_mplus")):
        L = ["threads=4", f"iterations={it}", "deterministic=1", f"fight_style={fs}", "input=../char_balance_2026-10-29.simc", f"talents={tal}"]
        for n, lines in V.items(): L += [f'profileset."{n}"+={l}' for l in lines]
        open(f + ".simc", "w").write("\n".join(L) + "\n")
    print(len(V), "profilesets")
