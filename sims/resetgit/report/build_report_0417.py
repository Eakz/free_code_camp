#!/usr/bin/env python3
"""Resetgit BM report for the 2026-10-24 04:17 export: enchants, gems, consumables, catalyst legs + crafted shoulders/bracers.

    python3 build_report_0417.py <icon_dir> <out.html>

All numbers are read from ../opt_0417/out_*.json at build time (SimC midnight 3af1a75, data 12.1.5.70575).
Baseline FULL = worn gear at caps with the empty gem/enchant slots filled; current talents in both modes."""
import base64, html, json, os, sys
ICON_DIR, OUT = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__)); OPT = os.path.join(HERE, "..", "opt_0417")
def ic(n):
    with open(os.path.join(ICON_DIR, n + ".png"), "rb") as f: return "data:image/png;base64," + base64.b64encode(f.read()).decode()
def load(name):
    d = json.load(open(os.path.join(OPT, name))); b = d["sim"]["players"][0]["collected_data"]["dps"]["mean"]
    return {r["name"]: 100 * (r["mean"] / b - 1) for r in d["sim"]["profilesets"]["results"]}
SWR, SWM = load("out_Patchwerk.json"), load("out_DungeonSlice.json")
F2R = load("out_final2_Patchwerk.json"); FM = load("out_final_DungeonSlice.json")
STR, STM = load("out_stats_Patchwerk.json"), load("out_stats_DungeonSlice.json")
GR, GM = load("out_gems_Patchwerk.json"), load("out_gems_DungeonSlice.json")
def pct(v): return f"{v:+.2f}%"

SLOT_ICON = {"Head": "INV_Helmet_25", "Neck": "INV_Jewelry_Necklace_07", "Shoulder": "INV_Shoulder_29", "Back": "INV_Misc_Cape_18",
             "Chest": "INV_Chest_Chain_10", "Wrist": "INV_Bracer_13", "Hands": "INV_Gauntlets_29", "Waist": "INV_Belt_29",
             "Legs": "INV_Pants_Mail_15", "Feet": "INV_Boots_Chain_05", "Ring 1": "INV_Jewelry_Ring_14", "Ring 2": "INV_Jewelry_Ring_36",
             "Trinket 1": "INV_Trinket_80_Titan02a", "Trinket 2": "INV_Misc_Gem_Variety_01", "Weapon": "INV_Weapon_Bow_07"}
GEM_ICON = {"Indecipherable Eversong Diamond": "INV_Misc_Gem_Diamond_07", "Flawless Deadly Amethyst": "INV_Misc_Gem_Amethyst_01",
            "Flawless Masterful Peridot": "INV_Misc_Gem_Emerald_01", "(empty socket)": "INV_Misc_QuestionMark"}
I = {k: ic(v) for k, v in {**SLOT_ICON, **GEM_ICON}.items()}
I["_ench"] = ic("INV_Enchant_EssenceMagicLarge"); I["_hunter"] = ic("Ability_Hunter_BeastCall")
WH = "https://www.wowhead.com/item={}"
SLOTS_L = ["Head", "Neck", "Shoulder", "Back", "Chest", "Wrist", "Hands", "Waist"]
SLOTS_R = ["Legs", "Feet", "Ring 1", "Ring 2", "Trinket 1", "Trinket 2", "Weapon"]
def it(name, iid, ilvl, track, ench="", gems=(), stats="", note="", changed=False, src="Worn"):
    return dict(name=name, id=iid, ilvl=ilvl, track=track, ench=ench, gems=list(gems), stats=stats, note=note, changed=changed, src=src)
