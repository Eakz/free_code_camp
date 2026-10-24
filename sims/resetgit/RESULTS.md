# Resetgit (BM Hunter) results

## 2026-10-18 — BiS, dungeons to farm, bag optimisation (export 2026-10-18 16:06)

SimC 1210-01, midnight git 5537d88, game data 12.1.5.70448 Live (matches client). Profile: `char_bm_2026-10-18.simc`
(build_profile.py, every slot at track cap). Patchwerk 20000 it (±0.03-0.05%), DungeonSlice 10000 it (±0.23-0.33%).
Sanity actor Z_SANITY within error in every run. Inputs: `opt_1018/*_variants.simc`, `run_*.simc`; combos in `final_1018/`.

### Combined sets (final_1018)
| Set | Changes vs now | M+ | Raid ST |
|---|---|---|---|
| F1 free | legs kit 8161->8163 (Agi + Armor), neck gem 240967->240983 Indecipherable Eversong Diamond | +0.72% | +0.67% |
| F2 dungeons, no catalyst | F1 + Lithiel's Linked Leggings 321 + Arc-Glass Bindings 321 + Lightspire Core 321 (trinket2) | +2.50% | +2.08% |
| F3 dungeons + catalysed tier legs | F1 + Skulking Viper's Coiled Legwraps 321 + Spaulders of Prime Emperor 321 + Arc-Glass + Lightspire | +2.80% | +2.57% |
| F4 projected BiS | F3 + tier legs/chest 334 + Boots of the Reckless Wayfarer + Amani Summoning Shawl + Vile Alchemist's Band + Voracious Heart of Ula'tek + Twisted Horror's Tendril (all 334) | +11.64% | +9.02% |

### Singles (opt_1018)
- Enchants: only the legs kit gains (+0.47/+0.49). Rings Eyes of the Eagle, weapon Rite of the Hash'ey, chest Worldsoul, boots Lynx's Dexterity: best or tied. Ring gems: current 240898 best or tied.
- Talents: current best in M+. Raider.IO raid build +5.34% raid ST but -26% M+; "solos" +1.77% raid.
- Bags: nothing beats worn gear in M+. Raid: Band of the Amani Warlord ring1 +0.34%, Yoke +0.17%.
- Dungeon drops at 321 (M+ / raid): Spaulders of Prime Emperor (Kings' Rest, needs tier legs) +1.16/+1.27; Chestguard of Corroded Scales (Altar of Fangs, tier legs) +0.99/+0.63;
  Lithiel's Linked Leggings (Murder Row) +0.68/+0.70; Ironroot Collar (Blinding Vale, tier legs) +0.64/+1.14; Lightspire Core (Blinding Vale) +0.51 M+;
  Legguards of the Awakening Brood (Temple of Sethraliss) +0.50/+0.59; Arc-Glass Bindings (Temple of Sethraliss) +0.40/+0.43. All dungeon weapons -3.8 to -4.7%; all dungeon necks lose.
- Projected (Kith'ix 334): Twisted Horror's Tendril +4.02% M+; Zul'jin's Guillotine +2.33% raid; Cuisses of the Uncoiled Union +1.52/+1.61; Caustic Repose Greatbow loses to the Sprigshot.

Currencies at export: Hero crest 105, Myth 25, Champion 148. Catalyst charges not readable from the export (3465:0).

### Bonus roll targets (2026-10-18, from opt_1018 proj singles at 334; boss sources via WebSearch 2026-10-18)
Coiled Altar (Zul'jin's Guillotine +1.21/+2.33, Cuisses +1.52/+1.61) > Entombed Sentinels (Keeper's Seething Core +0.82/+2.03)
> Vashnik (Rancor +0.78/+1.06, Vile Alchemist's Band, chest token) > Sszorak (tier legs token). Kith'ix (Tendril +4.02/+2.18) first if
Voidcores work there (not verified). Disputed sources: Boots of the Reckless Wayfarer (Lost Explorers vs Mor'zahi), Crown of the Eternal Fang
(Nek'zali vs Sentinels). Report: `report/` (build_report.py + template.html -> resetgit_bm_report.html), https://claude.ai/artifact/QWtd5ndDusKTmKb6psqWn7

## 2026-10-24 — Optimal gear, enchants, gems, talents from the start (export 2026-10-24 03:18, client 12.1.5.70529)
SimC midnight 3af1a75, data 12.1.5.70575 (one build newer than client). PROFILESETS (`opt_1024/`): sweep 101 variants
Patchwerk 5000 it (±0.07) in 7 min, DungeonSlice 2000 it (±0.57) in 5 min; finals Patchwerk 10000 / DungeonSlice 5000 in 2 min.
- Free: leg kit Agi&Stam 8159 (or Armor 8163) +0.50 M+ / +0.51 raid; neck Indecipherable +0.20 / +0.18. Raid talents 'solos' +2.29 (M+ -27%).
- M+ best (current talents): crafted legs Farstrider's Reinforced Faulds C/H 331 + crafted bracers H/M 331 + Vile Alchemist's Band 334 ring1
  + free fixes = +3.05% (±0.37); without bracers +2.86; ring + free only +1.44; free only +0.70.
- Raid best (solos): crafted legs C/H + bracers C/H + Sentinel's Vitriolic Chain 334 + Vile 334 + Deadly Peridot = +6.20% (±0.06);
  neck + ring only +4.29; free + solos +3.14.
- All owned weapons, trinkets, off-tier heads/hands and non-crafted belts lose. Report: https://claude.ai/artifact/QWtd5ndDusKTmKb6psqWn7
- 2026-10-24 neck follow-up (`opt_1024/neck_*`), inside best sets, Indecipherable in both necks: raid Sentinel's 334 +0.74 over
  Flowform (+6.20 vs +5.46, ±0.06), Venomstone 340 +0.28 more; M+ Sentinel's 334 +0.06 (tie, ±0.29), 340 +0.44 over Flowform (borderline).
- 2026-10-24 plan regenerated for unlimited Myth crests (user): Sentinel's 334 worn in both modes (M+ set +2.97), order by gain; Sparks are the only limit.

## 2026-10-24 04:17 export — consumables/gems/enchants + "catalyse legs, craft shoulders?" (current talents both modes, per user)
SimC midnight 3af1a75, data 12.1.5.70575 (client 70529). Profilesets, `opt_0417/`. Baseline FULL = worn at caps with the
empty slots filled (Indecipherable in Sentinel's, Eyes of the Eagle + Deadly Amethyst on Vile, Agi&Stam kit on Cuisses).
- As worn (no gem/enchants on the 3 new items) = -3.62% raid / -3.55% M+ vs FULL.
- Consumables: keep Magisters / Recklessness / Silvermoon Parade / Phoenix Oil / Void-Touched (no other pick wins in both
  modes; Blood Knights flask +1.41 raid alone but does not stack with Sickening Signet; rune -0.73 if dropped).
- Raid (Patchwerk 10000, ±0.05): Sickening Signet for Hex Loop +1.53; + tier legs (catalysed Cuisses 334) + crafted shoulders
  C/H 331 +2.54; + crafted bracers C/H +2.95; + Gebbo's Backup Blaster with Ritual Stone moved to the shoulders +3.58.
- M+ (DungeonSlice 6000, ±0.14): Quick Peridot gems +0.15 (tie); + tier legs + shoulders H/M +1.11; + bracers H/M +1.49;
  shoulders C/H + bracers H/M +1.60; Gebbo route +1.24.
- Previous (03:18) plan on this gear: crafted Faulds + bracers = raid +0.28 / M+ -0.12 -> Cuisses beat the crafted legs; superseded.
