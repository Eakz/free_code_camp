#!/usr/bin/env python3
"""2026-10-21 stage 2: Balance owned-gear, enchant and gem sweep at cap (CLAUDE.md s3), per mode on that mode's best talents.

    python3 gen_gear.py <tag> <fight_style> <iterations> <talent_string>

SimC midnight 7bc1071, data 12.1.5.70448 (= client). Baseline = char_balance_2026-10-21.simc (export 2026-10-21 17:19)."""
import sys
tag, fs, it, tal = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
CB = "12214/13667/12497/13751/14004/8960/13836"
TH = "hands=,id=271529,ilevel=321"            # tier gauntlets (bags, Hero 12842 -> 321) keep 4pc when a tier slot moves
CUR = {  # worn lines without enchant/gem
 "head": "head=,id=271528,bonus_id=12846/13334/6652/13696/13692/13698/1574,redirected_base_stats=268219,ilevel=321",
 "neck": "neck=,id=268265,bonus_id=6652/13668/13334/13987/12854,ilevel=334",
 "shoulder": "shoulder=,id=271526,bonus_id=13334/13694/6652/13697/12846,ilevel=321",
 "chest": "chest=,id=271531,bonus_id=6652/13440/13690/13698/12846,redirected_base_stats=239048,ilevel=321",
 "legs": "legs=,id=271527,bonus_id=13334/13693/6652/13698/12846,ilevel=321",
 "feet": "feet=,id=268247,bonus_id=6652/13662/13334/13696/12854,ilevel=334",
 "finger1": "finger1=,id=158366,bonus_id=13440/6652/13668/12699/12846,ilevel=321",
 "finger2": "finger2=,id=252258,bonus_id=13440/40/13668/12699/12846,ilevel=321",
 "main_hand": "main_hand=,id=271092,bonus_id=6652/13334/12854,ilevel=334",
}
V = {}
# ---- owned items, every one at its track cap; enchant/gem copied from the slot it replaces
V.update({
 "HE_VeilFeralRite308+TH": ["head=,id=277888,ilevel=308,enchant_id=8017", TH],
 "NE_Yoke321": ["neck=,id=251173,ilevel=321,gem_id=240983/240900"],
 "NE_Graft321": ["neck=,id=251234,ilevel=321,gem_id=240983/240900"],
 "NE_Strand321": ["neck=,id=273781,ilevel=321,gem_id=240983/240900"],
 "NE_PendantMaleficFury321": ["neck=,id=251142,ilevel=321,gem_id=240983/240900"],
 "SH_Snakeskin321+TH": ["shoulder=,id=273774,ilevel=321,enchant_id=8001", TH],
 "SH_Miststalker321+TH": ["shoulder=,id=272244,ilevel=321,enchant_id=8001", TH],
 "SH_Feverflare321+TH": ["shoulder=,id=171692,bonus_id=8902/7756/13662/1699,ilevel=321,enchant_id=8001", TH],
 "BA_Pyrewalker321": ["back=,id=272225,ilevel=321"],
 "BA_Pledgebearer321": ["back=,id=272230,ilevel=321"],
 "BA_MiststalkerShroud321": ["back=,id=272226,ilevel=321"],
 "CH_Invader321+TH": ["chest=,id=193764,ilevel=321,enchant_id=7987", TH],
 "HA_TierGauntlets321": [TH],
 "HA_MiststalkerGrips321": ["hands=,id=272241,ilevel=321"],
 "HA_FeveredDefense321": ["hands=,id=251124,ilevel=321"],
 "WA_Cinch321": ["waist=,id=272245,ilevel=321"],
 "WA_Slitherscale308": ["waist=,id=271436,bonus_id=41/13696/13662/13333/10844/12838,crafted_stats=40/36,crafting_quality=5,ilevel=308"],
 "FE_MiststalkerStriders321": ["feet=,id=272240,ilevel=321,enchant_id=7963"],
 "T1_Voracious334": ["trinket1=,id=270175,ilevel=334"],
 "T2_Voracious334": ["trinket2=,id=270175,ilevel=334"],
 "T1_CrusadersKeepsake308": ["trinket1=,id=251792,ilevel=308"],
 "MH_Spiritcudgel334": ["main_hand=,id=268210,ilevel=334,enchant_id=8689"],
 "MH_BonedustPestle321": ["main_hand=,id=272270,ilevel=321,enchant_id=8689"],
 "ST_Cane331": [f"main_hand=,id=245770,enchant_id=8689,bonus_id={CB}/13771,crafted_stats=32/36,crafting_quality=5,ilevel=331", "off_hand="],
})
for n, iid, il in (("Bubbleband",268266,321),("RitualBinder",159459,321),("Amani",273792,321),("Bloodmark",277897,321),("Swarmcaller",281029,334)):
    V[f"R1_{n}{il}"] = [f"finger1=,id={iid},ilevel={il},enchant_id=7967,gem_id=240900"]
    V[f"R2_{n}{il}"] = [f"finger2=,id={iid},ilevel={il},enchant_id=7967,gem_id=240908"]
