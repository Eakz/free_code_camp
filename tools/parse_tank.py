#!/usr/bin/env python3
"""Rank single-actor tank runs (one SimC output file per variant) on DPS and DTPS.

    python3 tools/parse_tank.py <dir_of_out_txt>

Baseline is the file named A_*.txt. Lower DTPS is better; dDTPS is shown so that negative = less damage taken.
"""
import glob, os, re, sys

def read(path):
    t = open(path, encoding='utf-8', errors='replace').read()
    d = re.search(r'DPS=([0-9.]+) DPS-Error=[0-9.]+/([0-9.]+)%', t)
    k = re.search(r'DTPS=([0-9.]+) DTPS-Error=[0-9.]+/([0-9.]+)%', t)
    if not d or not k:
        return None
    return float(d.group(1)), float(d.group(2)), float(k.group(1)), float(k.group(2))

def main(folder):
    rows = {}
    for p in glob.glob(os.path.join(folder, '*.txt')):
        r = read(p)
        if r:
            rows[os.path.basename(p)[:-4]] = r
        else:
            print(f"NO RESULT: {p}")
    base = next(v for k, v in rows.items() if k.startswith('A_'))
    out = []
    for n, (dps, de, dt, te) in rows.items():
        out.append((n, 100 * (dps / base[0] - 1), de, 100 * (dt / base[2] - 1), te))
    out.sort(key=lambda r: -r[1])
    print(f"{'variant':<40s} {'dDPS%':>7s} {'±':>5s} {'dDTPS%':>7s} {'±':>5s}")
    for n, dd, de, dt, te in out:
        print(f"{n:<40s} {dd:>+7.2f} {de:>5.2f} {dt:>+7.2f} {te:>5.2f}")

if __name__ == '__main__':
    if len(sys.argv) != 2: sys.exit(__doc__)
    main(sys.argv[1])
