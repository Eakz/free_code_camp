#!/usr/bin/env python3
"""Diff a class's spells between SimC's live and PTR game data.

    python3 tools/spell_diff.py <simc_dir> 7      # 7 = Druid spell family

Prints every spell of that family whose spell row or effect rows differ between
sc_spell_data.inc (live) and sc_spell_data_ptr.inc (PTR), with old -> new fields.
Effect fields shown: [3] type, [4] subtype, [8] sp/ap coefficient, [11] base value-ish.
"""
import re, sys

SPELL = re.compile(r'^\s*\{ "(.*?)"\s*,\s*(\d+),(.*)$')
EFF = re.compile(r'^\s*\{\s*(\d+),\s*(\d+),(.*)$')

def load(path):
    spells, effects, mode = {}, {}, None
    for line in open(path, encoding='utf-8', errors='replace'):
        if 'spell_data_t __' in line and 'effect' not in line:
            mode = 's'; continue
        if 'spelleffect_data_t __' in line:
            mode = 'e'; continue
        if mode == 's':
            m = SPELL.match(line)
            if m:
                fam = re.search(r'\}, \{ [^}]*\}, (\d+), \{', line)
                spells[int(m.group(2))] = (m.group(1), int(fam.group(1)) if fam else -1, line.strip())
        elif mode == 'e':
            m = EFF.match(line)
            if m:
                effects.setdefault(int(m.group(2)), {})[int(m.group(1))] = line.strip()
        if mode == 'e' and line.startswith('};'):
            break
    return spells, effects

def fields(line):
    return [f.strip() for f in re.sub(r'[{}]', '', line).split(',')]

def main(simc, family):
    g = f"{simc}/engine/dbc/generated/"
    ls, le = load(g + "sc_spell_data.inc")
    ps, pe = load(g + "sc_spell_data_ptr.inc")
    ids = sorted({i for i, v in ps.items() if v[1] == family} | {i for i, v in ls.items() if v[1] == family})
    for sid in ids:
        a, b = ls.get(sid), ps.get(sid)
        name = (b or a)[0]
        if a is None:
            print(f"NEW      {sid:>8} {name}"); continue
        if b is None:
            print(f"REMOVED  {sid:>8} {name}"); continue
        out = []
        if a[2] != b[2]:
            fa, fb = fields(a[2]), fields(b[2])
            diffs = [f"s[{i}] {x}->{y}" for i, (x, y) in enumerate(zip(fa, fb)) if x != y]
            out.append("spell: " + "; ".join(diffs[:6]))
        ea, eb = le.get(sid, {}), pe.get(sid, {})
        for eid in sorted(set(ea) | set(eb)):
            x, y = ea.get(eid), eb.get(eid)
            if x == y: continue
            if x is None or y is None:
                out.append(f"effect {eid} {'added' if x is None else 'removed'}"); continue
            fx, fy = fields(x), fields(y)
            diffs = [f"[{i}] {p}->{q}" for i, (p, q) in enumerate(zip(fx, fy)) if p != q]
            out.append(f"effect#{fx[2]} " + "; ".join(diffs))
        if out:
            print(f"CHANGED  {sid:>8} {name}: " + " | ".join(out))

if __name__ == '__main__':
    if len(sys.argv) != 3: sys.exit(__doc__)
    main(sys.argv[1], int(sys.argv[2]))
