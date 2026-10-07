#!/usr/bin/env python3
"""Look items up in SimC's item DB by exact name, name substring, or id.

    python3 tools/lookup.py <simc_dir> "Speakeasy Shroud" 251194 "~Ophidian"

A leading "~" means substring match. Prints id, inventory type, class/subclass and stats.
inv: 1 head 2 neck 3 shoulder 5 chest 6 waist 7 legs 8 feet 9 wrist 10 hands 11 finger
     12 trinket 13 1H 16 back 17 2H 20 robe 23 off-hand.  class 4 subclass 2 = leather.
"""
import re, sys

STAT = {3: 'Agi', 4: 'Str', 5: 'Int', 7: 'Sta', 32: 'Crit', 36: 'Haste', 40: 'Vers', 49: 'Mastery',
        71: 'StrAgiInt', 72: 'StrAgi', 73: 'AgiInt', 74: 'StrInt'}
ITEM = re.compile(r'^\s*\{ "(.*?)",\s*(\d+), [^,]+, [^,]+, [^,]+, (\d+), (\d+), \d+, \d+, (\d+), (\d+), (\d+), (\d+), '
                  r'\d+, \d+, [^,]+, [^,]+, &__item_stats_data\[(\d+)\], (\d+),')

def load(simc):
    path = f"{simc}/engine/dbc/generated/item_data.inc"
    stats, items = [], []
    with open(path, encoding='utf-8', errors='replace') as f:
        for line in f:
            m = ITEM.match(line)
            if m:
                items.append(m.groups())
                continue
            s = re.match(r'^\s*\{\s*(\d+),\s*(-?\d+), [^}]+\},?$', line)
            if s and not items:
                stats.append((int(s.group(1)), int(s.group(2))))
    return items, stats

def fmt(it, stats):
    name, iid, ilvl, req, qual, inv, cls, sub, idx, n = it
    st = [stats[int(idx) + i] for i in range(int(n))]
    sec = '/'.join(STAT.get(t, str(t)) for t, _ in st if t in (32, 36, 40, 49))
    prim = '/'.join(STAT.get(t, str(t)) for t, _ in st if t in (3, 4, 5, 71, 72, 73, 74))
    return f"{iid:>7s}  inv={inv:<3s} class={cls}/{sub:<3s} q={qual} ilvl={ilvl:<4s} {prim:<10s} {sec:<14s} {name}"

def main(simc, queries):
    items, stats = load(simc)
    for q in queries:
        if q.isdigit():
            hits = [i for i in items if i[1] == q]
        elif q.startswith('~'):
            hits = [i for i in items if q[1:].lower() in i[0].lower()]
        else:
            hits = [i for i in items if i[0].lower() == q.lower()]
        if not hits:
            print(f"   NOT FOUND  {q}")
        for h in hits:
            print(fmt(h, stats))

if __name__ == '__main__':
    if len(sys.argv) < 3: sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2:])
