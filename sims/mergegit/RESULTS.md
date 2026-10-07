# Mergegit results log

## 2026-10-07 — Jan'thrazet + Aln'hara Lantern vs Aln'hara Cane
SimC 1210-01, WoW 12.1.0.69933 (hotfix 2026-10-07), no-networking. Profile: `char_2026-10-07.simc`
(build_profile.py, all gear at cap). Inputs: `lantern_variants.simc`, `run_lantern_*.simc`.
Dagger enchant 8689 copied from the staff; Hunter's Ritual Stone (13771) moved to the lantern.
Lantern 331 q5: +295 Int, 50/50 of the two crafted stats.

| Variant (dagger ilvl, lantern stats) | Patchwerk ±0.05% | DungeonSlice ±0.16% |
|---|---|---|
| D337 Crit/Mastery | +1.73% | +1.79% |
| D337 Haste/Mastery | +1.40% | +1.53% |
| D334 Crit/Mastery | +1.18% | +1.30% |
| D334 Crit/Vers | +1.06% | +1.31% |
| D334 Mastery/Vers | +1.09% | +1.28% |
| D334 Haste/Mastery | +0.90% | +1.07% |
| D334 Crit/Haste | +0.84% | +1.03% |
| D334 Haste/Vers | +0.83% | +1.10% |
| D328 Crit/Mastery | +0.21% | +0.36% |
| Staff 331 (baseline) | 0 | 0 |
| SANITY | +0.01% | +0.05% |

Conclusion: dagger+lantern beats the staff from 334 up. Best lantern pair: Crit/Mastery
(+0.28% raid / +0.23% M+ over Mastery/Haste). Dagger 334->337: +0.55% raid / +0.49% M+.

Note: the user's crafted lantern line (`bonus_id=...8791..., crafted_stats=49/36`) resolves in SimC
as Crit/Mastery because bonus 8791 is a type-25 stat setter (32/49) and wins over crafted_stats
(`check_lantern.simc`). Confirm the real stats from the in-game tooltip.
