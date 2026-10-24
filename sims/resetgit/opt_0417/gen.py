#!/usr/bin/env python3
"""Resetgit BM 2026-10-24 04:17 export: enchants, gems, consumables (+ a gear check) with the user's current talents
in both modes (user: ignore talent changes). Profilesets. SimC midnight 3af1a75, data 12.1.5.70575 (client 70529).
Baseline FULL = worn gear at caps + the three empty slots filled: Indecipherable on Sentinel's Vitriolic Chain (socket
13668), Eyes of the Eagle + Flawless Deadly Amethyst on Vile Alchemist's Band (socket 13668), Agility & Stamina kit on
Cuisses of the Uncoiled Union. Every variant changes one thing against FULL."""
CUR = {
 "head": "head=,id=271492,bonus_id=13334/41/13696/13692/13698/12854,redirected_base_stats=268230,ilevel=334",
 "shoulder": "shoulder=,id=271490,bonus_id=6652/12838/13694/13697/1561,redirected_base_stats=272252,ilevel=308",
 "chest": "chest=,id=271495,bonus_id=6652/13690/13698/12846,redirected_base_stats=272247,ilevel=321",
 "legs": "legs=,id=268237,bonus_id=6652/13662/13334/12849,ilevel=334",
 "feet": "feet=,id=272248,bonus_id=6652/13662/12846,ilevel=321",
 "neck": "neck=,id=268250,bonus_id=6652/13668/13334/12849,ilevel=334",
 "finger1": "finger1=,id=272149,bonus_id=6652/13668/12846,ilevel=321",
 "finger2": "finger2=,id=268249,bonus_id=6652/13668/13334/12849,ilevel=334",
 "main_hand": "main_hand=,id=265337,bonus_id=12214/13667/12497/13751/14004/13771/8960/13836,crafted_stats=32/49,crafting_quality=5,ilevel=331",
}
FULL = [f"{CUR['neck']},gem_id=240983", f"{CUR['finger2']},enchant_id=7967,gem_id=240898", f"{CUR['legs']},enchant_id=8159"]
open("char_full.simc", "w").write(open("../char_bm_2026-10-24_0417.simc").read() + "\n# FULL: empty slots filled\n" + "\n".join(FULL) + "\n")
V = {"Z_SANITY": ["trinket2=,id=250228,bonus_id=13440/6652/12699/12846,ilevel=321"],
     "AS_WORN_no_gem_no_enchants": [CUR["neck"], CUR["finger2"], CUR["legs"]]}
E = {"shoulder": [(8001, "AmirdrassilsGrace"), (7971, "FlightOfTheEagle"), (7973, "AkilzonsSwiftness"), (7999, "NaturesGrace")],
     "legs": [(8163, "AgiArmorKit"), (8161, "AgiKit")],
     "head": [(7991, "EmpBlessingOfSpeed"), (7961, "EmpHexOfLeeching")],
     "chest": [(8013, "MarkOfTheMagister"), (7985, "MarkOfTheRootwarden"), (7957, "MarkOfNalorakk")],
     "feet": [(8019, "FarstridersHunt"), (7993, "ShaladrassilsRoots")],
     "main_hand": [(8609, "LacedZoomshots"), (8613, "SmugglersLynxeye"), (8615, "FarstridersHawkeye"), (7981, "JanalaisPrecision"),
                   (7983, "BerserkersRage"), (8007, "WorldsoulCradle"), (8037, "FlamesOfTheSindorei"), (8041, "ArcaneMastery")]}
for slot, opts in E.items():
    for eid, n in opts:
        extra = ",enchant_id=" + str(eid)
        V[f"EN_{slot[:2]}_{n}"] = [CUR[slot] + extra]
for eid, n in ((8025, "SilvermoonsAlacrity"), (7965, "AmaniMastery"), (7969, "ZuljinsMastery"), (8021, "ThalHaste"), (8023, "ThalVers"),
               (7995, "NaturesWrath"), (7997, "NaturesFury")):
    V[f"EN_rings_{n}"] = [f"{CUR['finger1']},enchant_id={eid},gem_id=240898", f"{CUR['finger2']},enchant_id={eid},gem_id=240898"]