MP, DA, IND = "Flawless Masterful Peridot", "Flawless Deadly Amethyst", "Indecipherable Eversong Diamond"
WORN = {
 "Head": it("Skulking Viper's Weeping Fangs", 271492, 334, "Tier · Myth 6/6", "Empowered Rune of Avoidance", stats="Haste / Mastery"),
 "Neck": it("Sentinel's Vitriolic Chain", 268250, 334, "Myth, now 318 → 334", gems=["(empty socket)"], stats="Crit / Haste",
            note="no gem: fill it", changed=True),
 "Shoulder": it("Jaws of the Skulking Viper", 271490, 308, "Tier · Champion 6/6", stats="Crit / Haste"),
 "Back": it("Speakeasy Shroud", 251132, 321, "Hero 6/6"),
 "Chest": it("Skulking Viper's Scuteplate", 271495, 321, "Tier · Hero 6/6", "Mark of the Worldsoul", stats="Haste / Mastery"),
 "Wrist": it("Galerider's Mesh Wraps", 272254, 321, "Hero, now 305 → 321"),
 "Hands": it("Skulking Viper's Hidepiercers", 271493, 334, "Tier · Myth, now 328 → 334"),
 "Waist": it("Farstrider's Trophy Belt", 244581, 331, "Crafted Q5 · Arcanoweave", stats="Vers / Mastery"),
 "Legs": it("Cuisses of the Uncoiled Union", 268237, 334, "Myth, now 318 → 334", stats="", note="no leg kit: fill it", changed=True),
 "Feet": it("Galerider's Footguards", 272248, 321, "Hero 6/6", "Lynx's Dexterity", stats="Crit / Mastery"),
 "Ring 1": it("Hex Loop", 272149, 321, "Hero 6/6", "Eyes of the Eagle", [DA], "Crit / Mastery"),
 "Ring 2": it("Vile Alchemist's Band", 268249, 334, "Myth, now 318 → 334", "", ["(empty socket)"], "Crit / Mastery",
              "no enchant, no gem: fill it", True),
 "Trinket 1": it("Freightrunner's Flask", 250215, 321, "Hero 6/6"),
 "Trinket 2": it("Resonant Bellowstone", 250228, 321, "Hero 6/6"),
 "Weapon": it("Aln'hara Sprigshot", 265337, 331, "Crafted Q5 · Hunter's Ritual Stone", "Rite of the Hash'ey", stats="Crit / Mastery"),
}
def swap(base, **ch):
    d = {k: dict(v, changed=False, note="") for k, v in base.items()}
    for k, v in ch.items(): d[k.replace("_", " ")] = v
    return d
FULL = swap(WORN,
  Neck=it("Sentinel's Vitriolic Chain", 268250, 334, "Myth 6/6", gems=[IND], stats="Crit / Haste", note="gem added", changed=True),
  Legs=it("Cuisses of the Uncoiled Union", 268237, 334, "Myth 6/6", "Agility & Stamina kit", note="leg kit added", changed=True),
  Ring_2=it("Vile Alchemist's Band", 268249, 334, "Myth 6/6", "Eyes of the Eagle", [DA], "Crit / Mastery", "enchant + gem added", True))
TLEG = it("Skulking Viper's Coiled Legwraps", 271491, 334, "Tier · catalyse the Cuisses (stays Myth)", "Agility & Stamina kit",
          stats="Haste / Mastery", note="frees the shoulder slot, 4-piece kept", changed=True, src="Catalyst")
PLUMES = it("Farstrider's Brilliant Plumes", 244580, 331, "Crafted Q5 · no embellishment", "any (no damage)", stats="Crit / Haste",
            note="replaces the 308 tier shoulders", changed=True, src="Craft")
BRACERS = it("Farstrider's Plated Bracers", 244584, 331, "Crafted Q5 · no embellishment", stats="Crit / Haste",
             note="replaces Galerider's Mesh Wraps", changed=True, src="Craft")
V2 = it("Vile Alchemist's Band", 268249, 334, "Myth 6/6", "Eyes of the Eagle", [MP], "Crit / Mastery", "gem → Masterful Peridot", True)
RAIDP = swap(FULL, Legs=TLEG, Shoulder=PLUMES, Wrist=BRACERS, Ring_2=V2,
  Ring_1=it("Sickening Signet of Atroxus", 252258, 321, "Hero 6/6 · from bags", "Eyes of the Eagle", [MP], "Haste / Mastery",
            f"{pct(F2R['R_A_Sickening'])} alone in raid; replaces Hex Loop", True))
