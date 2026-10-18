#!/usr/bin/env python3
"""Resetgit BM 2026-10-18: owned gear at cap, enchants, gems, talents. SimC 5537d88, data 12.1.5.70448 (= client).
Two runs: gear (owned items) and ench (enchants/gems/talents)."""
CUR = {  # equipped lines without enchant/gem, for enchant swaps
 "head":"head=,id=271492,bonus_id=13334/41/13696/13692/13698/12854,redirected_base_stats=268230,ilevel=334",
 "shoulder":"shoulder=,id=271490,bonus_id=6652/12838/13694/13697/1561,redirected_base_stats=272252,ilevel=308",
 "chest":"chest=,id=271495,bonus_id=6652/13690/13698/12846,redirected_base_stats=272247,ilevel=321",
 "legs":"legs=,id=272251,bonus_id=6652/13662/12838,ilevel=308",
 "feet":"feet=,id=272248,bonus_id=6652/13662/12846,ilevel=321",
 "main_hand":"main_hand=,id=265337,bonus_id=12214/13667/12497/13751/14004/13771/8960/13836,crafted_stats=32/49,crafting_quality=5,ilevel=331",
 "neck":"neck=,id=171720,bonus_id=8902/7756/13668/12699/12846,ilevel=321",
 "finger1":"finger1=,id=272149,bonus_id=6652/13668/12846,ilevel=321",
 "finger2":"finger2=,id=252258,bonus_id=13440/6652/13668/12699/12846,ilevel=321",
}
R1G, R2G = "gem_id=240898", "gem_id=240898"
E = {}
for eid, n in ((8001,"AmirdrassilsGrace"),(7971,"FlightOfTheEagle"),(7973,"AkilzonsSwiftness"),(7999,"NaturesGrace")):
    E[f"EN_sh_{n}"] = [f"{CUR['shoulder']},enchant_id={eid}"]
for eid, n in ((8159,"AgiStamKit"),(8163,"AgiArmorKit")): E[f"EN_le_{n}"] = [f"{CUR['legs']},enchant_id={eid}"]
for eid, n in ((7991,"EmpBlessingOfSpeed"),(7961,"EmpHexOfLeeching")): E[f"EN_he_{n}"] = [f"{CUR['head']},enchant_id={eid}"]
for eid, n in ((8013,"MarkOfTheMagister"),(7985,"MarkOfTheRootwarden"),(7957,"MarkOfNalorakk")): E[f"EN_ch_{n}"] = [f"{CUR['chest']},enchant_id={eid}"]
for eid, n in ((8019,"FarstridersHunt"),(7993,"ShaladrassilsRoots")): E[f"EN_fe_{n}"] = [f"{CUR['feet']},enchant_id={eid}"]
for eid, n in ((8609,"LacedZoomshots"),(8613,"SmugglersLynxeye"),(8615,"FarstridersHawkeye"),(7981,"JanalaisPrecision"),(7983,"BerserkersRage"),(8007,"WorldsoulCradle"),(8037,"FlamesOfTheSindorei"),(8041,"ArcaneMastery")):
    E[f"EN_wp_{n}"] = [f"{CUR['main_hand']},enchant_id={eid}"]
for eid, n in ((8025,"SilvermoonsAlacrity"),(7965,"AmaniMastery"),(7969,"ZuljinsMastery"),(8021,"ThalHaste"),(8023,"ThalVers"),(7995,"NaturesWrath"),(7997,"NaturesFury")):
    E[f"EN_rings_{n}"] = [f"{CUR['finger1']},enchant_id={eid},{R1G}", f"{CUR['finger2']},enchant_id={eid},{R2G}"]
for gid, n in ((240983,"Indecipherable"),(240971,"Stoic"),(240969,"Telluric")): E[f"GEM_neck_{n}"] = [f"{CUR['neck']},gem_id={gid}"]
for gid, n in ((240900,"QuickAmethyst"),(240902,"VersatileAmethyst"),(240904,"DeadlyGarnet"),(240906,"QuickGarnet"),(240908,"MasterfulGarnet"),
               (240910,"VersatileGarnet"),(240912,"VersatileLapis"),(240914,"DeadlyLapis"),(240916,"QuickLapis"),(240918,"MasterfulLapis")):
    E[f"GEM_rings_{n}"] = [f"{CUR['finger1']},enchant_id=7967,gem_id={gid}", f"{CUR['finger2']},enchant_id=7967,gem_id={gid}"]
