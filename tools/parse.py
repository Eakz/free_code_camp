#!/usr/bin/env python3
"""Rank actors in a SimC text output against the A_ baseline.

    python3 tools/parse.py out.txt

Prints DPS, error and % vs the actor whose name starts with "A_".
"""
import re, sys

def main(path):
    txt = open(path, encoding='utf-8', errors='replace').read()
    rows = []
    for m in re.finditer(r'^Player: (\S+) .*?\n(.*?)(?=^Player: |\Z)', txt, re.S | re.M):
        name, body = m.group(1), m.group(2)
        d = re.search(r'DPS=([0-9.]+) DPS-Error=([0-9.]+)/([0-9.]+)%', body)
        if d:
            rows.append((name, float(d.group(1)), float(d.group(3))))
    if not rows:
        sys.exit('no DPS lines found')
    base = next((r for r in rows if r[0].startswith('A_')), rows[0])
    rows.sort(key=lambda r: -r[1])
    print(f"{'actor':<28s} {'DPS':>10s} {'err%':>6s} {'vs ' + base[0]:>12s}")
    for n, dps, err in rows:
        print(f"{n:<28s} {dps:>10.0f} {err:>6.2f} {100 * (dps / base[1] - 1):>+11.2f}%")

if __name__ == '__main__':
    if len(sys.argv) != 2: sys.exit(__doc__)
    main(sys.argv[1])
