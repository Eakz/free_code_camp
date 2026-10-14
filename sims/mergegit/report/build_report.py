#!/usr/bin/env python3
"""Build the Feral/Guardian gear report (single self-contained HTML, icons embedded as data URIs).
Icons are generic WoW interface icons (Gethe/wow-ui-textures), one per slot type, not per item."""
import base64, os, sys
ICON_DIR = sys.argv[1]
OUT = sys.argv[2]
def ic(n):
    with open(os.path.join(ICON_DIR, n + ".png"), "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()
SLOT_ICON = {"Head":"INV_Helmet_25","Neck":"INV_Jewelry_Necklace_07","Shoulder":"INV_Shoulder_25","Back":"INV_Misc_Cape_18",
  "Chest":"INV_Chest_Leather_09","Wrist":"INV_Bracer_07","Hands":"INV_Gauntlets_25","Waist":"INV_Belt_25","Legs":"INV_Pants_Leather_09",
  "Feet":"INV_Boots_Chain_05","Ring 1":"INV_Jewelry_Ring_14","Ring 2":"INV_Jewelry_Ring_36","Trinket 1":"INV_Trinket_80_Titan02a",
  "Trinket 2":"INV_Misc_Gem_Variety_01","Weapon":"INV_Weapon_Halberd_02"}
GEM_ICON = {"Indecipherable Eversong Diamond":"INV_Misc_Gem_Diamond_07","Flawless Quick Amethyst":"INV_Misc_Gem_Amethyst_01",
  "Flawless Quick Lapis":"INV_Misc_Gem_Sapphire_02","Flawless Masterful Garnet":"INV_Misc_Gem_Ruby_01"}
ICONS = {k: ic(v) for k, v in {**SLOT_ICON, **GEM_ICON}.items()}
ICONS["_ench"] = ic("INV_Enchant_EssenceMagicLarge")
ICONS["_cat"] = ic("Ability_Druid_CatForm"); ICONS["_bear"] = ic("Ability_Racial_BearForm")

# (slot, name, ilvl, track, enchant, gems, stats, note)
CUR = [
 ("Head","Enigmatic Dreamwatcher's Somnolent Stare",321,"Tier · Hero 6/6","Empowered Rune of Avoidance",[],"Haste / Vers",""),
 ("Neck","Aqirbane Reliquary",334,"Myth 6/6","",["Indecipherable Eversong Diamond","Flawless Quick Amethyst"],"All four",""),
 ("Shoulder","Enigmatic Dreamwatcher's Plumage",321,"Tier · Hero 6/6","Amirdrassil's Grace",[],"Crit / Mastery",""),
 ("Back","Stylish Power Cape",321,"Hero 6/6","",[],"Crit / Haste",""),
 ("Chest","Enigmatic Dreamwatcher's Lunar Raiment",321,"Tier · Hero 6/6","Mark of the Worldsoul",[],"Crit / Haste",""),
 ("Wrist","Silvermoon Agent's Deflectors",331,"Crafted Q5","Embellishment: Arcanoweave Lining",[],"Vers / Crit",""),
 ("Hands","Miststalker's Grips",321,"Hero 6/6","",[],"Haste / Vers",""),
 ("Waist","Whirling Dervish Sash",321,"Hero 6/6","",[],"Haste / Mastery",""),
 ("Legs","Enigmatic Dreamwatcher's Leggings",321,"Tier · Hero 6/6","Agility armor kit (+Agi & Stam)",[],"Crit / Haste",""),
 ("Feet","Breakwater Boots",334,"Myth 6/6","Lynx's Dexterity",[],"Haste / Vers",""),
 ("Ring 1","Alluring Bubbleband",321,"Hero 6/6","Silvermoon's Alacrity",["Flawless Quick Lapis"],"Haste / Vers",""),
 ("Ring 2","Ritual Binder's Ring",321,"Hero 6/6","Silvermoon's Alacrity",["Flawless Quick Lapis"],"Haste / Vers",""),
 ("Trinket 1","Voracious Heart of Ula'tek",334,"Myth 6/6","",[],"Crit (use)",""),
 ("Trinket 2","Keeper's Seething Core",334,"Myth 6/6","",[],"Agility",""),
 ("Weapon","Toxin-Coated Warstaff",321,"Hero 6/6","Berserker's Rage",[],"Haste / Mastery",""),
]
def swap(base, changes):
    d = {r[0]: r for r in base}
    for c in changes: d[c[0]] = c
    return [d[r[0]] for r in base]
PIKE = ("Weapon","Aln'hara Pikestaff",331,"Crafted Q5 · 4 sparks + 80 Myth crests","Berserker's Rage · Embellishment: Hunter's Ritual Stone",[],"Haste / Vers","crafted weapon")
BEAR_OWN = swap(CUR, [PIKE,
 ("Waist","Miststalker's Cinch",321,"Hero 6/6 · upgrade 305→321 (100 Hero crests)","",[],"Crit / Vers","−2.9% dmg taken alone"),
 ("Hands","Subjugator's Chilling Grips",321,"Hero 6/6","",[],"Crit / Vers","−1.7% dmg taken alone"),
 ("Trinket 1","Gebbo's Bottomless Bag",334,"Myth 6/6 · replaces Voracious Heart","",[],"Agility","−4.4% dmg taken, −1.7% DPS alone"),
])
FERAL_OWN = swap(CUR, [PIKE,
 ("Ring 1","Charged Sandstone Band",321,"Hero 6/6","Silvermoon's Alacrity",["Flawless Quick Lapis"],"Crit / Mastery","+2.5% M+ alone"),
 ("Ring 2","Band of the Amani Warlord",321,"Hero 6/6 · upgrade 315→321 (40 Hero crests)","Silvermoon's Alacrity",["Flawless Quick Lapis"],"Crit / Haste","+0.4% M+ alone"),
 ("Hands","Subjugator's Chilling Grips",321,"Hero 6/6","",[],"Crit / Vers","+0.6% M+ alone"),
 ("Trinket 2","Gebbo's Bottomless Bag",334,"Myth 6/6 · replaces Keeper's Core","",[],"Agility","+0.9% M+ alone"),
])
BEAR_BIS = swap(BEAR_OWN, [
 ("Chest","Chestwrap of Palpable Terror",334,"Myth 6/6 · Kith'ix (new raid)","Mark of the Worldsoul",[],"Crit / Haste","−3.2% dmg taken, +0.7% DPS alone"),
 ("Hands","Enigmatic Dreamwatcher's Gauntlets",321,"Tier · Hero 6/6 · owned, keeps 4pc","",[],"Tier","needed for 4pc with Chestwrap"),
 ("Trinket 1","Twisted Horror's Tendril",334,"Myth 6/6 · Kith'ix (new raid)","",[],"Agility","−6.7% dmg taken alone"),
 ("Trinket 2","Gebbo's Bottomless Bag",334,"Myth 6/6 · owned","",[],"Agility","owned"),
 ("Ring 1","Masterwork Sin'dorei Band",331,"Crafted Q5 · 2 sparks + 80 Myth crests","Silvermoon's Alacrity",[],"Crit / Vers","−4.5% dmg taken alone"),
 ("Ring 2","Apex Brute's Claw Ring",334,"Myth 6/6 · Sszorak (Venomous Abyss)","Silvermoon's Alacrity",[],"Crit / Haste","−2.4% dmg taken alone"),
])
FERAL_BIS = swap(FERAL_OWN, [
 ("Trinket 1","Twisted Horror's Tendril",334,"Myth 6/6 · Kith'ix (new raid)","",[],"Agility","+4.2% M+ over your build"),
 ("Trinket 2","Font of Venomous Rage",334,"Myth 6/6 · raid (boss not verified)","",[],"Mastery","+1.2% M+ over Gebbo"),
 ("Ring 1","Vile Alchemist's Band",334,"Myth 6/6 · Venomous Abyss","Silvermoon's Alacrity",[],"Crit / Mastery","+1.1% M+"),
 ("Ring 2","Band of the Swarmcaller",334,"Myth 6/6 · Kith'ix (new raid)","Silvermoon's Alacrity",[],"Haste / Mastery","+2.9% M+"),
 ("Back","Silken Voodoo Drape",334,"Myth 6/6 · The Coiled Altar","",[],"Haste / Mastery","+0.9% M+"),
 ("Waist","Sash of the Forlorn Vessel",334,"Myth 6/6 · raid (boss not verified)","",[],"Haste / Mastery","+0.7% M+"),
 ("Chest","Chestwrap of Palpable Terror",334,"Myth 6/6 · Kith'ix (new raid)","Mark of the Worldsoul",[],"Crit / Haste","+0.4% M+"),
 ("Hands","Enigmatic Dreamwatcher's Gauntlets",321,"Tier · owned, keeps 4pc","",[],"Tier","needed for 4pc"),
])
SETS = [
 ("now","Equipped now","Your 2026-10-14 export (same gear on bear and cat), every piece at its track cap.", CUR, None),
 ("bear","Bear · your gear","Priority build. Crafted Pikestaff plus three swaps from your bags.", BEAR_OWN, ("−16.9%","+2.1%","Damage taken","DPS")),
 ("feral","Cat · your gear","Same Pikestaff plus four swaps from your bags. Keeps Whirling Dervish Sash.", FERAL_OWN, ("+6.9%","+5.9%","Mythic+","Raid")),
 ("bearbis","Bear · projected BiS","Next targets incl. the new Kith'ix raid. Raid items at Myth 334.", BEAR_BIS, ("−22.5%","+2.5%","Damage taken","DPS")),
 ("feralbis","Cat · projected BiS","Next targets incl. the new Kith'ix raid. Raid items at Myth 334.", FERAL_BIS, ("+17.1%","+9.3%","Mythic+","Raid")),
]
WEAPON = [  # stats, cat build M+, cat build raid, bear build dps, bear build dmg taken  (whole builds vs now)
 ("Haste / Vers (your pick)", "+6.9%", "+5.9%", "+2.1%", "−16.9%"),
 ("Crit / Vers", "+6.9%", "+5.9%", "+2.2%", "−18.3%"),
]
EMB = [ # embellishment, feral raid, feral M+, bear dps, bear taken  (Haste/Vers runs)
 ("Hunter's Ritual Stone","+3.33%","+3.29%","+3.69%","−9.1%"),
 ("Darkmoon Sigil: Hunt","+3.23%","+3.35%","+3.50%","−8.3%"),
 ("Prismatic Focusing Iris","+3.42%","+2.95%","+4.18%","−7.0%"),
 ("Darkmoon Sigil: Void","+2.81%","+2.79%","+3.27%","−8.9%"),
 ("No embellishment","+2.07%","—","+2.65%","−6.8%"),
]
def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
def item(r, changed=False):
    slot, name, ilvl, track, ench, gems, stats, note = r
    g = "".join(f'<img class="gem" src="{ICONS[x]}" alt="" title="{esc(x)}"><span class="gemname">{esc(x)}</span>' for x in gems)
    e = f'<div class="ench"><img src="{ICONS["_ench"]}" alt="">{esc(ench)}</div>' if ench else ""
    n = f'<div class="gain">{esc(note)}</div>' if note and changed else ""
    return (f'<div class="item{" changed" if changed else ""}"><div class="ic"><img src="{ICONS[slot]}" alt="{esc(slot)} icon">'
            f'<span class="ilvl">{ilvl}</span></div><div class="meta"><div class="slot">{esc(slot)}</div>'
            f'<div class="name">{esc(name)}</div><div class="sub">{esc(track)} · {esc(stats)}</div>{e}'
            f'{"<div class=gems>"+g+"</div>" if g else ""}{n}</div></div>')
LEFT = ["Head","Neck","Shoulder","Back","Chest","Wrist","Weapon"]
RIGHT = ["Hands","Waist","Legs","Feet","Ring 1","Ring 2","Trinket 1","Trinket 2"]
def doll(rows):
    d = {r[0]: r for r in rows}; cur = {r[0]: r for r in CUR}
    col = lambda slots: "".join(item(d[s], d[s][1] != cur[s][1]) for s in slots)
    return f'<div class="doll"><div class="col">{col(LEFT)}</div><div class="col">{col(RIGHT)}</div></div>'
tabs = "".join(f'<button class="tab" role="tab" id="t-{k}" aria-controls="p-{k}" data-k="{k}">{esc(t)}'
               f'{f"<span class=chip>{g[0]}</span>" if g else ""}</button>' for k, t, _, _, g in SETS)
panels = ""
for k, t, desc, rows, g in SETS:
    nums = (f'<div class="nums"><div><b>{g[0]}</b><span>{g[2]}</span></div>'
            f'<div><b>{g[1]}</b><span>{g[3]}</span></div></div>') if g else '<div class="nums"><div><b>baseline</b><span>all % below are vs this set</span></div></div>'
    panels += f'<section class="panel" role="tabpanel" id="p-{k}" aria-labelledby="t-{k}"><div class="ph"><div><h3>{esc(t)}</h3><p>{esc(desc)}</p></div>{nums}</div>{doll(rows)}</section>'
def table(head, rows):
    h = "".join(f"<th>{x}</th>" for x in head)
    b = "".join("<tr>" + "".join(f"<td>{esc(c)}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="tw"><table><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'
html = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "template.html")).read()
html = (html.replace("{{TABS}}", tabs).replace("{{PANELS}}", panels)
        .replace("{{WEAPON}}", table(["Pikestaff stats, whole build vs now","Cat M+","Cat raid","Bear DPS","Bear damage taken"], WEAPON))
        .replace("{{EMB}}", table(["Embellishment (Haste/Vers)","Feral raid","Feral M+","Bear DPS","Bear damage taken"], EMB))
        .replace("{{CAT}}", ICONS["_cat"]).replace("{{BEAR}}", ICONS["_bear"]))
open(OUT, "w").write(html)
print("wrote", OUT, len(html))