# ---- enchants on the worn piece
E = {
 "head": [(7991,"EmpBlessingOfSpeed"),(7961,"EmpHexOfLeeching")],
 "shoulder": [(7973,"AkilzonsSwiftness"),(7971,"FlightOfTheEagle"),(7999,"NaturesGrace")],
 "chest": [(8013,"MarkOfTheMagister"),(7985,"MarkOfTheRootwarden"),(7957,"MarkOfNalorakk")],
 "legs": [(7937,"IntMana"),(7939,"IntOnly")],
 "feet": [(8019,"FarstridersHunt"),(7993,"ShaladrassilsRoots")],
 "main_hand": [(7981,"JanalaisPrecision"),(7983,"BerserkersRage"),(8007,"WorldsoulCradle"),(8037,"FlamesOfTheSindorei"),(8039,"AcuityOfTheRendorei"),(8041,"ArcaneMastery")],
}
for slot, opts in E.items():
    for eid, n in opts: V[f"EN_{slot[:2]}_{n}"] = [f"{CUR[slot]},enchant_id={eid}"]
for eid, n in ((7965,"AmaniMastery"),(7969,"ZuljinsMastery"),(7995,"NaturesWrath"),(7997,"NaturesFury"),(8021,"ThalHaste"),(8023,"ThalVers"),(8025,"SilvermoonsAlacrity")):
    V[f"EN_rings_{n}"] = [f"{CUR['finger1']},gem_id=240900,enchant_id={eid}", f"{CUR['finger2']},gem_id=240907,enchant_id={eid}"]
# ---- gems: same Flawless (rank 2) in both rings + neck 2nd socket; neck diamond
GEMS = {240888:"QuickPeridot",240890:"DeadlyPeridot",240892:"MasterfulPeridot",240894:"VersatilePeridot",
        240896:"MasterfulAmethyst",240898:"DeadlyAmethyst",240900:"QuickAmethyst",240902:"VersatileAmethyst",
        240904:"DeadlyGarnet",240906:"QuickGarnet",240908:"MasterfulGarnet",240910:"VersatileGarnet",
        240912:"VersatileLapis",240914:"DeadlyLapis",240916:"QuickLapis",240918:"MasterfulLapis"}
for gid, n in GEMS.items():
    V[f"GEM_all_{n}"] = [f"{CUR['finger1']},enchant_id=7967,gem_id={gid}", f"{CUR['finger2']},enchant_id=7967,gem_id={gid}",
                         f"{CUR['neck']},gem_id=240983/{gid}"]
for gid, n in ((240967,"Powerful"),(240971,"Stoic"),(240969,"Telluric")):
    V[f"GEM_neckdia_{n}"] = [f"{CUR['neck']},gem_id={gid}/240900"]
L = [f"talents={tal}", "name=A_current", "copy=Z_SANITY,A_current", "trinket2=,id=270164,bonus_id=42/13334/12854,ilevel=334"]
for n, lines in V.items(): L += [f"copy={n},A_current"] + lines
open(f"gear_{tag}_variants.simc", "w").write("\n".join(L) + "\n")
open(f"run_gear_{tag}.simc", "w").write(f"threads=4\niterations={it}\ndeterministic=1\nfight_style={fs}\n"
    f"input=../char_balance_2026-10-21.simc\ninput=gear_{tag}_variants.simc\n")
print(tag, len(V), "variants")
