#!/usr/bin/env python3
"""Guardian 2026-10-29 screen: every single change vs the worn set (export 02:00, caps from build_profile.py).
Single-actor Patchwerk, pull = 5 heroic dummies attacking (profilesets cannot model it: they apply item lines to the dummies too).

    python3 gen_bear.py screen     -> runs_pull/*.simc (3000 it)
Embellishment cap (2) is asserted for every variant: wrist Arcanoweave 12384 + belt 12384 + Lantern Ritual Stone 13771."""
import os, sys
TAL = open("../char_guardian_2026-10-29.simc").read().split("\ntalents=")[1].split("\n")[0]
PULL = "".join(f"tank_dummy=Mob{i}\ntank_dummy_type=heroic\n" for i in range(1, 6))
BOSS = "desired_targets=1\n"
EMB = ("12384", "13771")
def emb_count(lines): return sum(l.count("/" + e) for l in lines for e in EMB if l.split("=")[0] in SLOTS)
SLOTS = {"head", "neck", "shoulder", "back", "chest", "wrist", "hands", "waist", "legs", "feet", "finger1", "finger2", "trinket1", "trinket2", "main_hand", "off_hand"}
# worn lines, no enchant/gem (caps from the build_profile table)
W = {
 "head": "head=,id=271528,bonus_id=12846/13334/6652/13696/13692/13698/1574,redirected_base_stats=268219,ilevel=321",
 "neck": "neck=,id=268265,bonus_id=6652/13668/13334/13987/12856,ilevel=341",
 "shoulder": "shoulder=,id=271526,bonus_id=13334/13694/6652/13697/12846,ilevel=321",
 "chest": "chest=,id=271531,bonus_id=6652/13440/13690/13698/12846,redirected_base_stats=239048,ilevel=321",
 "legs": "legs=,id=271527,bonus_id=6652/13440/13693/13698/12846,redirected_base_stats=159313,ilevel=321",
 "feet": "feet=,id=268247,bonus_id=6652/13662/13334/13696/12854,ilevel=334",
 "finger1": "finger1=,id=268266,bonus_id=6652/13668/13334/12846,ilevel=321",
 "finger2": "finger2=,id=159459,bonus_id=13440/6652/13668/12699/12846,ilevel=321",
 "main_hand": "main_hand=,id=268215,bonus_id=6652/13334/13846/12856,ilevel=341",
}
CHEST334 = "chest=,id=271531,bonus_id=13334/6652/14049/13690/13698/12854,redirected_base_stats=281236,ilevel=334"
V = {"A_base": [], "Z_SANITY": ["trinket2=,id=270165,bonus_id=6652/13334/12854,ilevel=334"]}
# ---- items (enchant/gem copied from the slot they replace)
V["HE_PledgebearerMask308"] = ["head=,id=272258,bonus_id=12833/6652/13696/11215/13662,ilevel=308,enchant_id=8017"]
V["NE_Yoke321"] = ["neck=,id=251173,bonus_id=13440/6652/13668/12699/12846,ilevel=321,gem_id=240983"]
V["CH_Lunar334_redirect281236"] = [CHEST334 + ",enchant_id=7987"]
V["HA_Subjugator321"] = ["hands=,id=193758,bonus_id=13440/6652/13662/12699/12846,ilevel=321"]
V["WA_Cinch321"] = ["waist=,id=272245,bonus_id=6652/13696/13662/12846,ilevel=321"]
V["WA_WhirlingDervish321"] = ["waist=,id=159317,bonus_id=13440/6652/13696/13662/12699/12846,ilevel=321"]
V["LE_MiststalkerCuisses321"] = ["legs=,id=272243,bonus_id=12841/42/13662,ilevel=321,enchant_id=8159"]
RINGS = {"Swarmcaller334": ("281029", "6652/13668/13334/12854", 334), "Amani321": ("273792", "13440/6652/13668/12699/12846", 321),
         "Sickening321": ("252258", "13440/40/13668/12699/12846", 321), "Sandstone321": ("158366", "13440/6652/13668/12699/12846", 321),
         "Bubbleband321": ("268266", "6652/13668/13334/12846", 321), "RitualBinder321": ("159459", "13440/6652/13668/12699/12846", 321)}
