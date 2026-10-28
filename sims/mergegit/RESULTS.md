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

## 2026-10-08 (fresh) — what to do with 2 sparks
Sources: Guardian export 2026-10-08 14:25; Balance profile 2026-10-07 21:24 (gear unchanged in 14:25 export);
SimC midnight 2c56391 (2026-10-08), live data 69933 = client. Costs verified today (wiki/Method/wowcarry):
armour 2 sparks, 2H 4; 331 = Q5 + 80 Myth Mistcrest (3446, player has 83). Inputs/outputs `sparks2/`.
Guardian (Patchwerk single actor, 8000 it, ±0.10 DPS / ±0.31 DTPS), crafts Haste/Vers per user:
Pikestaff+Ritual Stone (4 sparks) +3.79 / −7.38 | Belt+Adorned Fang +0.74 / −0.95 | Cover+tier gauntlets+AF +0.60 / −1.99 |
Leggings+TH+AF +0.63 / −1.20 | Belt (no emb) +0.41 / −0.42 | free Amani ring1 +0.38 / −1.93.
Balance (PW ±0.08 / DS ±0.20): Handwraps Crit/Mastery +0.74 / +0.54; Mastery/Vers +0.61 / +0.69; Haste/Vers +0.24 / +0.41.
Adorned Fang: SimC placeholder for low-health proc chance (approximate).
Conclusion: save sparks + 80 Myth crests for the Pikestaff (~5x any 2-spark craft for the bear).
If crafting now: bear = Utility Belt + Adorned Fang; Balance = Handwraps Crit/Mastery.

