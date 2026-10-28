#!/usr/bin/env python3
"""Rank bear single-actor runs (out_pull/, out_boss/): % vs A_base for damage taken, damage dealt, max health.
    python3 parse.py [prefix]"""
import glob, os, re, sys
def read(p):
    t = open(p, errors="replace").read()
    d = re.search(r"DPS=([0-9.]+) DPS-Error=[0-9.]+/([0-9.]+)%", t); k = re.search(r"DTPS=([0-9.]+) DTPS-Error=[0-9.]+/([0-9.]+)%", t)
    h = re.search(r"health=(\d+)\|(\d+)", t)
    return None if not (d and k and h) else (float(d[1]), float(d[2]), float(k[1]), float(k[2]), int(h[2]))
pre = sys.argv[1] if len(sys.argv) > 1 else ""
R = {m: {os.path.basename(p)[:-4]: read(p) for p in glob.glob(f"out_{m}/*.txt")} for m in ("pull", "boss")}
names = sorted(set(R["pull"]) | set(R["boss"]))
b = {m: R[m].get("A_base") for m in R}
print(f"{'variant':<34s} | {'PULL taken':>10s} {'±':>5s} {'dealt':>7s} {'maxHP':>7s} | {'BOSS taken':>10s} {'±':>5s} {'dealt':>7s}")
rows = []
for n in names:
    if not n.startswith(pre) and n not in ("A_base", "Z_SANITY"): continue
    cells = []
    for m in ("pull", "boss"):
        r = R[m].get(n)
        if not r or not b[m]: cells.append(None); continue
        cells.append((100 * (r[2] / b[m][2] - 1), r[3], 100 * (r[0] / b[m][0] - 1), 100 * (r[4] / b[m][4] - 1)))
    rows.append((n, cells))
rows.sort(key=lambda x: (x[1][0][0] if x[1][0] else 999))
for n, (p, bo) in rows:
    ps = f"{p[0]:>+9.2f}% {p[1]:>5.2f} {p[2]:>+6.2f}% {p[3]:>+6.2f}%" if p else " " * 31
    bs = f"{bo[0]:>+9.2f}% {bo[1]:>5.2f} {bo[2]:>+6.2f}%" if bo else ""
    print(f"{n:<34s} | {ps} | {bs}")
