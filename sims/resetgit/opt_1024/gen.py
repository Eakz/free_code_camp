#!/usr/bin/env python3
"""Resetgit BM 2026-10-24: talents, owned gear at cap, crafted options, enchants, gems -- one PROFILESET run per fight style.

    python3 gen.py            -> sweep_<fs>.simc for Patchwerk (raid) and DungeonSlice (M+)

SimC midnight 3af1a75, data 12.1.5.70575 (client 70529). Baseline = char_bm_2026-10-24.simc (build_profile.py, caps).
Profilesets sim each variant on its own (no shared raid), which is ~20x faster than copy= and keeps DungeonSlice honest.
Tier: head/shoulder/chest/hands are tier. A swap in one of those slots is also simmed with tier legs (catalysed
Galerider's Chausses -> Skulking Viper's Coiled Legwraps, Champion 308) so the 4-piece survives."""
import re
exp = open("../export_bm_2026-10-24_0318.txt").read()
CUR = {  # worn lines without enchant/gem
 "head": "head=,id=271492,bonus_id=13334/41/13696/13692/13698/12854,redirected_base_stats=268230,ilevel=334",
 "shoulder": "shoulder=,id=271490,bonus_id=6652/12838/13694/13697/1561,redirected_base_stats=272252,ilevel=308",
 "chest": "chest=,id=271495,bonus_id=6652/13690/13698/12846,redirected_base_stats=272247,ilevel=321",
 "legs": "legs=,id=272251,bonus_id=6652/13662/12838,ilevel=308",
 "feet": "feet=,id=272248,bonus_id=6652/13662/12846,ilevel=321",
 "neck": "neck=,id=171720,bonus_id=8902/7756/13668/12699/12846,ilevel=321",
 "finger1": "finger1=,id=272149,bonus_id=6652/13668/12846,ilevel=321",
 "finger2": "finger2=,id=252258,bonus_id=13440/6652/13668/12699/12846,ilevel=321",
 "main_hand": "main_hand=,id=265337,bonus_id=12214/13667/12497/13751/14004/13771/8960/13836,crafted_stats=32/49,crafting_quality=5,ilevel=331",
}
TL = "legs=,id=271491,ilevel=308,enchant_id=8161"     # catalysed tier legs (Champion 308)
CB = "12214/13667/12497/13751/14004/8960/13836"       # crafted base bonus ids (no embellishment: cap is 2, both used)
def cr(slot, iid, st, extra=""): return f"{slot}=,id={iid},bonus_id={CB},crafted_stats={st},crafting_quality=5,ilevel=331{extra}"
V = {"Z_SANITY": ["trinket2=,id=250228,bonus_id=13440/6652/12699/12846,ilevel=321"]}
# ---- talents
for m in re.finditer(r"# Saved Loadout: (.+)\n# talents=(\S+)", exp):
    V["TAL_" + re.sub(r"\W+", "_", m.group(1)).strip("_")] = [f"talents={m.group(2)}"]
# ---- owned gear at cap (enchant/gem copied from the replaced slot)
G = {
 "HE_CrownEternalFang321": ["head=,id=268230,ilevel=321,enchant_id=8017"],
 "HE_VoidscarredCrown321": ["head=,id=251220,ilevel=321,enchant_id=8017"],
 "NE_SentinelsVitriolic334": ["neck=,id=268250,ilevel=334,gem_id=240967"],
 "NE_Yoke321": ["neck=,id=251173,ilevel=321,gem_id=240967"],
 "SH_GaleriderMantle308": ["shoulder=,id=272252,ilevel=308"],
 "BA_SilkenVoodoo321": ["back=,id=268253,ilevel=321"],
 "BA_MiststalkerShroud321": ["back=,id=272226,ilevel=321"],
 "HA_SeasonsTurn321": ["hands=,id=251152,ilevel=321"],
 "WA_GaleriderSkirt321_noEmb": ["waist=,id=272253,ilevel=321"],
 "WA_ConsecratedTomb321_noEmb": ["waist=,id=159369,ilevel=321"],
 "FE_FelsoakedSoles321": ["feet=,id=251125,ilevel=321,enchant_id=7963"],
 "LE_TierLegs308": [TL],
 "MH_SnakebiteRecurve321": ["main_hand=,id=159637,ilevel=321,enchant_id=8689"],
 "MH_GebbosBackupBlaster334": ["main_hand=,id=268200,ilevel=334,enchant_id=8689"],
}
for n, iid, il in (("VileAlchemist", 268249, 334), ("Amani", 273792, 321), ("Lightwarden", 251194, 321)):
    G[f"R1_{n}{il}"] = [f"finger1=,id={iid},ilevel={il},enchant_id=7967,gem_id=240898"]
    G[f"R2_{n}{il}"] = [f"finger2=,id={iid},ilevel={il},enchant_id=7967,gem_id=240898"]