## 2026-10-10 — M+ consumables (fresh SimC 71a76b7, data 69933 = client)
Balance: profile 2026-10-07 21:24 (newest Balance export), DungeonSlice 6000 it (±0.19%).
Guardian: profile 2026-10-08 14:25, Patchwerk single actor 5000 it (DPS ±0.13, DTPS ±0.39). `consumables_1010/`.
Balance M+: Flask of the Magisters (others −0.6..−1.4) | Draught of Rampant Abandon +0.38 vs Light's Potential |
Harandar Celebration = Royal Roast = Impossibly Royal Roast = Silvermoon Parade | Void-Touched rune (+0.77 vs none) |
Thalassian Phoenix Oil (Oil of Dawn −0.69).
Guardian (vs Blood Knights / Light's Potential): Flask of Thalassian Resistance +0.20 DPS / −3.22 dmg taken;
Flask of the Shattered Sun +0.54 / −2.36; Draught of Rampant Abandon +0.54 / −0.33; food Harandar = Royal Roast = Parade;
rune Void-Touched (+0.65 / −1.30 vs none); oil Thalassian Phoenix Oil (Oil of Dawn −0.50 / +0.83).

## 2026-10-13 — Guardian: Bubbleband ring + Whirling Sash belt? (export 2026-10-13 18:09)
SimC midnight f762a63 (2026-10-13), live data 69933 = client. Patchwerk single actor 10000 it (DPS ±0.09, DTPS ±0.28).
Profile fixed: Slitherscale = Champion 6/6 308 (not 321). Inputs `guardian_1013/`.
| Change | DPS | Dmg taken |
| Bubbleband (Haste/Vers) for Sickening Signet | −0.03 | −1.67 |
| Whirling Sash (Haste/Mastery) for Slitherscale | +0.52 | +0.70 |
| both | +0.50 | −1.07 |
| Amani Warlord ring1 instead | +0.37 | −2.22 |
| Subjugator's Grips for Miststalker's Grips | +0.22 | −1.55 |
| Twin-Strike Polearm 321 | +0.21 | −1.10 |
| Amani + Subjugator + Polearm | +0.68 | −4.53 |
| Amani + Subjugator + Polearm + Sash | +1.13 | −3.91 |

## 2026-10-13 — What 12.1.5 changes for Mergegit (Druid)
Source of truth: SimC f762a63 game data diff, live 12.1.0.69933 vs PTR 12.1.5.70340 (`tools/spell_diff.py <simc> 7`).
Only 4 Druid-family spells change: Bear Form (melee-crit-taken −6% and +3% expertise removed from Bear Form),
Guardian Druid aura (those two effects added -> no net change for Guardian), Nature's Bounty (Resto 10%->15%),
Skyfire Heel (attribute flag). Balance: no spell changes.
Live-vs-ptr sims (`ptr_1215/`) are NOT valid yet: SimC's PTR mode uses a different Balance APL (−2.4% is APL, not game)
and still reads Bear Form effect indices from the old layout (Guardian DTPS ×3.4 is a SimC artifact).

## 2026-10-14 — Guardian crafted weapon: embellishment + stats (export 2026-10-14 23:01)
SimC midnight 8bd8f32, live data 12.1.5.70391 = client. Patchwerk single actor 10000 it (DPS ±0.09, DTPS ±0.35).
Aln'hara Pikestaff 331 Q5 + Berserker's Rage vs Toxin-Coated Warstaff 321. Bear uses 1/2 embellishments (wrist).
Phase 1 (Haste/Vers): Hunter's Ritual Stone +3.69/−9.13; Sigil Void +3.27/−8.87; Pango +3.14/−8.40;
Sigil Hunt +3.50/−8.31; Prismatic Focusing Iris +4.18/−7.04; no embellishment +2.65/−6.84
(Stabilizing Gemstone Bandolier = no-emb -> not modelled). Twin-Strike Polearm 321 +0.15/−1.23.
Phase 2 stats: HRS Crit/Vers +3.78/−10.85 (best); HRS Haste/Vers +3.69/−9.13; Sigil Hunt Crit/Vers +3.67/−10.24.
Conclusion: Pikestaff + Hunter's Ritual Stone, Crit/Vers.

## 2026-10-14 — Feral M+/raid gear and weapon for both specs (export Feral 2026-10-14 23:43)
SimC 8bd8f32, data 12.1.5.70391 = client. `feral_weapon_1014/`, `feral_final_1014/`, report `report/`.
Weapon (vs Toxin staff): Pikestaff HRS Mast/Crit +4.37 raid / +4.69 M+; Crit/Vers +3.88 / +4.04; Impetus ties Pikestaff;
HRS ties Sigil Hunt. Bear: Crit/Vers −10.85 dmg taken vs Mast/Crit −8.68, same DPS.
Feral owned best (Sandstone r1, Amani r2, Subjugator hands, Gebbo t2): +2.28 raid / +3.48 M+;
+ Pikestaff HRS Mast/Crit: +6.34 / +7.65. Projected BiS (murlok top-50 items: Bardiche, Vile Alchemist's Band,
Zul'jin's Guillotine, Silken Voodoo Drape, Agent's Sneakers + owned Sandstone/Subjugator): +8.34 / +9.30.
Neck: keep Aqirbane (Yoke −2.8/−3.5, Graft −1.1).
Report: https://claude.ai/artifact/Ec9Lj94rp1KYRpedec93Xb

## 2026-10-15 — Bear (priority) + cat M+ builds from owned gear with crafted weapon; projected BiS incl. Kith'ix
SimC 8bd8f32, data 12.1.5.70391. `bear_owned_1015/`, `plan_1015/`. Bear: Patchwerk single actor; cat: DungeonSlice + Patchwerk.
Weapon in full builds: Haste/Vers vs Crit/Vers — cat tie; bear −16.9% vs −18.3% dmg taken (user prefers Haste/Vers).
Bear owned (Pike HV + Miststalker's Cinch + Subjugator + Gebbo t1): +2.1% DPS / −16.9% dmg taken vs now.
Cat owned (Pike HV + Sandstone r1 + Amani r2 + Subjugator + Gebbo t2): +6.9% M+ / +5.9% raid.
Bear BiS (adds Chestwrap of Palpable Terror + tier gauntlets, Twisted Horror's Tendril, Masterwork Sin'dorei Band CV,
Apex Brute's Claw Ring): +2.5% / −22.5%. Cat BiS (Tendril, Font of Venomous Rage, Vile Alchemist's, Swarmcaller,
Silken Voodoo, Sash of the Forlorn Vessel, Chestwrap): +17.1% M+ / +9.3% raid; Bardiche loses to the Pikestaff.
Bear avoid: Lightbearer's Shield Fragment, Font, Zul'jin's, Swarmcaller, Bardiche (more dmg taken).
Report v2: https://claude.ai/artifact/Ec9Lj94rp1KYRpedec93Xb

## 2026-10-15 — Balance (export 10:59, correct talents) gear/talents + M+ consumables for Balance, cat, bear
SimC midnight 3dcabb9, data 12.1.5.70391. `opt3_1015/`. Balance DS 4000 it (±0.24) / PW 6000 (±0.10).
Balance: equipped set is already the best owned set (all swaps tie or lose; Voracious −5%, Yoke −4%, Cane −1.5%).
Talents: current = best M+ (m+ s2 ties); raid: ra s2 / Oct-7 21:24 string +1.85%; s2 ra2 −9..−11%, blitz −12..−17%.
Consumables (each spec's M+ build): Balance + cat — Flask of the Magisters, Draught of Rampant Abandon, Harandar
Celebration (Royal Roast ties), Void-Touched rune (+0.6..0.8%), Thalassian Phoenix Oil. Bear — Flask of Thalassian
Resistance (Magisters +4.4% dmg taken, Blood Knights +3.0%), Draught, Harandar (Twilight Angler's Medley −3.0% dmg taken
/ −0.7% DPS), Void-Touched, Phoenix Oil. Pikestaff simmed as crafted (Mastery/Crit).
Report v3: https://claude.ai/artifact/Ec9Lj94rp1KYRpedec93Xb

## 2026-10-21 — Guardian: Band of the Swarmcaller + crafted belt/gloves/cloak (export 17:31 tank loadout)
SimC 1210-01 midnight 7bc1071 (build string 2c56391), data 12.1.5.70448 (= client). Pull model: 5 heroic tank dummies all
attacking (CLAUDE.md s5), single actor, 5000 it (DPS ±0.10, DTPS ±0.40). Inputs `bear_1021/craft/`.
| Variant (vs tank loadout) | DPS | Dmg taken | Max HP |
|---|---|---|---|
| Swarmcaller 334 ring1 (Alacrity, Quick Lapis) | +0.51 | +4.42 | +4.6% (1.022M -> 1.069M) |
| Crafted belt 331 Haste/Vers + Hunter's Ritual Stone | +1.60 | -4.45 | |
| Swarmcaller + that belt | +2.13 | -0.72 | +5.4% |
| Swarmcaller + crafted gloves H/V Ritual Stone | +2.13 | -0.58 | |
| Swarmcaller + belt H/V without embellishment | +1.00 | +2.04 | |
| Swarmcaller + crafted cloak (Courtly Cloak) C/V | +1.90 | +0.16 | |
Swarmcaller loses Haste/Vers for Mastery: less Ironfur/rage, less Vers DR -> more damage taken, but mastery raises max HP,
which DTPS does not count. Embellished belt is the real gain; only legal with the Bardiche (Pikestaff + wrist = 2 already).

## 2026-10-22 — Balance raid/M+ + Guardian M+ options and a shared both-spec set (exports 2026-10-21 17:19 / 17:31)
SimC midnight 7bc1071, data 12.1.5.70448 (= client, hotfix 2026-10-20). Inputs/outputs: `bal_1021/`, `bear_1021/`, `final_1021/`.
Report: `report_1021/` -> https://claude.ai/artifact/G4GbjqV1SXKVQbARPvh3RU
- Balance raid (Patchwerk ±0.10): Swarmcaller 334 ring1 +1.11; + Fevered Defense hands + Masterful Peridot +1.23; same on Raider.IO talents +1.22.
  Talents: current = Raider.IO (tie); ra s2 -0.80; m+ s2 -2.21.
- Balance M+ (DungeonSlice ±0.25): m+ s2 talents +2.66 (talent run +2.95); + Swarmcaller +4.31; + Masterful Peridot + Shroud +4.30.
- Guardian M+ (pull model, ±0.40 taken): current talents best (m+ s2 +33% taken, others +150-450%).
  Craft belt H/V Ritual Stone -4.45 taken / +1.60 dealt; + Swarmcaller -0.72 / +2.13; Pikestaff -1.79 / -0.21.
- Shared set F1 (Swarmcaller + Ritual Binder, Eyes of the Eagle, Quick Lapis, Agi kit, Cinch; trinkets/weapons per spec):
  Balance raid -1.30, Balance M+ +2.31 (with m+ s2), bear +1.04 dealt / +5.33 taken. Trinkets and leg kit cannot be shared
  (Keeper's on Balance -5.7..-7%; Vile Vial on bear +10..15% taken; Agi kit costs Balance ~1.2%, Int kit costs bear 7-9% taken).

## 2026-10-28 — Guardian bear: belt/gloves/chest/cloak/rings, PROVISIONAL baseline (no 10-28 export was supplied)
SimC midnight 710c240, data 12.1.5.70575 (hotfix 2026-10-28). Baseline = `char_guardian_2026-10-28.simc` = 10-21 17:31 tank export
+ chest Lunar Raiment 334 redirect 281236 + Bardiche 341 (user-stated); everything else UNVERIFIED vs the real 10-28 gear.
Single actor Patchwerk 5000 it; pull = 5 heroic dummies attacking (taken ±0.4), boss = 1 default dummy (±0.55). Inputs/outputs `bear_1028/`
(`gen.py`, `gen2.py`, `run.sh`, `parse.py`, `table.txt` = full table). Sanity copy 0.00.
- Ritual Stone is the belt: stone -2.0..-4.7% taken vs no stone -0.7..-2.2% (pull). Best pairs Crit/Vers, Haste/Vers (tie, ±0.4); Crit/Haste -4.2 pull / -3.4 boss but best dealt.
- Crafted gloves equal the belt for the same stats (both can't carry the stone: cap 2 with wrist Arcanoweave).
- Miststalker's Grips 321 = tie with Subjugator's (-0.3 ±0.4). Grips/cloak at 334 are NOT verified to exist (Hero track caps 321): -2.3 / -1.8% if they did.
- Enchant 8730 (Eye of the Lynx) on the worn gloves has zero effect in SimC; its in-game value is unmodelled.
- Chest: redirect 281236 and 334 each matter (old 239048@321 = +4.9% taken, -1.1% dealt vs baseline).
- Rings: Bubbleband + Ritual Binder best taken; Swarmcaller pairs +3.5..+4.3% taken, +4.6% max HP, +0.8..+1.0% dealt.
- Best attainable (321): Crit/Vers belt + stone, nothing else changed = -4.7 pull / -4.8 boss; with Grips+Pall 321 no better.
- 2026-10-28 follow-up (user: Hunter's Ritual Stone cannot go on a belt, only Arcanoweave): the 'stone' belt rows above are NOT achievable;
  use the Arcanoweave rows (`bear_1028/gen3.py`, `E*`): belt + Arcanoweave on top of the wrist's = Crit/Vers -4.45 pull / -4.78 boss taken
  (+1.30 dealt), Haste/Vers -4.30 / -3.41, Crit/Haste -4.05 / -3.53 -- same as the stone (-4.7/-4.8). SimC counts the 2nd Arcanoweave; game
  duplicate rule UNVERIFIED. Moving the Arcanoweave from wrist to belt = no gain (belt no-emb -1.97/-1.71). Wrist Arcanoweave alone is worth
  +2.2% taken / -0.8% dealt on the bear.
  Balance (`bal_1028/`, export 10-21, raid current talents / M+ 'm+ s2'): Lantern stone worth -1.27% raid / -1.29% M+ if removed; wrist Arcanoweave
  -1.10 / -0.97; crafted Arcanoweave belt (Crit/Mastery or Haste/Mastery) with the Lantern's stone dropped = +0.14 / +0.30 (tie). Wearing
  all three (wrist, belt, Lantern stone) = +1.2..+1.5% but is 3 embellishments (cap 2).
- 2026-10-28 (user: 2 Arcanoweaves allowed; belt per spec): Balance layouts, 6 belt pairs (`bal_1028/gen2.py`, raid 10000 it ±0.10 / M+ 'm+ s2' 6000 it ±0.24),
  vs baseline = wrist Arcanoweave + Lantern stone + old belt (Whirling Dervish Sash) = 0.00:
  W (belt+wrist Arc, Lantern recrafted plain): raid -0.20..+0.09, M+ -0.07..+0.17 (tie).
  C (belt Arc + Lantern stone, wrist without Arc): raid best Haste/Mastery +0.47, Crit/Haste +0.31; M+ best Crit/Haste +0.61, Haste/Mastery +0.46.
  Bear belt + wrist Arcanoweave (`bear_1028`, extra pairs): Mastery/Vers -3.3 pull / -2.7 boss, Haste/Mastery -2.8 / -1.4 (CV -4.5/-4.8, HV -4.3/-3.4, CH -4.1/-3.5).
  Per-spec belts: Balance keeps old belt + wrist Arc + Lantern stone (baseline), bear wears the crafted Arcanoweave belt + wrist Arc: both at 2 embellishments.
