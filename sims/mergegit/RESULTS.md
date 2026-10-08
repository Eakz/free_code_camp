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

## 2026-10-07 — Best owned M+/raid set, enchants, talents, buffs, dungeon chase (21:24 export)
Profile `char_2026-10-07_2124.simc` (all gear at cap; crafted stats from `crafted_stats=`).
Inputs/outputs: `topgear/`, `dungeons/`, `consumables/`, `final/`. Queue: `run_queue.sh <simc>`.
Phase runs 4000 it PW (±0.12%) / 3000 DS (±0.26%); final 15000 PW (±0.06%) / 8000 DS (±0.16%).

- Owned gear: nothing in bags beats the equipped set (all swaps tie or lose). Spiritcudgel 334 −1.05/−1.72%,
  Aln'hara Cane −1.71/−2.28%, Graft vs Yoke tie/−1.14% (M+).
- Talents: 21:24 active = best; ra s2 ties; m+ s2 −2.0/−0.9%; old 20:59 active and blitz −13..−16%.
- Enchants: current set is best or tied in every slot. Rings Eyes of the Eagle beat every alternative by 1.3–1.8%.
- Buffs: Draught of Rampant Abandon > Light's Potential (+0.51% PW / +0.35% DS final run).
  Flask of the Magisters, Harandar Celebration (Silvermoon Parade/Royal Roast tie), Void-Touched rune (+0.7/+1.1%),
  Thalassian Phoenix Oil (Oil of Dawn −0.5/−0.65%).
- Dungeon chase (vs current + Draught), final run:
  raid: Pendant of Malefic Fury (Murder Row) +0.51%, + Desiccator's Blessed Gloves (Kings' Rest) +0.16% more.
  M+: nothing beats current beyond error. No dungeon trinket or weapon beats current gear.

## 2026-10-07 — Guardian: which dungeons to farm (M+ S2, Hero 321)
Profile `char_guardian_2026-10-07.simc`: shared gear from the 21:24 export, Toxin-Coated Warstaff 321,
tier legs with Agi kit 8159, talents "m+ dps" (from the 2026-09-16 Guardian export), Guardian consumables.
Patchwerk, one actor per run, 6000 it (DPS ±0.12%, DTPS ±0.37%). `guardian/runs`, `guardian/combo`, `tools/parse_tank.py`.
Ranked by damage taken (negative = better), DPS second.

| Dungeon | Item (slot) | DPS | Dmg taken |
|---|---|---|---|
| Den of Nalorakk | Pilfered Precious Band (ring) | +0.01 | −3.68 |
| Blinding Vale | Branch of Pride (staff) | +0.04 | −2.40 |
| Blinding Vale | Rootwalker Harness (waist) | +0.05 | −2.12 |
| Ruby Life Pools | Crown of Roaring Storms (head, + tier gauntlets) | +0.08 | −1.96 |
| Temple of Sethraliss | Twin-Strike Polearm (2H) | +0.22 | −1.28 |
| Kings' Rest | Primal Dinomancer's Belt (waist) | +0.12 | −1.29 |
| Temple of Sethraliss | Hood of the Slithering Loa (head, + tier gauntlets) | +0.35 | −0.75 |
Owned now: Band of the Amani Warlord (bags, 315→321) ring2 + Ritual Binder's Ring ring1: +0.49 DPS / −3.04 dmg taken.
Combos: owned rings + Pilfered + Polearm + Dinomancer + Hood: +0.84 / −8.53.
Avoid: Tumor of the Swarm (+0.55 DPS but +6.1% dmg taken), all other dungeon trinkets lose DPS and survivability.

## 2026-10-08 — Guardian stat values (why Crit shows up)
Same Guardian profile, Patchwerk, single actor, 10000 it (DPS ±0.09%, DTPS ±0.3%). `guardian/stats`, `guardian/stats_out`.
+600 rating injected: Vers −21.5% dmg taken / +9.3% DPS; Crit −18.2% / +9.8%; Haste −12.7% / +8.9%; Mastery −10.0% / +8.3%.
Real item check (crafted wrist 331, all 6 pairs): Crit/Vers = Crit/Haste = Haste/Vers (within error); Mastery pairs +1.1..+1.7% dmg taken.
Caveat: Patchwerk = one physical melee hitter on a dummy; no magic damage, no pulls. Talents = "m+ dps" (Elune's Chosen).

## 2026-10-08 — 2 sparks: craft for Guardian or Balance? (Guardian 14:25 export, Balance 21:24 profile)
Crafts 331 q5 Haste/Vers (user's assumption). Guardian: Patchwerk single actor 8000 it (DPS ±0.10, DTPS ±0.31).
Balance: Patchwerk 8000 (±0.08) / DungeonSlice 5000 (±0.21). Inputs `sparks/`.
| Craft | Bear DPS | Bear dmg taken | Balance raid | Balance M+ |
|---|---|---|---|---|
| Aln'hara Pikestaff + Hunter's Ritual Stone | +3.79 | −7.38 | n/a | n/a |
| Aln'hara Pikestaff, no embellishment | +2.75 | −5.28 | n/a | n/a |
| Pikestaff+RS + Silvermoon Agent's Utility Belt | +4.31 | −8.11 | +0.07 | +0.18 |
| Pikestaff+RS + Silvermoon Agent's Handwraps | +3.93 | −7.49 | +0.32 | +0.32 |
| Agent's Leggings + tier gauntlets (enchant conflict: Agi kit vs Int thread) | +0.32 | −0.50 | +0.38 | +0.61 |
| Agent's Sneakers (vs Breakwater 334) | −0.06 | +0.11 | −0.19 | −0.09 |
Free: Band of the Amani Warlord ring1 on bear +0.38 / −1.93.
~~Conclusion: spark 1 = Pikestaff, spark 2 = belt~~ WRONG: assumed 1 spark per craft. Corrected 2026-10-08:
2H costs 4 sparks, armour 2; the player has 2 sparks = exactly one armour craft now.
Corrected conclusion: hold the 2 sparks and craft the Pikestaff + Ritual Stone at 4 sparks (+3.8% DPS / −7.4% dmg taken),
because spending 2 now on the best single armour craft (≤ +0.4%) delays the Pikestaff from ~2 to ~4 weeks.
If crafting now: bear-first = Utility Belt (+0.41 / −0.42) or Agent's Cover + tier gauntlets (+0.23 / −1.59);
Balance-first = Handwraps (+0.32 raid / +0.32 M+; bear +0.13 / 0).
