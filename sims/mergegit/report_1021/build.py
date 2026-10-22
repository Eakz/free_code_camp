#!/usr/bin/env python3
"""Build the Mergegit 2026-10-22 report (self-contained HTML, icons as data URIs).

    python3 build.py <icon_dir> <out.html>

Numbers come from bal_1021/ (talents, gear sweeps), bear_1021/ (talents, gear, craft) and final_1021/ (set combinations).
SimC midnight 7bc1071, data 12.1.5.70448. Icons are generic WoW icons (Gethe/wow-ui-textures), not per-item icons."""
import base64, html, os, sys
ICON_DIR, OUT = sys.argv[1], sys.argv[2]
def ic(n):
    with open(os.path.join(ICON_DIR, n + ".png"), "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()
I = {k: ic(v) for k, v in {
    "moon": "Spell_Nature_StarFall", "bear": "Ability_Racial_BearForm", "both": "Spell_Nature_ForceOfNature",
    "ring": "INV_Jewelry_Ring_88", "ring2": "INV_Jewelry_Ring_36", "hands": "INV_Gauntlets_25", "belt": "INV_Belt_15",
    "back": "INV_Misc_Cape_18", "gem": "INV_Misc_Gem_Variety_01", "talent": "Ability_Druid_Eclipse", "legs": "INV_Pants_Leather_09",
    "weapon": "INV_Spear_04", "trinket": "INV_Trinket_80_Titan02a", "ench": "INV_Enchant_EssenceMagicLarge",
    "neck": "INV_Jewelry_Necklace_07"}.items()}
E = html.escape
WH = "https://www.wowhead.com/item={}"

def row(icon, name, iid, detail, gain=""):
    nm = f'<a href="{WH.format(iid)}" target="_blank" rel="noopener"><b>{E(name)}</b></a>' if iid else f"<b>{E(name)}</b>"
    g = f" <em>{E(gain)}</em>" if gain else ""
    return f'<div class="row"><img src="{I[icon]}" alt=""><div class="t">{nm} <span>· {E(detail)}</span>{g}</div></div>'

def num(v, label, good_low=False):
    if v is None: return ""
    cls = "eq" if abs(v) < 0.005 else (("up" if v < 0 else "dn") if good_low else ("up" if v > 0 else "dn"))
    return f'<div><b class="{cls}">{v:+.2f}%</b><span>{E(label)}</span></div>'

SWARM = ("ring", "Band of the Swarmcaller", 281029, "ring 1 · Myth 6/6 334 (needs 100 Myth crests)")
# Options per mode: (rank, title, why, [rows], nums[(value,label,good_low)], kind)
MODES = [
 ("braid", "Balance · Raid", "moon", "Patchwerk, current talents. Error ±0.10%.", [
  ("1", "Swarmcaller + Fevered Defense + Masterful Peridot", "Best raid set. The two extras are inside the error bar, so the ring does the work.",
   [row(*SWARM, gain="+1.11% alone"), row("hands", "Gauntlets of Fevered Defense", 251124, "hands · Hero 321", "+0.22% alone"),
    row("gem", "Flawless Masterful Peridot", 0, "both rings + neck socket", "+0.19% alone")],
   [(1.23, "Raid", False)], "top"),
  ("2", "Swarmcaller only", "Same result inside the error bar with one change. Keep Eyes of the Eagle and your gems.",
   [row(*SWARM)], [(1.11, "Raid", False)], ""),
  ("3", "Option 1 on the Raider.IO talents", "Raider.IO loadout ties your current one in raid (+0.02%), so either works.",
   [row("talent", "Raider.IO Build", 0, "talent loadout")], [(1.22, "Raid", False)], ""),
  ("◆", "Both specs: shared set", "The shared set below, on Balance. The Agility leg kit is what costs Balance here.",
   [row("both", "Shared set (see Guardian tab)", 0, "Swarmcaller + Ritual Binder · Eyes of the Eagle · Agility kit · Cinch")],
   [(-1.30, "Raid", False)], "both"),
 ]),
 ("bmp", "Balance · M+", "moon", "DungeonSlice. Error ±0.25%. Gains include the talent swap.", [
  ("1", "m+ s2 talents + Swarmcaller", "The talent swap is +2.66% on its own and free. The ring adds the rest.",
   [row("talent", "m+ s2", 0, "saved loadout", "+2.66% alone"), row(*SWARM)], [(4.31, "M+", False)], "top"),
  ("2", "Option 1 + Masterful Peridot + Miststalker's Shroud", "Ties option 1. The extras are each under 0.25%.",
   [row("talent", "m+ s2", 0, "saved loadout"), row(*SWARM), row("gem", "Flawless Masterful Peridot", 0, "rings + neck"),
    row("back", "Miststalker's Shroud", 272226, "back · Hero 321")], [(4.30, "M+", False)], ""),
  ("3", "m+ s2 talents only", "Free right now: no crests, no gear.",
   [row("talent", "m+ s2", 0, "saved loadout")], [(2.66, "M+", False)], ""),
  ("◆", "Both specs: shared set", "Shared set on m+ s2 talents. It gives back about 2% of option 1.",
   [row("both", "Shared set (see Guardian tab)", 0, "Swarmcaller + Ritual Binder · Eyes of the Eagle · Agility kit · Cinch")],
   [(2.31, "M+", False)], "both"),
 ]),
 ("gmp", "Guardian · M+", "bear", "Five heroic mobs all attacking. Ranked by damage taken (lower is better). Error ±0.40% taken, ±0.10% dealt.", [
  ("1", "Crafted belt: Haste/Vers + Hunter's Ritual Stone", "Biggest defensive gain. Only legal with the Bardiche (Pikestaff + wrist already use both embellishment slots).",
   [row("belt", "Silvermoon Agent's Utility Belt", 244573, "waist · crafted 331 · Haste/Vers · Hunter's Ritual Stone")],
   [(-4.45, "Taken", True), (1.60, "Dealt", False)], "top"),
  ("2", "Crafted belt + Swarmcaller", "Most damage. Swarmcaller trades haste and Vers for mastery: more damage taken, but +4.6% max health that this metric does not count.",
   [row("belt", "Silvermoon Agent's Utility Belt", 244573, "Haste/Vers · Ritual Stone"), row(*SWARM)],
   [(-0.72, "Taken", True), (2.13, "Dealt", False)], ""),
  ("3", "Aln'hara Pikestaff instead of the Bardiche", "Best you can do today without crafting or crests.",
   [row("weapon", "Aln'hara Pikestaff", 245771, "main hand · crafted 331 · as crafted")],
   [(-1.79, "Taken", True), (-0.21, "Dealt", False)], ""),
  ("◆", "Both specs: shared set", "One set of armour, rings and leg kit for both specs; trinkets and weapons stay per spec. Bear is the main, so the leg kit is Agility.",
   [row("ring", "Band of the Swarmcaller", 281029, "ring 1 · 334 · Eyes of the Eagle · Quick Lapis"),
    row("ring2", "Ritual Binder's Ring", 159459, "ring 2 · 321 · Eyes of the Eagle · Quick Lapis"),
    row("belt", "Miststalker's Cinch", 272245, "waist · 321"),
    row("legs", "Agility & Stamina leg kit", 0, "on the tier legs"),
    row("trinket", "Trinkets per spec", 0, "Balance: Vile Vial + Gebbo · Bear: Gebbo + Keeper's")],
   [(5.33, "Taken", True), (1.04, "Dealt", False)], "both"),
 ]),
]
tabs, panels = [], []
for k, label, icon, intro, opts in MODES:
    tabs.append(f'<button class="tab" role="tab" data-k="{k}" id="t-{k}" aria-controls="p-{k}"><img src="{I[icon]}" alt="">{E(label)}</button>')
    cards = []
    for rank, title, why, rows, nums, kind in opts:
        cards.append(f'<div class="opt {kind}"><div class="seal">{rank}</div><div class="ob"><h3>{E(title)}</h3><p class="why">{E(why)}</p>'
                     f'<div class="chg">{"".join(rows)}</div></div><div class="nums">{"".join(num(*n) for n in nums)}</div></div>')
    panels.append(f'<div class="panel" id="p-{k}" role="tabpanel" aria-labelledby="t-{k}"><p class="intro">{E(intro)}</p>'
                  f'<div class="opts">{"".join(cards)}</div></div>')

TODO = [
 ("m", "Balance, now", "Use the m+ s2 talents in M+ (+2.66%). In raid keep your current talents or Raider.IO (tie)."),
 ("m", "Balance, with crests", "Upgrade Band of the Swarmcaller to 334 and wear it in ring 1: +1.1% raid, +1.4% M+."),
 ("g", "Guardian, now", "Your current talents take the least damage by far. Swap the Bardiche for the Pikestaff if you want −1.8% damage taken today."),
 ("g", "Guardian, next week", "Craft the Haste/Vers belt with Hunter's Ritual Stone and keep the Bardiche: −4.5% damage taken, +1.6% damage."),
 ("x", "One set for both", "Possible, but it costs Balance 1.3% in raid and the bear 5% more damage taken. Keeping separate rings and leg kits is better: you already own both sets."),
]
todo = "".join(f'<div class="{c}"><b>{E(t)}</b><p>{E(p)}</p></div>' for c, t, p in TODO)

CRAFT = [("Swarmcaller replacing Alluring Bubbleband", 0.51, 4.42, "+4.6%"),
         ("Crafted belt Haste/Vers + Ritual Stone", 1.60, -4.45, ""),
         ("Swarmcaller + that belt", 2.13, -0.72, "+5.4%"),
         ("Swarmcaller + crafted gloves Haste/Vers + Ritual Stone", 2.13, -0.58, ""),
         ("Swarmcaller + crafted cloak Crit/Vers + Ritual Stone", 1.90, 0.16, ""),
         ("Swarmcaller + belt Haste/Vers, no embellishment", 1.00, 2.04, "")]
def td(v, low=False):
    cls = ("up" if (v < 0) == low else "dn") if abs(v) >= 0.005 else ""
    return f'<td class="n {cls}">{v:+.2f}%</td>'
craft = "".join(f"<tr{' class=best' if i == 1 else ''}><td>{E(n)}</td>{td(d)}{td(t, True)}<td class='n'>{E(h)}</td></tr>"
                for i, (n, d, t, h) in enumerate(CRAFT))
COST = [("100", "Myth crests: Swarmcaller 318 → 334 (5 steps × 20)"), ("80 + Sparks", "Myth crests + Sparks of Tides for a 331 craft (2 per armour piece by your count)"),
        ("289", "Myth crests in your export"), ("2 of 2", "Embellishments on the bear with the belt + wrist; the Pikestaff would make 3")]
cost = "".join(f"<div><b>{E(a)}</b><span>{E(b)}</span></div>" for a, b in COST)

TB = [("Current", 0.00, 0.00), ("Raider.IO Build", 0.02, 0.09), ("ra s2", -0.80, 0.71), ("m+ s2", -2.21, 2.95), ("nymryssa", -10.45, -1.62),
      ("s2 ra2", -12.88, -5.63), ("blitz st", -13.77, -10.75), ("blitz aoe", -15.58, -14.29), ("delves", -9.26, -15.60)]
tal_b = "".join(f"<tr{' class=best' if n in ('Current','m+ s2') else ''}><td>{E(n)}</td>{td(r)}{td(m)}</tr>" for n, r, m in TB)
TG = [("Current = m+ dps", 0, 0, 0), ("m+ s2", 33.02, 26.75, -5.62), ("m+ doc", 162.40, 175.50, 0.71), ("m+ hd", 152.49, 172.88, -8.09),
      ("m+ hs", 206.07, 191.01, -12.50), ("m+ strem", 247.98, 269.56, -15.64), ("delves", 451.71, 357.48, 9.47)]
tal_g = "".join(f"<tr{' class=best' if i == 0 else ''}><td>{E(n)}</td>{td(p, True)}{td(b, True)}{td(d)}</tr>" for i, (n, p, b, d) in enumerate(TG))

NOTES = [
 "SimC midnight 7bc1071 (2026-10-20), game data 12.1.5.70448 with the 2026-10-20 hotfixes, the same build as your client.",
 "Balance raid: Patchwerk, 3,000-6,000 iterations (±0.10%). Balance M+: DungeonSlice, 2,000-4,000 iterations (±0.25-0.36%). Treat M+ differences under 0.5% as ties.",
 "Guardian: one bear per run. Pull = five heroic-strength mobs that all attack (≈144k/s incoming, ≈113k/s absorbed, ≈30k/s taken on a 1.0M health bear); boss = one Mythic-strength dummy. SimC's 5-target setting has only one attacker, which made your Ursoc's Fury absorbs cover everything, so it was not used.",
 "The pull strength is a stand-in for a hard key; the exact number is an assumption. Damage taken does not count max health, so mastery-heavy changes like Swarmcaller look worse than they are.",
 "Every item is at its upgrade cap (Hero 321, Myth 334, crafted 331). Bag items were tested with enchants and gems copied from the slot they replace; enchants and gems were also swept separately.",
 "Not shareable: trinkets (Keeper's Seething Core has no Intellect, Balance −5.7 to −7%; Vile Vial costs the bear +10-15% damage taken) and the leg kit (Agility kit costs Balance ≈1.2%, Intellect kit costs the bear 7-9% damage taken).",
 "The bear baseline is your 17:31 tank loadout (Bardiche, Bubbleband + Ritual Binder, Gebbo + Keeper's, Cinch). Balance baseline is the 17:19 export.",
 'Crest costs: 20 per upgrade step (<a href="https://www.icy-veins.com/wow/news/these-five-mistcrests-decide-how-fast-your-gear-climbs-in-midnight-season-2/">Icy Veins</a>); 80 Myth crests + 2-4 Sparks per 331 craft (<a href="https://expcarry.com/wow-midnight-season-2-crafting-guide">expcarry</a>, single source). Your Spark count is not in the export.',
 "Inputs and raw outputs: sims/mergegit/bal_1021, bear_1021, final_1021 on branch claude/epic-cori-kqdhlt.",
]
notes = "".join(f"<li>{n}</li>" for n in NOTES)

tpl = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "template.html"), encoding="utf-8").read()
for k, v in {"{{I_MOON}}": I["moon"], "{{I_BEAR}}": I["bear"], "{{I_RING}}": I["ring"], "{{TODO}}": todo, "{{TABS}}": "".join(tabs),
             "{{PANELS}}": "".join(panels), "{{CRAFT}}": craft, "{{COST}}": cost, "{{TAL_B}}": tal_b, "{{TAL_G}}": tal_g, "{{NOTES}}": notes}.items():
    tpl = tpl.replace(k, v)
open(OUT, "w", encoding="utf-8").write(tpl)
print(OUT, len(tpl), "unfilled:", tpl.count("{{"))
