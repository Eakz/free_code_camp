#!/usr/bin/env python3
"""Generate M+ S2 dungeon-loot variants at 321 vs the 2026-10-07 21:24 profile (rerun after talent change).
Rules (CLAUDE.md s3): candidates at 321, enchant/gem copied from the slot they replace."""
ENCH = {'head': 8017, 'shoulder': 8001, 'chest': 7987, 'legs': 7935, 'feet': 7963,
        'finger1': 7967, 'finger2': 7967, 'main_hand': 8689}
GEM = {'neck': 240983, 'finger1': 240900, 'finger2': 240907}
TIER_HANDS = "hands=,id=271529,ilevel=321"   # Enigmatic Dreamwatcher's Gauntlets from bags, keeps 4pc
C = {  # slot: [(name, id, dungeon)]
 'neck': [("Strand of Warding Fangs",273781,"Altar"),("Pendant of Malefic Fury",251142,"MurderRow"),("Graft of the Domanaar",251234,"Voidscar")],
 'back': [("Speakeasy Shroud",251132,"MurderRow"),("Bloodthorn Burnous",251190,"BlindingVale"),("Fireproof Drape",193763,"RubyLife"),("Cloak of the Restless Tribes",159288,"KingsRest")],
 'wrist': [("Fury-fletched Armlets",251135,"MurderRow"),("Rootwarden Wraps",251183,"BlindingVale"),("Kula's Butchering Wristwraps",159300,"KingsRest")],
 'hands': [("Gauntlets of Fevered Defense",251124,"MurderRow"),("Desiccator's Blessed Gloves",159312,"KingsRest"),("Grips of Electrified Defense",159337,"Sethraliss")],
 'waist': [("Rootwalker Harness",251189,"BlindingVale"),("Gravitic Girdle",251235,"Voidscar"),("Primal Dinomancer's Belt",159301,"KingsRest")],
 'feet': [("Arctic Explorer's Legwraps",251153,"Nalorakk"),("Goldfeather Boots",159304,"KingsRest"),("Sand-Shined Snakeskin Sandals",159327,"Sethraliss")],
 'ring': [("Signet of Snarling Servitude",251136,"MurderRow"),("Pilfered Precious Band",251148,"Nalorakk"),("Lightwarden's Bind",251194,"BlindingVale"),
          ("Jade Ophidian Band",162544,"Sethraliss"),("Ritual Binder's Ring",159459,"KingsRest"),("Band of the Amani Warlord",273792,"Altar")],
 'trinket': [("Knot of Writhing Serpents",273794,"Altar"),("Freightrunner's Flask",250215,"MurderRow"),("Lightspire Core",250214,"BlindingVale"),
             ("Sapling of the Dawnroot",250259,"BlindingVale"),("Mindpiercer's Sigil",250224,"Voidscar"),("Ruby Whelp Shell",193757,"RubyLife"),
             ("Sethraliss' Defiled Relic",158368,"Sethraliss")],
 'head': [("Spare Speaker's Hood",273791,"Altar"),("Vilefiend's Guise",251140,"MurderRow"),("Crown of Roaring Storms",193751,"RubyLife"),("Hood of the Slithering Loa",239033,"Sethraliss")],
 'shoulder': [("Snakeskin Spaulders",273774,"Altar"),("Scavenger's Spaulders",251146,"Nalorakk"),("Somber Spaulders",251223,"Voidscar")],
 'chest': [("War Trial Vestments",251159,"Nalorakk"),("Hide of Pestilence",251226,"Voidscar"),("Vest of Reverent Adoration",239048,"KingsRest"),("Invader's Firestorm Chestguard",193764,"RubyLife")],
 'legs': [("Breeches of Deft Deals",251130,"MurderRow"),("Lightspore Leggings",251198,"BlindingVale"),("Breeches of the Sacred Hall",159313,"KingsRest"),("Leggings of the Galeforce Viper",159329,"Sethraliss")],
 'off_hand': [("Nocuous Focal Fang",273779,"Altar"),("Perennial Frostbound Charm",271681,"Nalorakk"),("Luminescent Sprout",251191,"BlindingVale"),("Kokia's Burnout Rod",193766,"RubyLife"),("Vessel of Last Rites",159667,"KingsRest")],
 'main_hand': [("Polished Lightwood Channeler",273778,"Altar"),("Fang of Contagion",251225,"Voidscar"),("Gilded Serpent's Tooth",159137,"KingsRest"),("Galvanized Stormcrusher",158369,"Sethraliss")],
 'staff': [("Nibbles' Training Rod",251123,"MurderRow"),("Fallen Speaker's Staff",251156,"Nalorakk"),("Chillworn's Infusion Staff",193761,"RubyLife"),("Staff of the Lightning Serpent",159636,"Sethraliss")],
}
TIER = {'head', 'shoulder', 'chest', 'legs'}
def line(slot, iid):
    s = f"{slot}=,id={iid},ilevel=321"
    if slot in ENCH: s += f",enchant_id={ENCH[slot]}"
    if slot in GEM: s += f",gem_id={GEM[slot]}"
    return s
def tag(n): return ''.join(ch for ch in n.title() if ch.isalnum())[:22]
groups = {}
for slot, items in C.items():
    out = []
    for name, iid, dg in items:
        if slot == 'ring':
            for f in ('finger1', 'finger2'):
                out.append((f"{f[-1]}R_{tag(name)}_{dg}", [line(f, iid)]))
        elif slot == 'trinket':
            for t in ('trinket1', 'trinket2'):
                out.append((f"{t[-1]}T_{tag(name)}_{dg}", [line(t, iid)]))
        elif slot == 'staff':
            out.append((f"ST_{tag(name)}_{dg}", [line('main_hand', iid), "off_hand="]))
        elif slot in TIER:
            out.append((f"{slot[:2].upper()}_{tag(name)}_{dg}", [line(slot, iid), TIER_HANDS]))
        else:
            out.append((f"{slot[:2].upper()}_{tag(name)}_{dg}", [line(slot, iid)]))
    if slot in TIER:
        groups.setdefault('tier', []).extend(out)
    else:
        key = {'neck':'jewel','ring':'jewel','back':'armor','wrist':'armor','hands':'armor','waist':'armor','feet':'armor',
               'trinket':'trinket','off_hand':'weapon','main_hand':'weapon','staff':'weapon'}[slot]
        groups.setdefault(key, []).extend(out)
groups['tier'].insert(0, ("REF_TierHandsOnly", [TIER_HANDS]))
for g, vs in groups.items():
    L = ["name=A_current", "copy=Z_SANITY,A_current", "trinket2=,id=270164,bonus_id=42/13334/12854,ilevel=334"]
    for n, lines in vs:
        L += [f"copy={n},A_current"] + lines
    open(f"{g}_variants.simc", "w").write("\n".join(L) + "\n")
    for fs, it in (("Patchwerk", 6000), ("DungeonSlice", 4000)):
        open(f"run_{g}_{fs}.simc", "w").write(
            f"threads=4\niterations={it}\ndeterministic=1\nfight_style={fs}\ndesired_targets=1\n"
            f"input=../char_2026-10-07_2124.simc\ninput={g}_variants.simc\n")
    print(g, len(vs))
