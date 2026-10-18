#!/usr/bin/env python3
"""Build the Resetgit BM Hunter gear report (one self-contained HTML, icons embedded as data URIs).

    python3 build_report.py <icon_dir> <out.html>

Every number comes from sims/resetgit (opt_1018 singles, final_1018 combos), SimC midnight 5537d88,
game data 12.1.5.70448. Icons are generic WoW slot icons (Gethe/wow-ui-textures), not per-item icons."""
import base64, html, os, sys
ICON_DIR, OUT = sys.argv[1], sys.argv[2]

def ic(n):
    with open(os.path.join(ICON_DIR, n + ".png"), "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()

SLOT_ICON = {"Head": "INV_Helmet_25", "Neck": "INV_Jewelry_Necklace_07", "Shoulder": "INV_Shoulder_29",
             "Back": "INV_Misc_Cape_18", "Chest": "INV_Chest_Chain_10", "Wrist": "INV_Bracer_13",
             "Hands": "INV_Gauntlets_29", "Waist": "INV_Belt_29", "Legs": "INV_Pants_Mail_15",
             "Feet": "INV_Boots_Chain_05", "Ring 1": "INV_Jewelry_Ring_14", "Ring 2": "INV_Jewelry_Ring_36",
             "Trinket 1": "INV_Trinket_80_Titan02a", "Trinket 2": "INV_Misc_Gem_Variety_01",
             "Weapon": "INV_Weapon_Bow_07"}
GEM_ICON = {"Indecipherable Eversong Diamond": "INV_Misc_Gem_Diamond_07",
            "Powerful Eversong Diamond": "INV_Misc_Gem_Diamond_07",
            "Flawless Deadly Amethyst": "INV_Misc_Gem_Amethyst_01"}
I = {k: ic(v) for k, v in {**SLOT_ICON, **GEM_ICON}.items()}
I["_ench"] = ic("INV_Enchant_EssenceMagicLarge")
I["_hunter"] = ic("Ability_Hunter_BeastCall")
I["_coin"] = ic("INV_Misc_Coin_17")

WH = "https://www.wowhead.com/item={}"
SLOTS_L = ["Head", "Neck", "Shoulder", "Back", "Chest", "Wrist", "Hands", "Waist"]
SLOTS_R = ["Legs", "Feet", "Ring 1", "Ring 2", "Trinket 1", "Trinket 2", "Weapon"]

# slot: (name, item_id, ilvl, track/upgrade note, source, enchant, [gems], stats, gain note, changed)
def it(name, iid, ilvl, track, src, ench="", gems=(), stats="", note="", changed=False):
    return dict(name=name, id=iid, ilvl=ilvl, track=track, src=src, ench=ench, gems=list(gems), stats=stats,
                note=note, changed=changed)

NOW = {
 "Head": it("Skulking Viper's Weeping Fangs", 271492, 334, "Tier · Myth 6/6", "Worn", "Empowered Rune of Avoidance", stats="Haste / Mastery"),
 "Neck": it("Flowform Choker", 171720, 321, "Hero 6/6", "Worn", gems=["Powerful Eversong Diamond"], stats="Haste / Mastery"),
 "Shoulder": it("Jaws of the Skulking Viper", 271490, 308, "Tier · Champion 6/6", "Worn", stats="Crit / Haste"),
 "Back": it("Speakeasy Shroud", 251132, 321, "Hero 6/6", "Worn"),
 "Chest": it("Skulking Viper's Scuteplate", 271495, 321, "Tier · Hero 6/6", "Worn", "Mark of the Worldsoul", stats="Haste / Mastery"),
 "Wrist": it("Galerider's Mesh Wraps", 272254, 308, "Champion 6/6", "Worn"),
 "Hands": it("Skulking Viper's Hidepiercers", 271493, 334, "Tier · Myth, now 321 → 334 = 4 steps, 80 Myth crests (you have 25)", "Worn"),
 "Waist": it("Farstrider's Trophy Belt", 244581, 331, "Crafted Q5 · Arcanoweave embellishment", "Worn", stats="Vers / Mastery"),
 "Legs": it("Galerider's Chausses", 272251, 308, "Champion 6/6", "Worn", "+Agility kit (8161)", stats="Haste / Vers"),
 "Feet": it("Galerider's Footguards", 272248, 321, "Hero 6/6", "Worn", "Lynx's Dexterity", stats="Crit / Mastery"),
 "Ring 1": it("Hex Loop", 272149, 321, "Hero 6/6", "Worn", "Eyes of the Eagle", ["Flawless Deadly Amethyst"], "Crit / Mastery"),
 "Ring 2": it("Sickening Signet of Atroxus", 252258, 321, "Hero 6/6", "Worn", "Eyes of the Eagle", ["Flawless Deadly Amethyst"], "Haste / Mastery"),
 "Trinket 1": it("Freightrunner's Flask", 250215, 321, "Hero 6/6", "Worn"),
 "Trinket 2": it("Resonant Bellowstone", 250228, 321, "Hero 6/6", "Worn"),
 "Weapon": it("Aln'hara Sprigshot", 265337, 331, "Crafted Q5 · Hunter's Ritual Stone", "Worn", "Rite of the Hash'ey", stats="Crit / Mastery"),
}
def swap(base, **ch):
    d = dict(base)
    for k, v in ch.items():
        d[k.replace("_", " ")] = v
    return d

FREE = swap(NOW,
  Legs=it("Galerider's Chausses", 272251, 308, "Champion 6/6", "Worn", "+Agility & Armor kit (8163)", stats="Haste / Vers", note="+0.47% M+ · +0.49% raid", changed=True),
  Neck=it("Flowform Choker", 171720, 321, "Hero 6/6", "Worn", gems=["Indecipherable Eversong Diamond"], stats="Haste / Mastery", note="+0.13% M+ · +0.14% raid", changed=True))
DUNG = swap(FREE,
  Legs=it("Skulking Viper's Coiled Legwraps", 271491, 321, "Tier · catalyse Galerider's Chausses or a 321 legs drop", "Catalyst", "+Agility & Armor kit (8163)", stats="Haste / Mastery", note="frees the tier shoulder slot", changed=True),
  Shoulder=it("Spaulders of Prime Emperor", 239049, 321, "Hero 6/6", "Kings' Rest", stats="Crit / Haste", note="+1.16% M+ · +1.27% raid (with tier legs)", changed=True),
  Wrist=it("Arc-Glass Bindings", 159380, 321, "Hero 6/6", "Temple of Sethraliss", stats="Crit / Haste", note="+0.40% M+ · +0.43% raid", changed=True),
  Trinket_2=it("Lightspire Core", 250214, 321, "Hero 6/6", "The Blinding Vale", note="+0.51% M+", changed=True))
BIS = swap(DUNG,
  Legs=it("Skulking Viper's Coiled Legwraps", 271491, 334, "Tier · Myth 6/6", "Sszorak (legs token)", "+Agility & Armor kit (8163)", stats="Haste / Mastery", note="tier at 334", changed=True),
  Chest=it("Skulking Viper's Scuteplate", 271495, 334, "Tier · Myth 6/6", "Vashnik (chest token)", "Mark of the Worldsoul", stats="Haste / Mastery", note="tier at 334", changed=True),
  Feet=it("Boots of the Reckless Wayfarer", 268258, 334, "Myth 6/6", "The Lost Explorers*", "Lynx's Dexterity", stats="Crit / Mastery", note="+0.64% M+ · +0.74% raid", changed=True),
  Back=it("Amani Summoning Shawl", 268248, 334, "Myth 6/6", "Nek'zali", stats="Crit / Vers", note="+0.40% M+ · +0.54% raid", changed=True),
  Ring_1=it("Vile Alchemist's Band", 268249, 334, "Myth 6/6", "Vashnik the Malignant", "Eyes of the Eagle", ["Flawless Deadly Amethyst"], "Crit / Mastery", "+0.38% M+ · +0.36% raid", True),
  Trinket_1=it("Voracious Heart of Ula'tek", 270175, 334, "Myth 6/6", "Ula'tek", stats="Crit (on use)", note="+2.00% M+ · +1.46% raid", changed=True),
  Trinket_2=it("Twisted Horror's Tendril", 281215, 334, "Myth 6/6", "Kith'ix", note="+4.02% M+ · +2.18% raid", changed=True))

SETS = [
 ("now", "Today", NOW, "0.00%", "0.00%", "Your worn gear, every piece at its track cap. This is the 0% line for every number on this page."),
 ("free", "Free fixes", FREE, "+0.72%", "+0.67%", "Swap the leg kit and the neck diamond. No drops, no crests."),
 ("dung", "Dungeon set", DUNG, "+2.80%", "+2.57%", "Free fixes, plus three dungeon drops at 321 and tier legs from the catalyst. Without the catalyst, take Lithiel's Linked Leggings (Murder Row), keep the tier shoulders and skip Kings' Rest: +2.50% M+, +2.08% raid."),
 ("bis", "Projected BiS", BIS, "+11.64%", "+9.02%", "The dungeon set plus raid and Great Vault pieces at Myth 334. Simmed as one set; the gain on each item is that item alone."),
]

FARM = [  # dungeon, item, id, slot, M+, raid, condition
 ("Kings' Rest", "Spaulders of Prime Emperor", 239049, "Shoulder", "+1.16", "+1.27", "needs tier legs to keep 4-piece"),
 ("Altar of Fangs", "Chestguard of Corroded Scales", 273789, "Chest", "+0.99", "+0.63", "needs tier legs; competes with Kings' Rest for the tier slot"),
 ("Murder Row", "Lithiel's Linked Leggings", 251141, "Legs", "+0.68", "+0.70", "best legs if you do not catalyse"),
 ("Murder Row", "Jangling Felpaulets", 251131, "Shoulder", "+0.57", "+0.71", "needs tier legs"),
 ("The Blinding Vale", "Ironroot Collar", 251184, "Shoulder", "+0.64", "+1.14", "needs tier legs; best raid shoulder from dungeons"),
 ("The Blinding Vale", "Lightspire Core", 250214, "Trinket", "+0.51", "–", "M+ only"),
 ("Temple of Sethraliss", "Legguards of the Awakening Brood", 159375, "Legs", "+0.50", "+0.59", "if you do not catalyse"),
 ("Temple of Sethraliss", "Arc-Glass Bindings", 159380, "Wrist", "+0.40", "+0.43", "no conditions"),
 ("Voidscar Arena", "Manipulator's Vest", 251233, "Chest", "+0.30", "+0.51", "needs tier legs"),
]

# Bonus roll targets (Nebulous Voidcore). Gains are single-swap sims at 334, M+ / raid.
ROLL = [
 ("1", "The Coiled Altar", "Zul'jin's Guillotine Technique (+1.21 / +2.33), Cuisses of the Uncoiled Union (+1.52 / +1.61), Silken Voodoo Drape (+0.19 / +0.38)",
  "Two strong upgrades on one boss, good in both M+ and raid. Sources put this boss's Mythic loot at 344."),
 ("2", "Entombed Sentinels", "Keeper's Seething Core (+0.82 / +2.03), Crown of the Eternal Fang (+1.11 / +1.06, boss disputed: Nek'zali or Sentinels), hands token",
  "Best raid trinket after the Guillotine."),
 ("3", "Vashnik the Malignant", "Vashnik's Sanguine Rancor (+0.78 / +1.06), Vile Alchemist's Band (+0.38 / +0.36), chest tier token",
  "Three useful items, all small."),
 ("4", "Sszorak", "Tier legs token (+1.02 / +1.06)",
  "One item, but it frees the shoulder slot for a dungeon shoulder."),
 ("–", "Kith'ix", "Twisted Horror's Tendril (+4.02 / +2.18), Band of the Swarmcaller (0.00 / +0.72)",
  "The biggest single upgrade on the page. Not verified that Voidcores work in this raid; if they do, roll here before anything above."),
]
SKIP = "Skip: The Lost Explorers (boots +0.64 / +0.74, nothing else), Nek'zali (shawl +0.40 / +0.54), The Twin Fangs (nothing that gains)."

ENCH = [  # slot, pick, runner-up, note
 ("Legs", "+Agility & Armor kit (8163)", "+Agility & Stamina kit, +0.45%", "+0.47% M+, change it"),
 ("Neck gem", "Indecipherable Eversong Diamond", "Stoic −0.09%, Telluric −0.19%", "+0.13% M+, change it"),
 ("Rings", "Eyes of the Eagle", "every other ring enchant −1.0 to −1.4%", "keep"),
 ("Ring gems", "Flawless Deadly Amethyst", "all other Flawless gems tie or lose (to −0.26%)", "keep"),
 ("Weapon", "Rite of the Hash'ey", "scopes −0.3 to −1.4%", "keep"),
 ("Chest", "Mark of the Worldsoul", "Mark of the Rootwarden −0.40%", "keep"),
 ("Feet", "Lynx's Dexterity", "others tie (−0.04 to −0.06%)", "keep"),
 ("Head", "Empowered Rune of Avoidance", "others tie", "keep"),
 ("Shoulder", "any", "all within error", "no DPS value"),
]
TAL = [
 ("M+", "Your current build", "Best in DungeonSlice. Raider.IO raid build is −26% here."),
 ("Raid single target", "Raider.IO raid build", "+5.34% over your build. The 'solos' build is +1.77%."),
]

E = html.escape
def gem_html(g):
    return f'<span class="gem-w"><img class="gem" src="{I[g]}" alt="">{E(g)}</span>'
def item_html(slot, x):
    cls = "item changed" if x["changed"] else "item"
    ench = f'<div class="ench"><img src="{I["_ench"]}" alt="">{E(x["ench"])}</div>' if x["ench"] else ""
    gems = f'<div class="gems">{"".join(gem_html(g) for g in x["gems"])}</div>' if x["gems"] else ""
    note = f'<div class="gain">{E(x["note"])}</div>' if x["note"] else ""
    src = "" if x["src"] == "Worn" else f' · <span class="src">{E(x["src"])}</span>'
    stats = f' · {E(x["stats"])}' if x["stats"] else ""
    return (f'<div class="{cls}"><div class="ic"><img src="{I[slot]}" alt=""><span class="ilvl">{x["ilvl"]}</span></div>'
            f'<div class="meta"><div class="slot">{slot}</div>'
            f'<a class="name" href="{WH.format(x["id"])}" target="_blank" rel="noopener">{E(x["name"])}</a>'
            f'<div class="sub">{E(x["track"])}{src}{stats}</div>{ench}{gems}{note}</div></div>')

tabs, panels = [], []
for k, label, gear, mp, rd, desc in SETS:
    tabs.append(f'<button class="tab" role="tab" data-k="{k}" id="t-{k}" aria-controls="p-{k}">{E(label)}'
                f'<span class="chip">{mp}</span></button>')
    L = "".join(item_html(s, gear[s]) for s in SLOTS_L)
    R = "".join(item_html(s, gear[s]) for s in SLOTS_R)
    panels.append(f'<div class="panel" id="p-{k}" role="tabpanel" aria-labelledby="t-{k}">'
                  f'<div class="ph"><div><h3>{E(label)}</h3><p>{E(desc)}</p></div>'
                  f'<div class="nums"><div><b>{mp}</b><span>M+ ±0.23%</span></div><div><b>{rd}</b><span>Raid ±0.04%</span></div></div></div>'
                  f'<div class="doll"><div class="col">{L}</div><div class="col">{R}</div></div></div>')

def link(n, i): return f'<a href="{WH.format(i)}" target="_blank" rel="noopener">{E(n)}</a>'
farm = "".join(f"<tr><td>{E(d)}</td><td>{link(n,i)}</td><td>{E(s)}</td><td class='g'>{m}</td><td class='g'>{r}</td><td class='c'>{E(c)}</td></tr>"
               for d, n, i, s, m, r, c in FARM)
roll = "".join(f'<div class="roll"><span class="rank">{E(n)}</span><div><h4>{E(b)}</h4><p class="loot">{E(l)}</p><p>{E(w)}</p></div></div>'
               for n, b, l, w in ROLL)
ench = "".join(f"<tr><td>{E(a)}</td><td>{E(b)}</td><td class='c'>{E(c)}</td><td>{E(d)}</td></tr>" for a, b, c, d in ENCH)
tal = "".join(f"<tr><td>{E(a)}</td><td>{E(b)}</td><td class='c'>{E(c)}</td></tr>" for a, b, c in TAL)

tpl = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "template.html"), encoding="utf-8").read()
out = (tpl.replace("{{HUNTER}}", I["_hunter"]).replace("{{COIN}}", I["_coin"]).replace("{{TABS}}", "".join(tabs))
          .replace("{{PANELS}}", "".join(panels)).replace("{{FARM}}", farm).replace("{{ROLL}}", roll)
          .replace("{{SKIP}}", E(SKIP)).replace("{{ENCH}}", ench).replace("{{TAL}}", tal))
open(OUT, "w", encoding="utf-8").write(out)
print(OUT, len(out))