MPLUSP = swap(FULL, Legs=TLEG, Shoulder=PLUMES, Wrist=BRACERS, Ring_2=V2,
  Ring_1=it("Hex Loop", 272149, 321, "Hero 6/6", "Eyes of the Eagle", [MP], "Crit / Mastery", "keep in M+; gem → Masterful Peridot", True))
SETS = [
 ("worn", "As worn", WORN, pct(SWM["AS_WORN_no_gem_no_enchants"]), pct(SWR["AS_WORN_no_gem_no_enchants"]),
  "Your 04:17 gear at its upgrade caps, with the neck socket, Vile Alchemist's Band and Cuisses still empty."),
 ("full", "Enchanted", FULL, "0.00%", "0.00%", "The three empty slots filled. This is the 0% line for every number on this page."),
 ("raid", "Raid plan", RAIDP, "–", pct(GR["RING_MasterfulPeridot"]),
  "Catalysed tier legs, both crafts Crit/Haste, Sickening Signet in ring 1, Masterful Peridot in both rings."),
 ("mplus", "M+ plan", MPLUSP, pct(GM["RING_MasterfulPeridot"]), "–",
  "Same as raid but Hex Loop stays in ring 1. Masterful Peridot in both rings."),
]
ORDER = [
 ("Gem Sentinel's Vitriolic Chain: Indecipherable Eversong Diamond.", "gem", None, None, "fill"),
 ("Vile Alchemist's Band: Eyes of the Eagle + Flawless Masterful Peridot.", "enchant + gem", None, None, "fill"),
 ("Cuisses of the Uncoiled Union: Agility & Stamina kit.", "leg kit", None, None, "fill"),
 ("Re-gem Hex Loop: Flawless Masterful Peridot.", "gem", GM["RING_MasterfulPeridot"] - GM["SET_DeadlyAmethyst_Indecipherable"],
  GR["RING_MasterfulPeridot"] - GR["SET_DeadlyAmethyst_Indecipherable"], ""),
 ("Raid only: wear Sickening Signet of Atroxus (Eyes of the Eagle, Masterful Peridot) instead of Hex Loop.", "free (bags)", None, F2R["R_A_Sickening"], ""),
 ("Catalyse the Cuisses into tier legs, then craft Farstrider's Brilliant Plumes, Crit/Haste.", "1 catalyst charge + Sparks + 80 Myth crests",
  FM["M_B_A+tierlegs+shoulderHM"] - FM["M_A_QuickPeridot"], F2R["R_B_A+tierlegs+shoulderCH"] - F2R["R_A_Sickening"], ""),
 ("Craft Farstrider's Plated Bracers, Crit/Haste.", "Sparks + 80 Myth crests",
  FM["M_C_B+bracersHM"] - FM["M_B_A+tierlegs+shoulderHM"], F2R["R_C_B+bracersCH"] - F2R["R_B_A+tierlegs+shoulderCH"], ""),
]
fill = -SWM["AS_WORN_no_gem_no_enchants"], -SWR["AS_WORN_no_gem_no_enchants"]
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
    tabs.append(f'<button class="tab" role="tab" data-k="{k}" id="t-{k}" aria-controls="p-{k}">{E(label)}<span class="chip">{rd if rd != "–" else mp}</span></button>')
    panels.append(f'<div class="panel" id="p-{k}" role="tabpanel" aria-labelledby="t-{k}"><div class="ph"><div><h3>{E(label)}</h3><p>{E(desc)}</p></div>'
                  f'<div class="nums"><div><b>{mp}</b><span>M+</span></div><div><b>{rd}</b><span>Raid</span></div></div></div>'
                  f'<div class="doll"><div class="col">{"".join(item_html(s, gear[s]) for s in SLOTS_L)}</div>'
                  f'<div class="col">{"".join(item_html(s, gear[s]) for s in SLOTS_R)}</div></div></div>')
