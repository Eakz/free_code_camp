#!/usr/bin/env python3
"""2026-10-21: Guardian owned gear / enchants / gems at cap, single actor Patchwerk (CLAUDE.md s5).

    python3 gen_gear.py <talent_string> <targets>

Baseline char_guardian_2026-10-21.simc (export 17:31, the user's tank loadout, at cap). One file per variant in gruns/."""
import os, sys
tal, tg = sys.argv[1], int(sys.argv[2])
CB = "12214/13667/12497/13751/14004/8960/13836"
TH = "hands=,id=271529,ilevel=321"
CUR = {
 "head": "head=,id=271528,bonus_id=12846/13334/6652/13696/13692/13698/1574,redirected_base_stats=268219,ilevel=321",
 "neck": "neck=,id=268265,bonus_id=6652/13668/13334/13987/12854,ilevel=334",
 "shoulder": "shoulder=,id=271526,bonus_id=13334/13694/6652/13697/12846,ilevel=321",
 "chest": "chest=,id=271531,bonus_id=6652/13440/13690/13698/12846,redirected_base_stats=239048,ilevel=321",
 "legs": "legs=,id=271527,bonus_id=13334/13693/6652/13698/12846,ilevel=321",
 "feet": "feet=,id=268247,bonus_id=6652/13662/13334/13696/12854,ilevel=334",
 "finger1": "finger1=,id=268266,bonus_id=6652/13668/13334/12846,ilevel=321",
 "finger2": "finger2=,id=159459,bonus_id=13440/6652/13668/12699/12846,ilevel=321",
 "main_hand": "main_hand=,id=268215,bonus_id=6652/13334/13846/12854,ilevel=334",
}
V = {"A_base": [], "Z_SANITY": ["trinket2=,id=270165,bonus_id=6652/13334/12854,ilevel=334"]}
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
 "WA_WhirlingDervish321": ["waist=,id=159317,ilevel=321"],
 "WA_Slitherscale308": ["waist=,id=271436,bonus_id=41/13696/13662/13333/10844/12838,crafted_stats=40/36,crafting_quality=5,ilevel=308"],
 "FE_MiststalkerStriders321": ["feet=,id=272240,ilevel=321,enchant_id=7963"],
 "WP_Pikestaff331_MC": [f"main_hand=,id=245771,bonus_id={CB}/13771,crafted_stats=49/32,crafting_quality=5,ilevel=331,enchant_id=7983"],
})
for n, l in (("Voracious334","id=270175,ilevel=334"),("VileVial321","id=273796,ilevel=321"),("Tumor321","id=250245,ilevel=321"),
             ("Lightbearer308","id=280617,ilevel=308"),("Keepsake308","id=251792,ilevel=308")):
    V[f"T1_{n}"] = [f"trinket1=,{l}"]; V[f"T2_{n}"] = [f"trinket2=,{l}"]
for n, iid, il in (("Sandstone",158366,321),("Sickening",252258,321),("Amani",273792,321),("Bloodmark",277897,321),("Swarmcaller",281029,334)):
    V[f"R1_{n}{il}"] = [f"finger1=,id={iid},ilevel={il},enchant_id=8025,gem_id=240916"]
    V[f"R2_{n}{il}"] = [f"finger2=,id={iid},ilevel={il},enchant_id=8025,gem_id=240916"]
E = {
 "head": [(7991,"EmpBlessingOfSpeed"),(7961,"EmpHexOfLeeching")],
 "shoulder": [(7973,"AkilzonsSwiftness"),(7971,"FlightOfTheEagle"),(7999,"NaturesGrace")],
 "chest": [(8013,"MarkOfTheMagister"),(7985,"MarkOfTheRootwarden"),(7957,"MarkOfNalorakk")],
 "legs": [(8163,"AgiArmorKit"),(8161,"AgiKit")],
 "feet": [(8019,"FarstridersHunt"),(7993,"ShaladrassilsRoots")],
 "main_hand": [(7981,"JanalaisPrecision"),(8689,"RiteHashey"),(8007,"WorldsoulCradle"),(8037,"FlamesOfTheSindorei"),(8041,"ArcaneMastery")],
}
for slot, opts in E.items():
    for eid, n in opts: V[f"EN_{slot[:2]}_{n}"] = [f"{CUR[slot]},enchant_id={eid}"]
for eid, n in ((7965,"AmaniMastery"),(7969,"ZuljinsMastery"),(7995,"NaturesWrath"),(7997,"NaturesFury"),(8021,"ThalHaste"),(8023,"ThalVers"),(7967,"EyesOfTheEagle")):
    V[f"EN_rings_{n}"] = [f"{CUR['finger1']},gem_id=240916,enchant_id={eid}", f"{CUR['finger2']},gem_id=240916,enchant_id={eid}"]
GEMS = {240888:"QuickPeridot",240890:"DeadlyPeridot",240892:"MasterfulPeridot",240894:"VersatilePeridot",
        240896:"MasterfulAmethyst",240898:"DeadlyAmethyst",240900:"QuickAmethyst",240902:"VersatileAmethyst",
        240904:"DeadlyGarnet",240906:"QuickGarnet",240908:"MasterfulGarnet",240910:"VersatileGarnet",
        240912:"VersatileLapis",240914:"DeadlyLapis",240916:"QuickLapis",240918:"MasterfulLapis"}
for gid, n in GEMS.items():
    V[f"GEM_all_{n}"] = [f"{CUR['finger1']},enchant_id=8025,gem_id={gid}", f"{CUR['finger2']},enchant_id=8025,gem_id={gid}",
                         f"{CUR['neck']},gem_id=240983/{gid}"]
for gid, n in ((240967,"Powerful"),(240971,"Stoic"),(240969,"Telluric")):
    V[f"GEM_neckdia_{n}"] = [f"{CUR['neck']},gem_id={gid}/240900"]
os.makedirs("gruns", exist_ok=True)
for n, lines in V.items():
    open(f"gruns/{n}.simc", "w").write(f"threads=4\niterations=6000\ndeterministic=1\nfight_style=Patchwerk\ndesired_targets={tg}\n"
        f"input=../../char_guardian_2026-10-21.simc\ntalents={tal}\nname={n}\n" + "".join(l + "\n" for l in lines))
print(len(V), "variants")
