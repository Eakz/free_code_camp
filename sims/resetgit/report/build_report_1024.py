#!/usr/bin/env python3
"""Resetgit BM gear plan, export 2026-10-24 03:18. One self-contained HTML, icons as data URIs.

    python3 build_report_1024.py <icon_dir> <out.html>

Numbers come from ../opt_1024/out_sweep_*.json (single changes) and out_final_*.json (sets), SimC midnight 3af1a75,
data 12.1.5.70575. Single-change values are read from the JSON at build time so the page matches the raw output."""
import base64, html, json, math, os, sys
ICON_DIR, OUT = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
OPT = os.path.join(HERE, "..", "opt_1024")

def ic(n):
    with open(os.path.join(ICON_DIR, n + ".png"), "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()
def load(name):
    d = json.load(open(os.path.join(OPT, name)))
    b = d["sim"]["players"][0]["collected_data"]["dps"]["mean"]
    return {r["name"]: 100 * (r["mean"] / b - 1) for r in d["sim"]["profilesets"]["results"]}
SR, SM = load("out_sweep_Patchwerk.json"), load("out_sweep_DungeonSlice.json")
FR, FM = load("out_final_Patchwerk.json"), load("out_final_DungeonSlice.json")
def pct(v): return f"{v:+.2f}%"

SLOT_ICON = {"Head": "INV_Helmet_25", "Neck": "INV_Jewelry_Necklace_07", "Shoulder": "INV_Shoulder_29", "Back": "INV_Misc_Cape_18",
             "Chest": "INV_Chest_Chain_10", "Wrist": "INV_Bracer_13", "Hands": "INV_Gauntlets_29", "Waist": "INV_Belt_29",
             "Legs": "INV_Pants_Mail_15", "Feet": "INV_Boots_Chain_05", "Ring 1": "INV_Jewelry_Ring_14", "Ring 2": "INV_Jewelry_Ring_36",
             "Trinket 1": "INV_Trinket_80_Titan02a", "Trinket 2": "INV_Misc_Gem_Variety_01", "Weapon": "INV_Weapon_Bow_07"}
GEM_ICON = {"Indecipherable Eversong Diamond": "INV_Misc_Gem_Diamond_07", "Powerful Eversong Diamond": "INV_Misc_Gem_Diamond_07",
            "Flawless Deadly Amethyst": "INV_Misc_Gem_Amethyst_01", "Flawless Deadly Peridot": "INV_Misc_Gem_Emerald_01"}
I = {k: ic(v) for k, v in {**SLOT_ICON, **GEM_ICON}.items()}
I["_ench"] = ic("INV_Enchant_EssenceMagicLarge"); I["_hunter"] = ic("Ability_Hunter_BeastCall")
WH = "https://www.wowhead.com/item={}"
SLOTS_L = ["Head", "Neck", "Shoulder", "Back", "Chest", "Wrist", "Hands", "Waist"]
SLOTS_R = ["Legs", "Feet", "Ring 1", "Ring 2", "Trinket 1", "Trinket 2", "Weapon"]
def it(name, iid, ilvl, track, ench="", gems=(), stats="", note="", changed=False, src="Worn"):
    return dict(name=name, id=iid, ilvl=ilvl, track=track, ench=ench, gems=list(gems), stats=stats, note=note, changed=changed, src=src)

NOW = {
 "Head": it("Skulking Viper's Weeping Fangs", 271492, 334, "Tier · Myth 6/6", "Empowered Rune of Avoidance", stats="Haste / Mastery"),
 "Neck": it("Flowform Choker", 171720, 321, "Hero 6/6", gems=["Powerful Eversong Diamond"], stats="Haste / Mastery"),
 "Shoulder": it("Jaws of the Skulking Viper", 271490, 308, "Tier · Champion 6/6", stats="Crit / Haste"),
 "Back": it("Speakeasy Shroud", 251132, 321, "Hero 6/6"),
 "Chest": it("Skulking Viper's Scuteplate", 271495, 321, "Tier · Hero 6/6", "Mark of the Worldsoul", stats="Haste / Mastery"),
 "Wrist": it("Galerider's Mesh Wraps", 272254, 321, "Hero, now 305 → 321: 5 steps, 100 Hero crests"),
 "Hands": it("Skulking Viper's Hidepiercers", 271493, 334, "Tier · Myth, now 328 → 334: 2 steps, 40 Myth crests"),
 "Waist": it("Farstrider's Trophy Belt", 244581, 331, "Crafted Q5 · Arcanoweave", stats="Vers / Mastery"),
 "Legs": it("Galerider's Chausses", 272251, 308, "Champion 6/6", "Agility kit (8161)", stats="Haste / Vers"),
 "Feet": it("Galerider's Footguards", 272248, 321, "Hero 6/6", "Lynx's Dexterity", stats="Crit / Mastery"),
 "Ring 1": it("Hex Loop", 272149, 321, "Hero 6/6", "Eyes of the Eagle", ["Flawless Deadly Amethyst"], "Crit / Mastery"),
 "Ring 2": it("Sickening Signet of Atroxus", 252258, 321, "Hero 6/6", "Eyes of the Eagle", ["Flawless Deadly Amethyst"], "Haste / Mastery"),
 "Trinket 1": it("Freightrunner's Flask", 250215, 321, "Hero 6/6"),
 "Trinket 2": it("Resonant Bellowstone", 250228, 321, "Hero 6/6"),
 "Weapon": it("Aln'hara Sprigshot", 265337, 331, "Crafted Q5 · Hunter's Ritual Stone", "Rite of the Hash'ey", stats="Crit / Mastery"),
}
def swap(base, **ch):
    d = dict(base)
    for k, v in ch.items(): d[k.replace("_", " ")] = v
    return d
KIT = it("Galerider's Chausses", 272251, 308, "Champion 6/6", "Agility & Stamina kit (8159)", stats="Haste / Vers",
         note=f"{pct(SM['EN_le_AgiStamKit'])} M+ · {pct(SR['EN_le_AgiStamKit'])} raid", changed=True)
NECKG = it("Flowform Choker", 171720, 321, "Hero 6/6", gems=["Indecipherable Eversong Diamond"], stats="Haste / Mastery",
           note=f"{pct(SM['GEM_neck_Indecipherable'])} M+ · {pct(SR['GEM_neck_Indecipherable'])} raid", changed=True)
CLEGS = lambda st, n: it("Farstrider's Reinforced Faulds", 244582, 331, "Crafted Q5 · 80 Myth crests + Sparks", "Agility & Stamina kit (8159)",
                         stats=st, note=n, changed=True, src="Craft")
VILE = lambda gem, n: it("Vile Alchemist's Band", 268249, 334, "Myth, now 318 → 334: 100 Myth crests", "Eyes of the Eagle", [gem],
                         "Crit / Mastery", n, True, "Vashnik (bags)")
FREE = swap(NOW, Legs=KIT, Neck=NECKG)
MPLUS = swap(FREE,
  Legs=CLEGS("Crit / Haste", f"{pct(SM['CR_Legs331_CH'])} M+ alone"),
  Wrist=it("Farstrider's Plated Bracers", 244584, 331, "Crafted Q5 · 80 Myth crests + Sparks", stats="Haste / Mastery",
           note=f"{pct(SM['CR_Wrist331_HM'])} M+ alone (tie)", changed=True, src="Craft"),
  Ring_1=VILE("Flawless Deadly Amethyst", f"{pct(SM['R1_VileAlchemist334'])} M+ alone; replaces Hex Loop"),
  Neck=it("Sentinel's Vitriolic Chain", 268250, 334, "Myth, now 318 → 334: 100 Myth crests", gems=["Indecipherable Eversong Diamond"],
          stats="Crit / Haste", note="M+ tie with Flowform (+0.06%); same neck as raid", changed=True, src="bags"))
NK = {}
for fs in ("Patchwerk", "DungeonSlice"): NK[fs] = load(f"out_neck_{fs}.json")
RAID = swap(FREE,
  Legs=CLEGS("Crit / Haste", f"{pct(SR['CR_Legs331_CH'])} raid alone"),
  Wrist=it("Farstrider's Plated Bracers", 244584, 331, "Crafted Q5 · 80 Myth crests + Sparks", stats="Crit / Haste",
           note=f"{pct(SR['CR_Wrist331_CH'])} raid alone", changed=True, src="Craft"),
  Neck=it("Sentinel's Vitriolic Chain", 268250, 334, "Myth, now 318 → 334: 100 Myth crests", gems=["Indecipherable Eversong Diamond"],
          stats="Crit / Haste", note=f"{pct(SR['NE_SentinelsVitriolic334'])} raid alone; replaces Flowform Choker", changed=True, src="bags"),
  Ring_1=VILE("Flawless Deadly Peridot", f"{pct(SR['R1_VileAlchemist334'])} raid alone; replaces Hex Loop"),
  Ring_2=it("Sickening Signet of Atroxus", 252258, 321, "Hero 6/6", "Eyes of the Eagle", ["Flawless Deadly Peridot"], "Haste / Mastery",
            "gem swap: tie (+0.1%)", True))
SETS = [
 ("now", "Today", NOW, "0.00%", "0.00%", "Your worn gear at its upgrade caps (hands 334, wrist 321 are counted as upgraded). The 0% line for this page."),
 ("free", "Free fixes", FREE, pct(FM["M1_free"]), pct(FR["R1_free"]),
  "Leg kit and neck diamond. No crests. Raid number includes the 'solos' talents (+2.29% alone); M+ keeps your current talents."),
 ("mplus", "Best M+", MPLUS, pct(NK["DungeonSlice"]["M4_sentinel334"]), "–",
  "Current talents. Two crafts, Myth ring and Myth neck (the neck ties Flowform in M+ but is the same neck you want for raid). Without the wrist craft: " + pct(FM["M3_vile+craftlegs"]) + "."),
 ("raid", "Best raid", RAID, "–", pct(FR["R4_myth+craft_legs+wrist"]),
  "'solos' talents. Two crafts, Myth neck and ring. Without the crafts (neck + ring only): " + pct(FR["R3_myth_sentinel+vile"]) + ". Venomstone on the neck (340): " + pct(NK["Patchwerk"]["R4_sentinel340_venomstone"]) + "."),
]
ORDER = [
 ("Leg kit: Agility kit → Agility & Stamina kit (8159). The Armor kit (8163) ties.", "free", SM["EN_le_AgiStamKit"], SR["EN_le_AgiStamKit"]),
 ("Neck gem: Powerful → Indecipherable Eversong Diamond.", "free", SM["GEM_neck_Indecipherable"], SR["GEM_neck_Indecipherable"]),
 ("Raid only: load the 'solos' talents. Never in M+.", "free", SM["TAL_solos"], SR["TAL_solos"]),
 ("Upgrade Skulking Viper's Hidepiercers 328 → 334 and Galerider's Mesh Wraps 305 → 321 (already counted in every number).", "40 Myth + 100 Hero crests", None, None),
 ("Craft Farstrider's Reinforced Faulds, Crit/Haste, 331 (replaces Galerider's Chausses). Biggest gear gain.", "Sparks + 80 Myth crests", SM["CR_Legs331_CH"], SR["CR_Legs331_CH"]),
 ("Upgrade Vile Alchemist's Band 318 → 334 and wear it instead of Hex Loop. Helps both modes.", "100 Myth crests", SM["R1_VileAlchemist334"], SR["R1_VileAlchemist334"]),
 ("Upgrade Sentinel's Vitriolic Chain 318 → 334 (replaces Flowform Choker). Raid +0.74% inside the set; M+ tie, so wear it everywhere.", "100 Myth crests", SM["NE_SentinelsVitriolic334"], SR["NE_SentinelsVitriolic334"]),
 ("Craft Farstrider's Plated Bracers 331 (Haste/Mastery for M+, Crit/Haste for raid). Smallest gain: only if you have Sparks to spare.", "Sparks + 80 Myth crests", SM["CR_Wrist331_HM"], SR["CR_Wrist331_CH"]),
]
LOSE = [("Gebbo's Backup Blaster 334", "Weapon", "MH_GebbosBackupBlaster334"), ("Snakebite Recurve 321", "Weapon", "MH_SnakebiteRecurve321"),
        ("Crown of the Eternal Fang 321 + tier legs", "Head", "HE_CrownEternalFang321+TL"), ("Voidscarred Crown 321 + tier legs", "Head", "HE_VoidscarredCrown321+TL"),
        ("Season's Turn Gauntlets 321 + tier legs", "Hands", "HA_SeasonsTurn321+TL"), ("Yoke of the Charging Bear 321", "Neck", "NE_Yoke321"),
        ("Band of the Amani Warlord 321", "Ring", "R1_Amani321"), ("Lightwarden's Bind 321", "Ring", "R1_Lightwarden321"),
        ("Silken Voodoo Drape 321", "Back", "BA_SilkenVoodoo321"), ("Miststalker's Shroud 321", "Back", "BA_MiststalkerShroud321"),
        ("Felsoaked Soles 321", "Feet", "FE_FelsoakedSoles321"), ("Galerider's Mail Skirt 321 (loses Arcanoweave)", "Waist", "WA_GaleriderSkirt321_noEmb"),
        ("Belt of the Consecrated Tomb 321 (loses Arcanoweave)", "Waist", "WA_ConsecratedTomb321_noEmb"), ("Tier legs 308 (catalyst) alone", "Legs", "LE_TierLegs308"),
        ("Effigy of Ula'tek's Faithful 308", "Trinket", "T2_Effigy308"), ("Glorious Crusader's Keepsake 308", "Trinket", "T2_Keepsake308"),
        ("Tattered Amani War Banner 321", "Trinket", "T2_TatteredBanner321"), ("Sylvan Wakrapuku 321", "Trinket", "T2_Wakrapuku321"),
        ("Tiny Electromental in a Jar 321", "Trinket", "T2_TinyElectromental321"), ("Keeper's Seething Core 295", "Trinket", "T1_KeepersCore295"),
        ("Drum of Renewed Bonds 321", "Trinket", "T2_DrumRenewedBonds321"), ("Ophidian Bone Whistle 321", "Trinket", "T2_OphidianWhistle321"),
        ("Spirit-Rending Poison 321", "Trinket", "T2_SpiritRending321")]
def rng(prefix, d):
    v = [x for k, x in d.items() if k.startswith(prefix)]
    return f"{min(v):+.1f} to {max(v):+.1f}%"
ENCH = [
 ("Legs", "Agility & Stamina kit (or Armor kit)", "your Agility kit is 0.5% lower", "change"),
 ("Neck gem", "Indecipherable Eversong Diamond", "Stoic and Telluric tie or lose", "change"),
 ("Rings", "Eyes of the Eagle", "others " + rng("EN_rings_", SM) + " M+", "keep"),
 ("Ring gems", "Flawless Deadly Amethyst (M+) · Deadly Peridot (raid)", "every Flawless gem within ±0.4%", "keep or swap, tie"),
 ("Weapon", "Rite of the Hash'ey", "others " + rng("EN_ma_", SM) + " M+", "keep"),
 ("Chest", "Mark of the Worldsoul", "others " + rng("EN_ch_", SM) + " M+", "keep"),
 ("Head / Shoulder / Feet", "any", "no measurable damage", "keep"),
]
TAL = [("M+", "Your current build", f"Best. 'aa' and 'delve' are identical in damage; Raider.IO {pct(SM['TAL_Raider_IO_Build'])}; solos {pct(SM['TAL_solos'])}."),
       ("Raid ST", "'solos'", f"{pct(SR['TAL_solos'])}. Current, 'aa', 'delve' tie at 0; Raider.IO {pct(SR['TAL_Raider_IO_Build'])}.")]
NOTES = [
 "SimC midnight 3af1a75 (2026-10-23), game data 12.1.5.70575. Your client is 70529: SimC is one build newer and includes the Oct 23 hotfixes.",
 "Raid = Patchwerk; M+ = DungeonSlice. Sweep: 5,000 / 2,000 iterations (±0.07% / ±0.57%). Final sets: 10,000 / 5,000 (±0.06% / ±0.37%). M+ single changes under 0.6% are ties; set totals are what to trust.",
 "Every variant ran as its own profileset (not 100 copies in one raid). The whole job took about 15 minutes of simming.",
 "Caps: Champion 308, Hero 321, Myth 334, crafted 331. Venomstones (Hero 328 / Myth 340 on weapons, trinkets, necks) were not applied.",
 "Crafted pieces carry no embellishment: your belt (Arcanoweave) and bow (Hunter's Ritual Stone) already use the cap of 2.",
 "Plan assumes unlimited Myth crests (your call): every Myth-track item is used at 334. The real limits left are Sparks of Tides (2-4 per 331 craft, single source; not in the export) and 100 Hero crests for the wrist (you have 275).",
 'Sources: <a href="https://www.icy-veins.com/wow/news/these-five-mistcrests-decide-how-fast-your-gear-climbs-in-midnight-season-2/">Icy Veins crests</a>, <a href="https://expcarry.com/wow-midnight-season-2-crafting-guide">expcarry crafting</a>, <a href="https://www.method.gg/guides/how-to-unlock-ascendant-venomstones-in-wow-midnight-season-2-neck-weapon-trinket-upgrades">Method Venomstones</a>.',
 "Inputs and raw outputs: sims/resetgit/opt_1024 on branch claude/epic-cori-kqdhlt.",
]

E = html.escape
def gem_html(g): return f'<span class="gem-w"><img class="gem" src="{I[g]}" alt="">{E(g)}</span>'
def item_html(slot, x):
    cls = "item changed" if x["changed"] else "item"
    ench = f'<div class="ench"><img src="{I["_ench"]}" alt="">{E(x["ench"])}</div>' if x["ench"] else ""
    gems = f'<div class="gems">{"".join(gem_html(g) for g in x["gems"])}</div>' if x["gems"] else ""
    note = f'<div class="gain">{E(x["note"])}</div>' if x["note"] else ""
    src = "" if x["src"] == "Worn" else f' · <span class="src">{E(x["src"])}</span>'
    stats = f' · {E(x["stats"])}' if x["stats"] else ""
    return (f'<div class="{cls}"><div class="ic"><img src="{I[slot]}" alt=""><span class="ilvl">{x["ilvl"]}</span></div>'
            f'<div class="meta"><div class="slot">{slot}</div><a class="name" href="{WH.format(x["id"])}" target="_blank" rel="noopener">{E(x["name"])}</a>'
            f'<div class="sub">{E(x["track"])}{src}{stats}</div>{ench}{gems}{note}</div></div>')
tabs, panels = [], []
for k, label, gear, mp, rd, desc in SETS:
    tabs.append(f'<button class="tab" role="tab" data-k="{k}" id="t-{k}" aria-controls="p-{k}">{E(label)}<span class="chip">{mp if mp != "–" else rd}</span></button>')
    panels.append(f'<div class="panel" id="p-{k}" role="tabpanel" aria-labelledby="t-{k}"><div class="ph"><div><h3>{E(label)}</h3><p>{E(desc)}</p></div>'
                  f'<div class="nums"><div><b>{mp}</b><span>M+</span></div><div><b>{rd}</b><span>Raid</span></div></div></div>'
                  f'<div class="doll"><div class="col">{"".join(item_html(s, gear[s]) for s in SLOTS_L)}</div>'
                  f'<div class="col">{"".join(item_html(s, gear[s]) for s in SLOTS_R)}</div></div></div>')
def cell(v): return "<td class='g'>–</td>" if v is None else f"<td class='g'>{pct(v)}</td>"
order = "".join(f"<tr><td>{i}</td><td>{E(d)}</td><td class='c'>{E(c)}</td>{cell(m) if (m is None or m > -5) else '<td class=g>loses</td>'}{cell(r)}</tr>"
                for i, (d, c, m, r) in enumerate(ORDER, 1))
order = order.replace(f"<td class='g'>{pct(SM['TAL_solos'])}</td>", f"<td class='g'>{pct(SM['TAL_solos'])}</td>")
lose = "".join(f"<tr><td>{E(n)}</td><td class='c'>{E(s)}</td>{cell(SM[k])}{cell(SR[k])}</tr>" for n, s, k in LOSE)
ench = "".join(f"<tr><td>{E(a)}</td><td>{E(b)}</td><td class='c'>{E(c)}</td><td>{E(d)}</td></tr>" for a, b, c, d in ENCH)
tal = "".join(f"<tr><td>{E(a)}</td><td>{E(b)}</td><td class='c'>{E(c)}</td></tr>" for a, b, c in TAL)
tpl = open(os.path.join(HERE, "template_1024.html"), encoding="utf-8").read()
for k, v in {"{{HUNTER}}": I["_hunter"], "{{TABS}}": "".join(tabs), "{{PANELS}}": "".join(panels), "{{ORDER}}": order,
             "{{LOSE}}": lose, "{{ENCH}}": ench, "{{TAL}}": tal, "{{NOTES}}": "".join(f"<li>{n}</li>" for n in NOTES)}.items():
    tpl = tpl.replace(k, v)
tpl = tpl.replace("var start='dung';", "var start='mplus';").replace("'rg-tab'", "'rg2-tab'")
open(OUT, "w", encoding="utf-8").write(tpl)
print(OUT, len(tpl), "unfilled:", tpl.count("{{"))