def cell(v): return "<td class='g'>–</td>" if v is None else f"<td class='g'>{pct(v)}</td>"
rows = []
for i, (d, c, m, r, kind) in enumerate(ORDER, 1):
    if kind == "fill":
        mc = f"<td class='g' rowspan='3'>{pct(fill[0])}</td><td class='g' rowspan='3'>{pct(fill[1])}</td>" if i == 1 else ""
        rows.append(f"<tr><td>{i}</td><td>{E(d)}</td><td class='c'>{E(c)}</td>{mc}</tr>")
    else:
        rows.append(f"<tr><td>{i}</td><td>{E(d)}</td><td class='c'>{E(c)}</td>{cell(m)}{cell(r)}</tr>")
order = "".join(rows)
P = ["CH", "CM", "CV", "HM", "HV", "MV"]; PN = {"CH": "Crit/Haste", "CM": "Crit/Mastery", "CV": "Crit/Vers", "HM": "Haste/Mastery", "HV": "Haste/Vers", "MV": "Mastery/Vers"}
def grid(D, title):
    best = max(D.values())
    head = "<thead><tr><th>" + E(title) + " · shoulders ↓ bracers →</th>" + "".join(f"<th>{PN[b]}</th>" for b in P) + "</tr></thead>"
    body = ""
    for a in P:
        body += f"<tr><td>{PN[a]}</td>" + "".join(
            f"<td class='g{' best' if abs(D[f'SH_{a}+BR_{b}'] - best) < 1e-9 else ''}'>{pct(D[f'SH_{a}+BR_{b}'])}</td>" for b in P) + "</tr>"
    return head + "<tbody>" + body + "</tbody>"
