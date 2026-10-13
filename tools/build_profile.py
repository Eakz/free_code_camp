#!/usr/bin/env python3
"""Turn a SimC addon export into a sim-ready profile with every item at its track cap.

Profiles are NEVER hand-written. Hand-writing them is how items end up simmed at the
item level they happen to be sitting at, which silently invalidates every comparison
built on top. Run this, read the printed table, then sim.

    python3 tools/build_profile.py export.txt > char.simc

The table it prints is part of the deliverable: if a slot shows RAW != CAP and you did
not intend that, the profile is wrong and no result from it can be reported.
"""
import re, sys

SLOTS = ['head','neck','shoulder','back','chest','wrist','hands','waist','legs','feet',
         'finger1','finger2','trinket1','trinket2','main_hand','off_hand']

# Midnight Season 2. Update deliberately, with a source, never by guessing.
DUNGEON_CAP = 321   # M+ / Hero track. Dungeons do not drop Mythic.
CRAFTED_CAP = 331   # crafted PvE, proven by the worn crafted wrist and staff

# Bonus ids of type 25 (crafted stat setters). In SimC they override crafted_stats=, but they
# never match the player's real stat choice (5 of 5 crafted items in Mergegit's export disagree,
# e.g. lantern 8791=Crit/Mastery vs chosen crafted_stats=49/36). crafted_stats= is the truth:
# strip these whenever crafted_stats= is present.
CRAFTED_STAT_BONUS = {6647, 6648, 6649, 6650, 6673, 6674, 6675, 8790, 8791, 8792, 8793, 8794,
                      8795, 8862, 8948, 8949, 8950, 8951, 8952, 8953, 8954, 8955, 8956, 8957,
                      11136, 11137, 11138, 11139, 11313}

def strip_stat_bonus(rest):
    if 'crafted_stats=' not in rest:
        return rest
    def fix(m):
        ids = [b for b in m.group(1).split('/') if int(b) not in CRAFTED_STAT_BONUS]
        return 'bonus_id=' + '/'.join(ids)
    return re.sub(r'bonus_id=([0-9/]+)', fix, rest)

# Upgrade-track step bonus ids -> (track, 6/6 cap). S2 caps verified 2026-10-13 (Method, Icy Veins):
# Champion 292-308, Hero 305-321, Myth 318-334. Re-verify every season/patch.
TRACKS = [(range(12833, 12841), 'Champion', 308),
          (range(12841, 12849), 'Hero', 321),
          (range(12849, 12857), 'Myth', 334)]

def track_of(line):
    m = re.search(r'bonus_id=([0-9/]+)', line)
    ids = {int(b) for b in m.group(1).split('/')} if m else set()
    for rng, name, cap in TRACKS:
        if ids & set(rng):
            return name, cap
    return None, None

def cap_for(line, raw, name=''):
    """Return (cap, why). Never invent an item level a source cannot produce."""
    if 'crafting_quality=' in line:
        return CRAFTED_CAP, 'crafted PvE'
    if re.search(r"Competitor|Gladiator|Aspirant|Combatant", name + line):
        return raw, 'PvP - does not scale in PvE'
    track, cap = track_of(line)
    if track:
        return max(cap, raw), f'{track} track 6/6'
    if raw > DUNGEON_CAP:
        return raw, 'no track id, above Hero cap - leave alone'
    return DUNGEON_CAP, 'no track id - assumed Hero/dungeon'

def main(path):
    txt = open(path, encoding='utf-8', errors='replace').read()
    head, _, bags = txt.partition('### Gear from Bags')
    out, rows = [], []
    pending_ilvl = None
    for line in head.splitlines():
        s = line.strip()
        m = re.match(r'^#\s*(.+?)\s*\((\d+)\)\s*$', s)
        if m:
            pending_ilvl = (m.group(1), int(m.group(2))); continue
        m = re.match(r'^(\w+)=(.*)$', s)
        if not m:
            if s.startswith('#') or not s: continue
            out.append(s); continue
        slot, rest = m.group(1), m.group(2)
        if slot not in SLOTS:
            out.append(s); continue
        if pending_ilvl is None:
            sys.exit(f"ERROR: {slot} has no '# Name (ilvl)' comment above it - cannot "
                     f"establish its item level. Fix the export, do not guess.")
        name, raw = pending_ilvl; pending_ilvl = None
        cap, why = cap_for(s, raw, name)
        rest = re.sub(r',?\s*ilevel=\d+', '', rest)
        rest = re.sub(r',?\s*content_tuning=\d+', '', rest)
        rest = strip_stat_bonus(rest)
        out.append(f"{slot}={rest.rstrip(',')},ilevel={cap}" if rest.strip(',') else f"{slot}=,ilevel={cap}")
        rows.append((slot, name, raw, cap, why))
    if not rows:
        sys.exit('ERROR: no equipped item lines found - is this a SimC addon export?')
    w = max(len(r[1]) for r in rows)
    print("# SLOT        RAW -> CAP   ITEM", file=sys.stderr)
    for slot, name, raw, cap, why in rows:
        flag = '  <-- UPGRADE' if cap != raw else ''
        print(f"# {slot:<11s} {raw:>3d} -> {cap:>3d}   {name:<{w}s}  ({why}){flag}", file=sys.stderr)
    print("\n".join(out))

if __name__ == '__main__':
    if len(sys.argv) != 2: sys.exit(__doc__)
    main(sys.argv[1])
