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

- **Max item level — BOTH SIDES.** Every item in the comparison, the equipped one included, is
  simmed at the top of its own upgrade track. The incumbent does not stay at the item level it
  happens to be sitting at any more than the candidate does: if a worn ring is 315 and rings cap
  at 321, it is simmed at 321. Never sweep past a track's real cap — that invents item levels the
  player cannot obtain and produces a chase list they cannot act on.

  Track caps for this character, Midnight Season 2:
  - **M+ / dungeon (Hero) tops out at 321.** Dungeons do not drop Mythic. Anything worn below
    321 that came from a dungeon goes to 321 on both sides of the comparison.
  - Items already above 321 (crafted 331, raid/vault 334) are on higher tracks — leave them at
    the item level they are, do not push them further without evidence of the cap.
  - **Crafted PvE** is proven to 331 (the worn crafted wrist and staff sit there).
  - **PvP crafted ("Thalassian Competitor's", "Venomous Gladiator's/Aspirant's")** stays at its
    PvE item level — it scales in PvP only. Do not upgrade it in a PvE comparison.
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

### 3a. BUILD THE PROFILE WITH THE SCRIPT - never by hand

`python3 tools/build_profile.py export.txt > char.simc`

The max-item-level rule below was written, committed, and then broken anyway, twice, because
it reads as a rule about *candidates* while the baseline profile was still being typed out by
hand straight from the export - leaving the worn gear at whatever item level it happened to be
sitting at. Both the Balance and Guardian profiles were built that way and every number from
them had to be thrown out.

So profile construction is no longer a judgement call:

1. Run the script. It pins `ilevel=` on every slot at that item's track cap and prints a
   RAW -> CAP table to stderr.
2. **Paste that table into the answer, or at minimum read every row.** A slot showing
   `RAW -> CAP` with an UPGRADE flag you did not expect means the profile is wrong.
3. Only then sim. A result from a hand-written profile is not reportable.

The script refuses to guess: if an item has no `# Name (ilvl)` comment above it in the export
it aborts rather than inventing a level.

### 3b. Mistakes already made here — do not repeat any of them

Each of these was made in a real session, cost the user several rounds, and is now a hard rule.

1. **Try WebSearch before declaring the web unavailable.** `curl` and WebFetch are blocked by the
   egress proxy for wowhead, wago, expcarry, conquestcapped, vercel apps and most fansites. The
   **WebSearch tool is not blocked** and returns page content. Four rounds were wasted telling the
   user dungeon loot tables were unobtainable without ever trying it. Test each channel separately;
   never generalise one tool's failure to "no web access".
2. **Never sim above a track's real cap.** A run comparing everything at 334/347 produced a chase
   list of item levels dungeons cannot drop. Establish the cap first, then sim at it.
3. **Do not invent a filter from a small sample.** Quality==3 was declared to identify M+ loot on
   the strength of 31 of the player's own items. It only means "rare" and matched hundreds of
   trinkets back to Warlords. Validate any classifier against the whole table before using it.
4. **Sim gains are not always real gains.** Check what an item actually does before recommending
   it. Sealed Chaos Urn simmed +0.81% and is a delve trinket that horrifies the wearer for 5s —
   SimC models the buff, not the downside. Vaelgor's Final Stare simmed +0.99% and is a Season 1
   raid drop that caps at 279, so it can never reach 321. Always check source and cap.
5. **`crafted_stats=` does nothing** — see the quirks section. Variants using it are no-ops, not
   ties, and must not be reported as "no difference".
6. **Put a sanity actor in every run.** Re-declare one already-equipped item as its own variant.
   It must come back at 0.00% +/- the error bar. Every run in this project has one.
7. **Single-change comparisons are Droptimizer, not Top Gear.** One change at a time misses
   combinations that only win together. When the user asks for "optimal", run the combinations too.
8. **Sweep stat pairings, not just the items the player happens to own.** Bag items cluster
   around the player's current stat mix, so testing only those returns a page of ties and hides
   the answer. For every slot in question, pick one real item per distinct pairing
   (Crit/Mastery, Mastery/Crit, Mastery/Haste, Haste/Mastery, Mastery/Vers, Crit/Vers,
   Haste/Vers) and sim them all. That is what makes "chase this stat combination" sayable.
9. **Check crafted alternatives in EVERY slot.** Crafted PvE gear reaches 331 while dungeon gear
   stops at 321, so a crafted piece can win on item level alone. A third crafted item is legal —
   the two-embellishment cap limits embellishments, not crafted pieces.
9b. **`crafted_stats=` in an export does NOT mean the item is crafted.** Dropped items can have
   selectable stats too. The Slitherscale Girdle carries `crafted_stats=40/36` and the 24/25 stat
   codes, and is a **Venomous Abyss raid trash drop**. It was wrongly assumed craftable, given a
   crafted item level of 331 it has no claim to, and reported as +0.58%; at a defensible 321 it
   is +0.08%, a tie. A real crafted piece in this player's bags also carries
   **`crafting_quality=5`** and `content_tuning=3615` — check those, and confirm the item's
   source, before applying any track cap to it. Never assign an item level a source cannot drop.
10. **Filter by armour subclass before simming.** `item_class=4` with `item_subclass` 1=cloth,
   2=leather, 3=mail, 4=plate. Cloaks are subclass 1 for everyone. Feeding a mail belt to a
   druid aborts the whole run with "Invalid type" and wastes the batch.

### 3c. Season 2 item level facts (verified)

- **M+ end-of-dungeon cache caps at 321.** Great Vault from M+ reaches 337. Dungeons never drop
  Mythic-track gear. Confirmed in-game by the player and independently by search.
- The player's own gear proves: crafted PvE reaches 331; two pieces sit at 334 from bonus rolls.
- Published track tables (Champion 285-302, Myth 315-328, last two Mythic raid bosses 344) do not
  fully reconcile with the player's actual item levels. **Trust the player's export and watermarks
  over a fansite table**, and say which you used.

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

- **`crafted_stats=` WORKS, but only with `crafting_quality=5` AND without the stat-setting
  bonus ids.** An earlier note in this file claimed it was ignored; that was wrong and it
  invalidated every crafted-item comparison made under it.
  - A crafted item's two stat slots show up as stat codes **24 and 25** in `item_data.inc`. If
    the bonus id list already resolves them (the worn wrist's 13751/14001, the worn staff's
    13751/14004), those win and `crafted_stats=` does nothing.
  - If the bonus ids do NOT resolve them, the item sims with **zero secondary stats** and loses
    by a mile for no real reason. Slitherscale Girdle simmed at Crit 0 / Haste 0 / Mastery 0 /
    Vers 0 and was reported as -2.2%, which was meaningless.
  - Correct form: `waist=,id=271436,ilevel=331,crafted_stats=49/36,crafting_quality=5`.
  - **Always print an item's resolved secondaries before trusting its result.** A crafted item
    showing zeroes is a broken profile line, not a bad item.
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