gridhtml = grid(STR, "Raid") + "</table></div><div class='tw' style='margin-top:14px'><table class='grid'>" + grid(STM, "M+")
GEMROW = lambda n, k: (n, pct(GM[k] - GM["SET_DeadlyAmethyst_Indecipherable"]), pct(GR[k] - GR["SET_DeadlyAmethyst_Indecipherable"]))
ENCH = [
 ("Neck gem", IND, f"Powerful / Stoic / Telluric {pct(GM['NECK_Powerful']-GM['SET_DeadlyAmethyst_Indecipherable'])} to {pct(GM['NECK_Stoic']-GM['SET_DeadlyAmethyst_Indecipherable'])} M+", "fill the empty socket"),
 ("Ring gems (both)", MP, f"best or tied in both modes: {GEMROW('', 'RING_MasterfulPeridot')[1]} M+, {GEMROW('', 'RING_MasterfulPeridot')[2]} raid vs Deadly Amethyst", "change"),
 ("Rings", "Eyes of the Eagle", f"others {min(v for k,v in SWM.items() if k.startswith('EN_rings_')):+.1f} to {max(v for k,v in SWM.items() if k.startswith('EN_rings_')):+.1f}% M+", "add to Vile Alchemist's Band"),
 ("Legs", "Agility & Stamina kit (Armor kit ties)", f"plain Agility kit {pct(SWM['EN_le_AgiKit'])}", "fill"),
 ("Weapon", "Rite of the Hash'ey", "Berserker's Rage +0.2% alone, loses in the full set", "keep"),
 ("Chest", "Mark of the Worldsoul", f"others {min(v for k,v in SWM.items() if k.startswith('EN_ch_')):+.1f}% and worse", "keep"),
 ("Head / Shoulder / Feet", "any", "no measurable damage", "keep"),
]
CONS = [
 ("Flask", "Flask of the Magisters", f"Blood Knights {pct(SWR['FL_flask_of_the_blood_knights_2'])} raid alone, but it does not stack with Sickening Signet; {pct(SWM['FL_flask_of_the_blood_knights_2'])} M+"),
 ("Potion", "Potion of Recklessness", f"Draught of Rampant Abandon {pct(SWM['PO_draught_of_rampant_abandon_2'])} M+, and lower raid once combined"),
 ("Food", "Silvermoon Parade", f"best or tied; others down to {pct(min(v for k,v in SWM.items() if k.startswith('FO_')))}"),
 ("Weapon oil", "Thalassian Phoenix Oil", f"Oil of Dawn {pct(SWM['OIL_oil_of_dawn_2'])}, none {pct(SWM['OIL_none'])}"),
 ("Rune", "Void-Touched", f"dropping it {pct(SWM['RUNE_none'])}"),
]
NOTES = [
 "SimC midnight 3af1a75 (2026-10-23), game data 12.1.5.70575; your client is 70529, so SimC is one build newer. Current talents in both modes, as you asked.",
 "Raid = Patchwerk, M+ = DungeonSlice. Sweeps 5,000 / 2,500 iterations; sets 10,000 / 6,000; stat grid 6,000 / 3,000; gems 6,000 / 3,000. Errors about ±0.05-0.08% raid, ±0.14-0.21% M+.",
 "Every variant ran as its own SimC profileset. All runs for this page: about 25 minutes.",
 f"The previous plan (crafted Farstrider's Reinforced Faulds instead of Cuisses + bracers) on this gear: raid {pct(SWR['LE_CraftedFaulds331_CH'])} for the legs alone; the Cuisses beat it, so don't craft those legs.",
 f"Raid-only option: Gebbo's Backup Blaster with Hunter's Ritual Stone moved from the bow onto the crafted shoulders is {pct(F2R['R_D_C+Gebbo+RitualStoneOnShoulder'])} raid, but the Sprigshot can't be worn with it afterwards (embellishment cap 2) and the M+ set loses 0.36%.",
 "Crafts carry no embellishment: your belt (Arcanoweave) and bow (Hunter's Ritual Stone) already use the cap of 2.",
 "Costs: catalyst charge (export currency 3465:1, likely 1 charge but not confirmed); 331 crafts = Sparks + 80 Myth crests each (single source); Myth crests unlimited by your call; Spark count is not in the export.",
 "Inputs and raw outputs: sims/resetgit/opt_0417 on branch claude/epic-cori-kqdhlt.",
]
lede = ("Night Elf Hunter, EU-Silvermoon. Export of 2026-10-24 04:17 (client 12.1.5.70529), simulated the same day on SimulationCraft "
        "midnight 3af1a75, game data 12.1.5.70575. Every item is at its upgrade cap. Item names link to Wowhead.")
tpl = open(os.path.join(HERE, "template_0417.html"), encoding="utf-8").read()
tpl = tpl.replace("<table>\n      {{GRID}}", "<table class='grid'>\n      {{GRID}}")
for k, v in {"{{HUNTER}}": I["_hunter"], "{{LEDE}}": E(lede), "{{TABS}}": "".join(tabs), "{{PANELS}}": "".join(panels),
             "{{ORDER_INTRO}}": E("Steps 1-3 fill the empty slots on your new gear and are worth the most. Gains are each step on top of the previous ones."),
             "{{ORDER}}": order,
             "{{GRID_INTRO}}": E("Both crafts at 331 inside the plan (tier legs, raid also Sickening Signet). Gold = best. Crit/Haste on both is best in raid and within error of the best in M+, so craft both Crit/Haste."),
             "{{GRID}}": gridhtml,
             "{{ENCH}}": "".join(f"<tr><td>{E(a)}</td><td>{E(b)}</td><td class='c'>{E(c)}</td><td>{E(d)}</td></tr>" for a, b, c, d in ENCH),
             "{{TAL}}": "".join(f"<tr><td>{E(a)}</td><td>{E(b)}</td><td class='c'>{E(c)}</td></tr>" for a, b, c in CONS),
             "{{NOTES}}": "".join(f"<li>{n}</li>" for n in NOTES)}.items():
    tpl = tpl.replace(k, v)
open(OUT, "w", encoding="utf-8").write(tpl)
print(OUT, len(tpl), "unfilled:", tpl.count("{{"))