for gid, n in ((240967, "Powerful"), (240971, "Stoic"), (240969, "Telluric")): V[f"GEM_neck_{n}"] = [f"{CUR['neck']},gem_id={gid}"]
GEMS = {240888: "QuickPeridot", 240890: "DeadlyPeridot", 240892: "MasterfulPeridot", 240894: "VersatilePeridot",
        240896: "MasterfulAmethyst", 240900: "QuickAmethyst", 240902: "VersatileAmethyst", 240904: "DeadlyGarnet",
        240906: "QuickGarnet", 240908: "MasterfulGarnet", 240910: "VersatileGarnet", 240912: "VersatileLapis",
        240914: "DeadlyLapis", 240916: "QuickLapis", 240918: "MasterfulLapis"}
for gid, n in GEMS.items():
    V[f"GEM_rings_{n}"] = [f"{CUR['finger1']},enchant_id=7967,gem_id={gid}", f"{CUR['finger2']},enchant_id=7967,gem_id={gid}"]
# consumables (names from SimC's own lists; base = potion_of_recklessness_2, flask_of_the_magisters_2, silvermoon_parade,
# void_touched rune, thalassian_phoenix_oil_2)
for f in ("flask_of_the_shattered_sun_2", "flask_of_the_blood_knights_2", "flask_of_thalassian_resistance_2"): V["FL_" + f] = ["flask=" + f]
for p in ("draught_of_rampant_abandon_2", "lights_potential_2", "liquid_luster_2", "potion_of_zealotry_2"): V["PO_" + p] = ["potion=" + p]
for f in ("harandar_celebration", "royal_roast", "impossibly_royal_roast", "twilight_anglers_medley", "loas_gathering", "amani_cornucopia"):
    V["FO_" + f] = ["food=" + f]
V["OIL_oil_of_dawn_2"] = ["temporary_enchant=main_hand:oil_of_dawn_2"]
V["OIL_none"] = ["temporary_enchant=disabled"]
V["RUNE_none"] = ["augmentation=disabled"]
# gear check vs FULL (bag alternatives at cap, enchanted/gemmed like the slot they replace)
CB = "12214/13667/12497/13751/14004/8960/13836"
V.update({
 "NE_Flowform321": ["neck=,id=171720,ilevel=321,gem_id=240983"],
 "R1_Sickening321_for_HexLoop": ["finger1=,id=252258,ilevel=321,enchant_id=7967,gem_id=240898"],
 "LE_GaleriderChausses308": ["legs=,id=272251,ilevel=308,enchant_id=8159"],
 "LE_CraftedFaulds331_CH": [f"legs=,id=244582,bonus_id={CB},crafted_stats=32/36,crafting_quality=5,ilevel=331,enchant_id=8159"],
 "WR_CraftedBracers331_HM": [f"wrist=,id=244584,bonus_id={CB},crafted_stats=36/49,crafting_quality=5,ilevel=331"],
 "WR_CraftedBracers331_CH": [f"wrist=,id=244584,bonus_id={CB},crafted_stats=32/36,crafting_quality=5,ilevel=331"],
 "MH_GebbosBackupBlaster334": ["main_hand=,id=268200,ilevel=334,enchant_id=8689"],
})
# user idea: catalyse Cuisses (Myth) into tier legs at 334, craft shoulders 331 (no embellishment: cap used by belt + bow)
TLEG = "legs=,id=271491,ilevel=334,enchant_id=8159"
V["SET_tierlegs334_only"] = [TLEG]
for k, st in (("CM", "32/49"), ("CH", "32/36"), ("HM", "36/49"), ("VM", "40/49"), ("HV", "36/40")):
    V[f"SET_tierlegs334+CraftShoulder331_{k}"] = [TLEG, f"shoulder=,id=244580,bonus_id={CB},crafted_stats={st},crafting_quality=5,ilevel=331,enchant_id=8001"]
for fs, it in (("Patchwerk", 5000), ("DungeonSlice", 2500)):
    L = ["threads=4", f"iterations={it}", "deterministic=1", f"fight_style={fs}", "input=char_full.simc"]
    for n, lines in V.items(): L += [f'profileset."{n}"+={l}' for l in lines]
    open(f"sweep_{fs}.simc", "w").write("\n".join(L) + "\n")
print(len(V))
