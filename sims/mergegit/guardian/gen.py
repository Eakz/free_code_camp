#!/usr/bin/env python3
"""Guardian M+ S2 dungeon sweep at 321. Tanks: Patchwerk, one actor per run (CLAUDE.md s5).
Baseline ../char_guardian_2026-10-07.simc (shared gear from the 21:24 Balance export, m+ dps talents)."""
import os
ENCH = {'head': 8017, 'shoulder': 8001, 'chest': 7987, 'legs': 8159, 'feet': 7963,
        'finger1': 7967, 'finger2': 7967, 'main_hand': 7983}
GEM = {'neck': 240983, 'finger1': 240900, 'finger2': 240907}
TH = "hands=,id=271529,ilevel=321"
C = {
 'neck': [("Strand of Warding Fangs",273781,"Altar"),("Pendant of Malefic Fury",251142,"MurderRow"),("Graft of the Domanaar",251234,"Voidscar")],
 'back': [("Speakeasy Shroud",251132,"MurderRow"),("Bloodthorn Burnous",251190,"BlindingVale"),("Fireproof Drape",193763,"RubyLife"),("Cloak of the Restless Tribes",159288,"KingsRest")],
 'wrist': [("Fury-fletched Armlets",251135,"MurderRow"),("Rootwarden Wraps",251183,"BlindingVale"),("Kula's Butchering Wristwraps",159300,"KingsRest")],
 'hands': [("Gauntlets of Fevered Defense",251124,"MurderRow"),("Desiccator's Blessed Gloves",159312,"KingsRest"),("Grips of Electrified Defense",159337,"Sethraliss")],
 'waist': [("Rootwalker Harness",251189,"BlindingVale"),("Gravitic Girdle",251235,"Voidscar"),("Primal Dinomancer's Belt",159301,"KingsRest")],
 'feet': [("Arctic Explorer's Legwraps",251153,"Nalorakk"),("Goldfeather Boots",159304,"KingsRest"),("Sand-Shined Snakeskin Sandals",159327,"Sethraliss")],
 'ring': [("Signet of Snarling Servitude",251136,"MurderRow"),("Pilfered Precious Band",251148,"Nalorakk"),("Lightwarden's Bind",251194,"BlindingVale"),
          ("Jade Ophidian Band",162544,"Sethraliss"),("Ritual Binder's Ring",159459,"KingsRest"),("Band of the Amani Warlord",273792,"Altar")],
 'trinket': [("Tattered Amani War Banner",273797,"Altar"),("Freightrunner's Flask",250215,"MurderRow"),("Manaheart's Binding Flame",250243,"MurderRow"),
             ("Resonant Bellowstone",250228,"MurderRow"),("Lightspire Core",250214,"BlindingVale"),("Sapling of the Dawnroot",250259,"BlindingVale"),
             ("Tumor of the Swarm",250245,"Voidscar"),("Void Execution Mandate",250225,"Voidscar"),("Ruby Whelp Shell",193757,"RubyLife"),
             ("Lustrous Golden Plumage",159617,"KingsRest"),("Mchimba's Ritual Bandages",159618,"KingsRest"),("Tiny Electromental in a Jar",158374,"Sethraliss")],
 'head': [("Spare Speaker's Hood",273791,"Altar"),("Vilefiend's Guise",251140,"MurderRow"),("Crown of Roaring Storms",193751,"RubyLife"),("Hood of the Slithering Loa",239033,"Sethraliss")],
 'shoulder': [("Snakeskin Spaulders",273774,"Altar"),("Scavenger's Spaulders",251146,"Nalorakk"),("Somber Spaulders",251223,"Voidscar")],
 'chest': [("War Trial Vestments",251159,"Nalorakk"),("Hide of Pestilence",251226,"Voidscar"),("Vest of Reverent Adoration",239048,"KingsRest"),("Invader's Firestorm Chestguard",193764,"RubyLife")],
 'legs': [("Breeches of Deft Deals",251130,"MurderRow"),("Lightspore Leggings",251198,"BlindingVale"),("Breeches of the Sacred Hall",159313,"KingsRest"),("Leggings of the Galeforce Viper",159329,"Sethraliss")],
 'main_hand': [("Branch of Pride",251192,"BlindingVale"),("Twin-Strike Polearm",158370,"Sethraliss")],
}
TIER = {'head', 'shoulder', 'chest', 'legs'}
def line(slot, iid):
    s = f"{slot}=,id={iid},ilevel=321"
    if slot in ENCH: s += f",enchant_id={ENCH[slot]}"
    if slot in GEM: s += f",gem_id={GEM[slot]}"
    return s
def tag(n): return ''.join(ch for ch in n.title() if ch.isalnum())[:22]
V = [("A_current", []), ("Z_SANITY", ["trinket2=,id=270164,bonus_id=42/13334/12854,ilevel=334"])]
for slot, items in C.items():
    for name, iid, dg in items:
        if slot == 'ring':
            for f in ('finger1', 'finger2'): V.append((f"{f[-1]}R_{tag(name)}_{dg}", [line(f, iid)]))
        elif slot == 'trinket':
            for t in ('trinket1', 'trinket2'): V.append((f"{t[-1]}T_{tag(name)}_{dg}", [line(t, iid)]))
        elif slot in TIER:
            V.append((f"{slot[:2].upper()}_{tag(name)}_{dg}", [line(slot, iid), TH]))
        else:
            V.append((f"{slot[:2].upper()}_{tag(name)}_{dg}", [line(slot, iid)]))
V.append(("REF_TierHandsOnly", [TH]))
os.makedirs("runs", exist_ok=True)
for n, lines in V:
    open(f"runs/{n}.simc", "w").write("threads=4\niterations=6000\ndeterministic=1\nfight_style=Patchwerk\ndesired_targets=1\n"
        "input=../../char_guardian_2026-10-07.simc\n" + f"name={n}\n" + "".join(l + "\n" for l in lines))
print(len(V))
