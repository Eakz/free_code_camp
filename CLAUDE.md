# Project memory

## WoW / SimulationCraft analysis for Mergegit (EU-Silvermoon, Druid — Balance main, Guardian offspec)

When asked to work out a loadout, gear choice, enchant, gem, talent or upgrade priority for
this character, follow this method. Guide sites say what is generally true; the sim says what
is true for *this* gear. Sim before committing crests, catalyst charges or a craft.

### 1. Build the sim

Web sandboxes block raidbots/wowhead/archon, but GitHub is reachable.

```bash
git clone --depth 1 --branch midnight https://github.com/simulationcraft/simc
cmake -S simc -B simc/build -G Ninja -DCMAKE_BUILD_TYPE=Release -DBUILD_GUI=OFF -DSC_NO_NETWORKING=ON
cmake --build simc/build -j4     # ~6 min on 4 cores
```

`midnight` = current expansion, `thewarwithin` = previous. Build it in the background and do the
profile prep while it compiles.

### 2. Turn the addon export into a profile

Strip the commented "Gear from Bags" block, keep the equipped lines, and **append the
consumables to the same file** — in a separate file they are parsed before the spec is known and
silently ignored. A wrong flask name exits with code 30 and the DPS table just never prints.

**Pin `ilevel=` on every single item.** SimC's item-bonus DB lags the live client and does not
contain the newest ilevel bonus ids (12846, 13334, 1574 were all missing in 1210-01), so an item
can silently resolve to a lower ilevel than it really is. Take the number from the export's own
comment — `# Graft of the Domanaar (321)` — and write `ilevel=321` on that line.

### 3. THE COMPARISON RULE — max upgraded, enchanted, gemmed

**Never compare a bag item at the item level it happens to be sitting at.** A bag item is a
*candidate*, not an artefact. Before it is compared it must be brought to the same footing as the
piece it would replace:

- **Max item level.** Upgrade the candidate to the highest item level that slot can reach — at
  minimum the slot's watermark (the equipped piece's ilevel is a safe floor for this; the export's
  `slot_high_watermarks` line has the authoritative numbers). Then also sweep **+13 and +26** on
  top, so the answer covers "what if I sink crests into this instead". Report the crossover:
  how many item levels the candidate needs before it wins.
- **Enchant.** Copy the equipped piece's `enchant_id=` onto the candidate. Slots that take an
  enchant this expansion: head, shoulder, chest, legs, feet, both rings, weapon. Wrist, back,
  hands and waist have none — never recommend one there.
- **Gem.** Copy the equipped piece's `gem_id=` onto the candidate if the candidate has a socket.
  **Bonus id `13668` is the socket marker** on this character's necks and rings. SimC applies a
  `gem_id` whether or not the item really has a socket, so check `13668` rather than assuming —
  gemming an unsocketed candidate silently inflates it.
- Dropping a candidate's own `bonus_id` list is safe once `ilevel` is pinned (verified: identical
  stats in 11 of 11 cases, the twelfth differed only by a tertiary) — **except on crafted items**,
  where the stats live in the bonus ids. Crafted candidates keep their full bonus id list.

An item compared raw against a gemmed, enchanted, upgraded incumbent is not a comparison, it is
a foregone conclusion. If any of the three cannot be matched, say so in the answer.

### 4. Run the comparison

One run, many variants, shared RNG, via `name=` / `copy=`:

```
threads=4
iterations=20000
deterministic=1
fight_style=Patchwerk
input=char.simc
talents=<string>
name=A_current
copy=B_variant,A_current
neck=,id=251173,ilevel=321,gem_id=240983
```

Every line after a `copy=` modifies that copy only. Read the DPS Ranking block.

- **Use fixed `iterations`, not `target_error`.** `target_error` escalates to a 1,000,000-iteration
  cap and can take minutes per profile; `iterations=20000 deterministic=1` gives ±0.05% in seconds.
- SimC sims all `copy=` profiles as **one raid**, so runtime scales with the number of profiles.
  DungeonSlice with 25 actors is ~13 min; Patchwerk ~9 min; plan accordingly.
- Fight styles: `Patchwerk` = raid single target. `Patchwerk` + `desired_targets=5` = AoE.
  `DungeonSlice` = generic M+ model, not a real Season 2 route — treat sub-0.5% M+ deltas as ties.
- Always print the error next to the result and refuse to call anything inside it a difference:
  `grep -m1 -o "DPS-Error=[0-9.]*/[0-9.]*%" out.txt`.

### 5. Tanks: DPS is the wrong metric, and DungeonSlice cannot answer it

`fight_style=DungeonSlice` records **no incoming damage at all** — no DTPS is printed. Tank
comparisons must run on **Patchwerk**, and as **separate single-actor invocations** (16 tank copies
in one raid is not a clean damage-taken model). Extract both numbers and rank by damage taken, not
damage done — a build that sims higher can be the one that gets you killed.

### 6. Known SimC 1210-01 quirks — check these before trusting a result

- **`crafted_stats=` is ignored.** The crafted stat pair is encoded in the bonus ids (type-23
  entries such as 13751/13760/13766/14001/14004) and those win. Every `crafted_stats=` variant
  sims identical to the baseline — that is a no-op, not a tie. Testing a recraft needs the bonus
  ids, and the id-to-stat-pair mapping is not yet decoded.
- **Scale factors disagree with item-vs-item swaps.** Stats injected via `enchant_*_rating` (which
  is what `calculate_scale_factors` does internally) are worth measurably less than the same stats
  from a real item — two profiles with identical stat blocks came out 0.8% apart, order-independent,
  with pet damage (fey_missile) as the suspect. **Trust item-vs-item comparisons; treat stat
  weights as indicative only.**
- Confirm embellishments and set bonuses actually fired by grepping the buff list
  (`akilzons_clarity` = Balance 4pc, `arcanoweave_insight`, `critical_ritual`/`hasty_ritual`).
  A buff missing from the list means the export did not carry the flag and it needs forcing.
- An addon export contains equipped gear plus bags only — **not the bank**.

### 7. Reference data lives in the sim, not on the web

- `engine/dbc/generated/item_data.inc` — item names and stats. Stat codes: `3=Agi 4=Str 5=Int
  7=Stam 32=Crit 36=Haste 40=Vers 49=Mastery`, flexible `71=Str/Agi/Int 72=Str/Agi 73=Agi/Int
  74=Str/Int`. **A weapon or trinket showing plain `Int` is dead for Guardian; plain `Agi` is dead
  for Balance.** Flexible codes work in both specs, which is why most gear is shared.
- `engine/dbc/generated/spell_item_enchantment.inc` — enchant ids to names.
- Gem naming: the **stone is the major stat, the adjective the minor** — Amethyst=Mastery,
  Garnet=Crit, Lapis=Vers, Peridot=Haste; Quick=+Haste, Masterful=+Mastery, Versatile=+Vers,
  Deadly=+Crit. A Flawless gem is ~16 major + 7 minor rating, i.e. worth <0.2% DPS: never a
  headline recommendation. The **Eversong Diamonds are flexible primary-stat gems** and much
  stronger — Indecipherable (240983) is +33 Int / +32 Agi.
- `engine/class_modules/sc_druid.cpp` (`default_flask` / `default_food` / `default_potion` /
  `default_rune` / `default_temporary_enchant`) is the authority on consumables per spec.
- `profiles/MID2/*.simc` are the maintained reference profiles — grep them to see which slots even
  have enchants and which enchant the class consensus actually uses. There is no MID2 Balance or
  Guardian druid profile, only Feral; Druid reference gear comes from `profiles/MID1/`.