for n, t in (("RaiderIO","C0PAD57yiELKEty14ekTDtZEqAMmxwCsAzwghNAAMDjZWmZYGzMmhZGjZGmZMjZYmZMjZwgZAAAAAzAAAwMzMDwMbADzCYbAYA"),
             ("delve","C0PAD57yiELKEty14ekTDtZEqAMmxwCsAzwghNAAMjHYmZWmZYmZmxMDmZMzwMzMjZYmZYMDGMDAAAAAAAAmZMDwMbAWmZBsNAM"),
             ("solos","C0PAD57yiELKEty14ekTDtZEqAMmxwCsAzwghNAAMjZMziZYGzMMegZGDzYmZGjZsYmxMzMGGmBAAAAMDAAAzwMDYmNYBzsAWGAG"),
             ("aa","C0PAD57yiELKEty14ekTDtZEqAMmxwCsBzwghNAAMjHYmZWmZYmZmxMDmZMzwMjZmZsNzMMmhlBzAAAAAAAAg5BGzMgZ2AwsA2GAG")):
    E[f"TAL_{n}"] = [f"talents={t}"]
G = {  # owned bag items at their track cap; enchant/gem copied from the slot they replace
 "HE_CrownEternalFang321": ["head=,id=268230,ilevel=321,enchant_id=8017"],
 "HE_VoidscarredCrown321": ["head=,id=251220,ilevel=321,enchant_id=8017"],
 "NE_Yoke321": ["neck=,id=251173,ilevel=321,gem_id=240967"],
 "BA_SilkenVoodoo321": ["back=,id=268253,ilevel=321"],
 "BA_MiststalkerShroud321": ["back=,id=272226,ilevel=321"],
 "HA_SeasonsTurn321": ["hands=,id=251152,ilevel=321"],
 "WA_GaleriderSkirt308": ["waist=,id=272253,ilevel=308"],
 "FE_FelsoakedSoles321": ["feet=,id=251125,ilevel=321,enchant_id=7963"],
 "R1_Amani321": ["finger1=,id=273792,ilevel=321,enchant_id=7967,gem_id=240898"],
 "R2_Amani321": ["finger2=,id=273792,ilevel=321,enchant_id=7967,gem_id=240898"],
 "R1_Lightwarden321": ["finger1=,id=251194,ilevel=321,enchant_id=7967,gem_id=240898"],
 "R2_Lightwarden321": ["finger2=,id=251194,ilevel=321,enchant_id=7967,gem_id=240898"],
 "MH_SnakebiteRecurve321": ["main_hand=,id=159637,ilevel=321,enchant_id=8689"],
 "MH_GebbosBackupBlaster334": ["main_hand=,id=268200,ilevel=334,enchant_id=8689"],
}
for n, l in (("DrumRenewedBonds321","id=248583,ilevel=321"),("SpiritRendingPoison321","id=274497,ilevel=321"),
             ("OphidianBoneWhistle321","id=274496,ilevel=321"),("KeepersSeethingCore295","id=270165,ilevel=295"),
             ("TatteredAmaniBanner321","id=273797,ilevel=321")):
    G[f"T1_{n}"] = [f"trinket1=,{l}"]; G[f"T2_{n}"] = [f"trinket2=,{l}"]
for tag, V in (("gear", G), ("ench", E)):
    L = ["name=A_current", "copy=Z_SANITY,A_current", "trinket2=,id=250228,bonus_id=13440/6652/12699/12846,ilevel=321"]
    for n, lines in V.items(): L += [f"copy={n},A_current"] + lines
    open(f"{tag}_variants.simc","w").write("\n".join(L)+"\n")
    for fs, it in (("DungeonSlice",4000),("Patchwerk",6000)):
        open(f"run_{tag}_{fs}.simc","w").write(f"threads=4\niterations={it}\ndeterministic=1\nfight_style={fs}\n"
            f"input=../char_bm_2026-10-18.simc\ninput={tag}_variants.simc\n")
print(len(G), len(E))
