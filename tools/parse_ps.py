#!/usr/bin/env python3
"""Rank SimC profileset results from a json2 file against the baseline actor.

    python3 tools/parse_ps.py out.json [prefix]

Error column = combined 95% interval of baseline and profileset (sqrt(e_b^2 + e_p^2) / baseline, SimC mean_error).
Optional prefix filters profileset names (e.g. GEM_)."""
import json, math, signal, sys
signal.signal(signal.SIGPIPE, signal.SIG_DFL)

def main(path, prefix=""):
    d = json.load(open(path))
    base = d["sim"]["players"][0]["collected_data"]["dps"]
    b, be = base["mean"], 2 * base["mean_std_dev"]
    rows = [("A_baseline", b, be)]
    for r in d["sim"]["profilesets"]["results"]:
        if r["name"].startswith(prefix):
            rows.append((r["name"], r["mean"], r["mean_error"]))
    rows.sort(key=lambda x: -x[1])
    print(f"{'profileset':<44s} {'DPS':>9s} {'vs base':>8s} {'±':>5s}")
    for n, m, e in rows:
        err = 100 * math.sqrt(be ** 2 + e ** 2) / b if n != "A_baseline" else 100 * be / b
        print(f"{n:<44s} {m:>9.0f} {100 * (m / b - 1):>+7.2f}% {err:>5.2f}")

if __name__ == "__main__":
    if len(sys.argv) < 2: sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "")