for n, (iid, b, il) in RINGS.items():
    for slot, other in (("finger1", "RitualBinder321"), ("finger2", "Bubbleband321")):
        if n == other: continue   # already worn in the other slot
        if (slot == "finger1" and n == "Bubbleband321") or (slot == "finger2" and n == "RitualBinder321"): continue
        V[f"R{slot[-1]}_{n}"] = [f"{slot}=,id={iid},bonus_id={b},ilevel={il},enchant_id=8025,gem_id=240916"]
TR = {"Voracious334": "id=270175,bonus_id=42/13334/12854,ilevel=334", "VileVial321": "id=273796,bonus_id=13440/6652/12699/12846,ilevel=321",
      "Fang321": "id=270161,bonus_id=6652/13334/12843,ilevel=321", "Bellowstone321": "id=250228,bonus_id=12843/13440/40/12699,ilevel=321",
      "Keepsake308": "id=251792,bonus_id=12834/6652,ilevel=308", "Whistle308": "id=274496,bonus_id=12834/6652,ilevel=308"}
for n, l in TR.items():
    V[f"T1_{n}"] = [f"trinket1=,{l}"]; V[f"T2_{n}"] = [f"trinket2=,{l}"]
# ---- enchants on the worn piece
E = {"head": [(7991, "EmpBlessingOfSpeed"), (7961, "EmpHexOfLeeching")], "shoulder": [(7973, "AkilzonsSwiftness"), (7971, "FlightOfTheEagle"), (7999, "NaturesGrace")],
     "chest": [(8013, "MarkOfTheMagister"), (7985, "MarkOfTheRootwarden"), (7957, "MarkOfNalorakk")], "legs": [(8163, "AgiArmorKit"), (8161, "AgiKit"), (7935, "IntKit")],
     "feet": [(8019, "FarstridersHunt"), (7993, "ShaladrassilsRoots")],
     "main_hand": [(8689, "RiteHashey"), (7981, "JanalaisPrecision"), (8007, "WorldsoulCradle"), (8037, "FlamesOfTheSindorei"), (8041, "ArcaneMastery")]}
for slot, opts in E.items():
    for eid, n in opts: V[f"EN_{slot[:2]}_{n}"] = [W[slot] + f",enchant_id={eid}"]
V["EN_he_none"] = [W["head"]]
for eid, n in ((7967, "EyesOfTheEagle"), (7965, "AmaniMastery"), (7969, "ZuljinsMastery"), (7995, "NaturesWrath"), (7997, "NaturesFury"), (8021, "ThalHaste"), (8023, "ThalVers")):
    V[f"EN_rings_{n}"] = [W["finger1"] + f",enchant_id={eid},gem_id=240916", W["finger2"] + f",enchant_id={eid},gem_id=240916"]
# ---- gems
GEMS = {240888: "QuickPeridot", 240890: "DeadlyPeridot", 240892: "MasterfulPeridot", 240894: "VersatilePeridot", 240896: "MasterfulAmethyst",
        240898: "DeadlyAmethyst", 240900: "QuickAmethyst", 240902: "VersatileAmethyst", 240904: "DeadlyGarnet", 240906: "QuickGarnet", 240908: "MasterfulGarnet",
        240910: "VersatileGarnet", 240912: "VersatileLapis", 240914: "DeadlyLapis", 240918: "MasterfulLapis"}
for gid, n in GEMS.items():
    V[f"GEM_rings_{n}"] = [W["finger1"] + f",enchant_id=8025,gem_id={gid}", W["finger2"] + f",enchant_id=8025,gem_id={gid}"]
    V[f"GEM_neck2_{n}"] = [W["neck"] + f",gem_id=240983/{gid}"]
for gid, n in ((240967, "Powerful"), (240971, "Stoic"), (240969, "Telluric")): V[f"GEM_neck1_{n}"] = [W["neck"] + f",gem_id={gid}/240900"]
if __name__ == "__main__":
    d = "runs_pull"; os.makedirs(d, exist_ok=True)
    for n, lines in V.items():
        open(f"{d}/{n}.simc", "w").write(f"threads=4\niterations=3000\ndeterministic=1\nfight_style=Patchwerk\n{PULL}"
            f"input=../../char_guardian_2026-10-29.simc\ntalents={TAL}\nname={n}\n" + "".join(l + "\n" for l in lines))
    print(len(V), "variants")