for n, l in (("Effigy308", "id=274493,ilevel=308"), ("SpiritRending321", "id=274497,ilevel=321"), ("OphidianWhistle321", "id=274496,ilevel=321"),
             ("DrumRenewedBonds321", "id=248583,ilevel=321"), ("TatteredBanner321", "id=273797,ilevel=321"), ("Wakrapuku321", "id=251784,ilevel=321"),
             ("KeepersCore295", "id=270165,ilevel=295"), ("Keepsake308", "id=251792,ilevel=308"), ("TinyElectromental321", "id=158374,ilevel=321")):
    G[f"T1_{n}"] = [f"trinket1=,{l}"]; G[f"T2_{n}"] = [f"trinket2=,{l}"]
for k in [k for k in G if k[:2] in ("HE", "HA")]:
    G[k + "+TL"] = G[k] + [TL]
# ---- crafted 331, no embellishment (waist Arcanoweave + Sprigshot Ritual Stone already = 2)
for k, st in (("CM", "32/49"), ("HM", "36/49"), ("CH", "32/36"), ("VM", "40/49")):
    G[f"CR_Legs331_{k}"] = [cr("legs", 244582, st, ",enchant_id=8161")]
    G[f"CR_Wrist331_{k}"] = [cr("wrist", 244584, st)]
G["CR_Shoulder331_CM+TL"] = [cr("shoulder", 244580, "32/49"), TL]
V.update(G)
# ---- enchants on the worn piece
E = {"shoulder": [(8001, "AmirdrassilsGrace"), (7971, "FlightOfTheEagle"), (7973, "AkilzonsSwiftness"), (7999, "NaturesGrace")],
     "legs": [(8159, "AgiStamKit"), (8163, "AgiArmorKit")],
     "head": [(7991, "EmpBlessingOfSpeed"), (7961, "EmpHexOfLeeching")],
     "chest": [(8013, "MarkOfTheMagister"), (7985, "MarkOfTheRootwarden"), (7957, "MarkOfNalorakk")],
     "feet": [(8019, "FarstridersHunt"), (7993, "ShaladrassilsRoots")],
     "main_hand": [(8609, "LacedZoomshots"), (8613, "SmugglersLynxeye"), (8615, "FarstridersHawkeye"), (7981, "JanalaisPrecision"),
                   (7983, "BerserkersRage"), (8007, "WorldsoulCradle"), (8037, "FlamesOfTheSindorei"), (8041, "ArcaneMastery")]}
for slot, opts in E.items():
    for eid, n in opts: V[f"EN_{slot[:2]}_{n}"] = [f"{CUR[slot]},enchant_id={eid}"]
for eid, n in ((8025, "SilvermoonsAlacrity"), (7965, "AmaniMastery"), (7969, "ZuljinsMastery"), (8021, "ThalHaste"), (8023, "ThalVers"),
               (7995, "NaturesWrath"), (7997, "NaturesFury")):
    V[f"EN_rings_{n}"] = [f"{CUR['finger1']},enchant_id={eid},gem_id=240898", f"{CUR['finger2']},enchant_id={eid},gem_id=240898"]
# ---- gems: neck diamond; same Flawless (rank 2) in both rings
for gid, n in ((240983, "Indecipherable"), (240971, "Stoic"), (240969, "Telluric")): V[f"GEM_neck_{n}"] = [f"{CUR['neck']},gem_id={gid}"]
GEMS = {240888: "QuickPeridot", 240890: "DeadlyPeridot", 240892: "MasterfulPeridot", 240894: "VersatilePeridot",
        240896: "MasterfulAmethyst", 240900: "QuickAmethyst", 240902: "VersatileAmethyst", 240904: "DeadlyGarnet",
        240906: "QuickGarnet", 240908: "MasterfulGarnet", 240910: "VersatileGarnet", 240912: "VersatileLapis",
        240914: "DeadlyLapis", 240916: "QuickLapis", 240918: "MasterfulLapis"}
for gid, n in GEMS.items():
    V[f"GEM_rings_{n}"] = [f"{CUR['finger1']},enchant_id=7967,gem_id={gid}", f"{CUR['finger2']},enchant_id=7967,gem_id={gid}"]
for fs, it in (("Patchwerk", 5000), ("DungeonSlice", 2000)):
    L = ["threads=4", f"iterations={it}", "deterministic=1", f"fight_style={fs}", "input=../char_bm_2026-10-24.simc"]
    for n, lines in V.items():
        L += [f'profileset."{n}"+={l}' for l in lines]
    open(f"sweep_{fs}.simc", "w").write("\n".join(L) + "\n")
print(len(V), "profilesets")
