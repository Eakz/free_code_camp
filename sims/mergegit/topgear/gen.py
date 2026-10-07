#!/usr/bin/env python3
"""Top Gear phase 1 (owned items at cap, enchants, talents) vs the 2026-10-07 21:24 profile."""
TH = "hands=,id=271529,ilevel=321"   # tier gauntlets from bags -> keeps 4pc when a tier slot is swapped
T = {
 'mplus_s2': "CYGADBD3hSPCL9Y9gz68WcKvMAAAAAAAAAAAAAAAAAWAzmZMmZAmlZmZmZhBjZZmlZWYmxGLzsMmZM2wwAM22mZwY2GADAAAALMzMzgNDjxAAwMDWGA",
 'ra_s2':    "CYGADBD3hSPCL9Y9gz68WcKvMAAAAAAAAAAAAAAAAAWAzmZMmZgHwsMzMzMYwYMzyMbmZGbsMzyYMzYBDDwYbbmBjZZAMAAAAsYmZmZwmBGzAAYmBGA",
 'blitz_st': "CYGADBD3hSPCL9Y9gz68WcKvMAAAAAAAAAAAAAAAAAWAziZMmZAmtZmZmZzMgZZsMzyMmZMzyMLzMzgNMAYstYstNzmlZMzsMDAAAAbmZegxgNjZMGAmZwMDMA",
 'blitz_aoe':"CYGADBD3hSPCL9Y9gz68WcKvMAAAAAAAAAAAAAAAAAWAziZMmZAmtZmZmZzMgZZsMzyMmZMzyMmZmZYDDAGbLGbbzsZZGzMLzAAAAwmZmHYMYzYGjBgZGMzADA",
 'prev_active':"CYGADBD3hSPCL9Y9gz68WcKvMAAAAAAAAAAAAAAAAAWoMLNjxMDwsNzMzMbmBMLjlZWmxMjZWmZZmZGshBAjtFjttZ2sMTzMLzEAAAgNzMPwYwmxMGDAzMYmBGA",
}
V = []
for k, s in T.items(): V.append((f"TAL_{k}", [f"talents={s}"]))
# gear (CLAUDE.md s3: candidates at cap, enchant/gem copied)
G = [
 ("NE_GraftOfTheDomanaar", ["neck=,id=251234,ilevel=321,gem_id=240983"]),
 ("BA_PyrewalkersMantle", ["back=,id=272225,ilevel=321"]),
 ("SH_MiststalkersSpaulders+TierHands", ["shoulder=,id=272244,ilevel=321,enchant_id=8001", TH]),
 ("CH_InvadersFirestorm+TierHands", ["chest=,id=193764,ilevel=321,enchant_id=7987", TH]),
 ("WR_FuryFletchedArmlets", ["wrist=,id=251135,ilevel=321"]),
 ("HA_TierGauntlets", [TH]),
 ("WA_MiststalkersCinch", ["waist=,id=272245,ilevel=321"]),
 ("WA_SlitherscaleGirdle", ["waist=,id=271436,ilevel=321,crafted_stats=40/36,crafting_quality=5"]),
 ("FE_MiststalkersStriders", ["feet=,id=272240,ilevel=321,enchant_id=7963"]),
 ("MH_MalevolentSpiritcudgel334", ["main_hand=,id=268210,ilevel=334,enchant_id=8689"]),
 ("ST_AlnharaCane331", ["main_hand=,id=245770,enchant_id=8689,bonus_id=12214/13667/12497/13751/14004/13771/8960/13836,crafted_stats=32/36,crafting_quality=5,ilevel=331", "off_hand="]),
]
for n, iid in (("RitualBindersRing",159459),("BandOfTheAmaniWarlord",273792),("AlluringBubbleband",268266)):
    G.append((f"1R_{n}", [f"finger1=,id={iid},ilevel=321,enchant_id=7967,gem_id=240900"]))
    G.append((f"2R_{n}", [f"finger2=,id={iid},ilevel=321,enchant_id=7967,gem_id=240907"]))
V += G
# enchants: replace current Tier2 enchant on the worn piece
CUR = {
 'head': "head=,id=271528,bonus_id=12846/13334/6652/13696/13692/13698/1574,redirected_base_stats=268219,ilevel=321",
 'shoulder': "shoulder=,id=271526,bonus_id=13334/13694/6652/13697/12846,ilevel=321",
 'chest': "chest=,id=271531,bonus_id=6652/13440/13690/13698/12846,redirected_base_stats=239048,ilevel=321",
 'legs': "legs=,id=271527,bonus_id=13334/13693/6652/13698/12846,ilevel=321",
 'feet': "feet=,id=268247,bonus_id=6652/13662/13334/13696/12854,ilevel=334",
 'main_hand': "main_hand=,id=271092,bonus_id=6652/13334/12854,ilevel=334",
}
E = {
 'head': [(7991,"EmpBlessingOfSpeed"),(7961,"EmpHexOfLeeching")],
 'shoulder': [(7973,"AkilzonsSwiftness"),(7971,"FlightOfTheEagle"),(7999,"NaturesGrace")],
 'chest': [(8013,"MarkOfTheMagister"),(7985,"MarkOfTheRootwarden"),(7957,"MarkOfNalorakk")],
 'legs': [(7937,"IntMana"),(7939,"IntOnly")],
 'feet': [(8019,"FarstridersHunt"),(7993,"ShaladrassilsRoots")],
 'main_hand': [(7981,"JanalaisPrecision"),(7983,"BerserkersRage"),(8007,"WorldsoulCradle"),(8037,"FlamesOfTheSindorei"),(8039,"AcuityOfTheRendorei"),(8041,"ArcaneMastery")],
}
for slot, opts in E.items():
    for eid, n in opts:
        V.append((f"EN_{slot[:2]}_{n}", [f"{CUR[slot]},enchant_id={eid}"]))
R1 = "finger1=,id=158366,bonus_id=13440/6652/13668/12699/12846,ilevel=321,gem_id=240900,enchant_id="
R2 = "finger2=,id=252258,bonus_id=13440/40/13668/12699/12846,ilevel=321,gem_id=240907,enchant_id="
for eid, n in ((7965,"AmaniMastery"),(7969,"ZuljinsMastery"),(7995,"NaturesWrath"),(7997,"NaturesFury"),(8021,"ThalHaste"),(8023,"ThalVers"),(8025,"SilvermoonsAlacrity")):
    V.append((f"EN_rings_{n}", [f"{R1}{eid}", f"{R2}{eid}"]))
L = ["name=A_current", "copy=Z_SANITY,A_current", "trinket2=,id=270164,bonus_id=42/13334/12854,ilevel=334"]
for n, lines in V: L += [f"copy={n},A_current"] + lines
open("p1_variants.simc", "w").write("\n".join(L) + "\n")
for fs, it in (("Patchwerk", 4000), ("DungeonSlice", 3000)):
    open(f"run_p1_{fs}.simc", "w").write(f"threads=4\niterations={it}\ndeterministic=1\nfight_style={fs}\ndesired_targets=1\n"
        f"input=../char_2026-10-07_2124.simc\ninput=p1_variants.simc\n")
print(len(V), "variants")
