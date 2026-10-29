#!/usr/bin/env python3
"""Mergegit gear guide for the 2026-10-29 exports (Guardian 02:00, Balance 02:03): three options with old -> new arrows.

    python3 build.py <icon_dir> <out.html>

Matrix numbers are read from ../opt_1029 (bear_final.txt, out_final_bal_*.json, bear_talents.txt); single-change values come from the
screens (out_pull/*, out_bal_*.json, out_ring_*.json) and are quoted in comments. SimC midnight 710c240, data 12.1.5.70575 (= client)."""
import base64, html, json, os, re, sys
ICON_DIR, OUT = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__)); OPT = os.path.join(HERE, "..", "opt_1029")
E = html.escape
def ic(n):
    with open(os.path.join(ICON_DIR, n + ".png"), "rb") as f: return "data:image/png;base64," + base64.b64encode(f.read()).decode()
I = {k: ic(v) for k, v in {
 "moon": "Spell_Nature_StarFall", "bear": "Ability_Racial_BearForm", "both": "Spell_Nature_ForceOfNature", "head": "INV_Helmet_25",
 "neck": "INV_Jewelry_Necklace_07", "shoulder": "INV_Shoulder_25", "back": "INV_Misc_Cape_18", "chest": "INV_Chest_Leather_09", "wrist": "INV_Bracer_07",
 "hands": "INV_Gauntlets_25", "waist": "INV_Belt_25", "legs": "INV_Pants_Leather_09", "feet": "INV_Boots_Chain_05", "ring": "INV_Jewelry_Ring_14",
 "ring2": "INV_Jewelry_Ring_36", "trinket": "INV_Trinket_80_Titan02a", "weapon": "INV_Spear_04", "talent": "Ability_Druid_Eclipse",
 "ench": "INV_Enchant_EssenceMagicLarge", "gem": "INV_Misc_Gem_Variety_01"}.items()}
WH = "https://www.wowhead.com/item={}"

# ---------- measured numbers
bear = {}
for l in open(os.path.join(OPT, "bear_final.txt")).read().splitlines()[1:]:
    m = re.match(r"(\S+)\s+([+-][\d.]+)%\s+([\d.]+)\s+([+-][\d.]+)%\s+([+-][\d.]+)%\s+([+-][\d.]+)%", l)
    if m: bear[m[1]] = dict(pull=float(m[2]), err=float(m[3]), boss=float(m[4]), dealt=float(m[5]), hp=float(m[6]))
def bal(name):
    d = json.load(open(os.path.join(OPT, name))); b = d["sim"]["players"][0]["collected_data"]["dps"]["mean"]
    return {r["name"]: 100 * (r["mean"] / b - 1) for r in d["sim"]["profilesets"]["results"]}
BR, BM = bal("out_final_bal_raid.json"), bal("out_final_bal_mplus.json")
G, S, SA = bear["G_guardian_optimum"], bear["S_shared_Eyes_variant"], bear["S_shared"]
def f(v, d=1): return f"{v:+.{d}f}%"

# ---------- building blocks
def item(icon, name, iid=0, sub="", cls=""):
    nm = f'<a href="{WH.format(iid)}" target="_blank" rel="noopener">{E(name)}</a>' if iid else f"<b>{E(name)}</b>"
    return f'<div class="it {cls}"><img src="{I[icon]}" alt=""><div><div class="nm">{nm}</div><div class="su">{sub}</div></div></div>'
def line(kind, text): return f'<span class="ln {kind}"><img src="{I["ench" if kind == "e" else "gem"]}" alt="">{E(text)}</span>'
def swap(slot, old, new, gain="", note=""):
    g = f'<div class="gain">{E(gain)}</div>' if gain else ""
    n = f'<div class="note">{E(note)}</div>' if note else ""
    return f'<div class="swap"><div class="sl">{E(slot)}</div><div class="old">{old}</div><div class="arr" aria-hidden="true">➜</div><div class="new">{new}</div>{g}{n}</div>'
def keep(slot, icon, text): return f'<div class="kp"><img src="{I[icon]}" alt=""><div><b>{E(slot)}</b><span>{text}</span></div></div>'
def stats(g, label, items):
    return ''.join(f'<div><b class="{c}">{E(v)}</b><span>{E(t)}</span></div>' for v, t, c in items)

# ---------- GUARDIAN
g_swaps = swap("Chest",
    item("chest", "Enigmatic Dreamwatcher's Lunar Raiment", 271531, "321 · stats of Vest of Reverent Adoration", "dim"),
    item("chest", "Enigmatic Dreamwatcher's Lunar Raiment", 271531, "334 · stats of Chestwrap of Palpable Terror · from your bags") + line("e", "Mark of the Worldsoul (the bag copy has no enchant: apply it)"),
    f"{f(G['pull'])} damage taken (pull) · {f(G['boss'])} (boss) · {f(G['dealt'])} damage dealt",
    "Still a tier piece, so the 4-piece stays. The one change that clears the noise.")
g_keep = "".join([
 keep("Head", "head", "Somnolent Stare 321 · Empowered Rune of Avoidance"), keep("Neck", "neck", "Aqirbane Reliquary 341 · Indecipherable Diamond + Quick Amethyst"),
 keep("Shoulder", "shoulder", "Plumage 321 · Amirdrassil's Grace"), keep("Back", "back", "Stylish Power Cape 321"), keep("Wrist", "wrist", "crafted Deflectors 331 · Arcanoweave"),
 keep("Hands", "hands", "Miststalker's Grips 334"), keep("Belt", "waist", "crafted Utility Belt 331 · Arcanoweave"), keep("Legs", "legs", "Leggings 321 · Agility &amp; Stamina kit"),
 keep("Feet", "feet", "Breakwater Boots 334 · Lynx's Dexterity"), keep("Rings", "ring", "Alluring Bubbleband + Ritual Binder's Ring · Silvermoon's Alacrity · Quick Lapis"),
 keep("Trinkets", "trinket", "Gebbo's Bottomless Bag + Keeper's Seething Core"), keep("Weapon", "weapon", "Abyssal Broodfiend's Bardiche 341 · Berserker's Rage")])
g_lose = [("Band of the Swarmcaller (either ring)", "+4.6 to +5.2%", "+4.5% max HP, but it takes more damage"), ("Voracious Heart of Ula'tek", "+8.6 to +10.1%", ""),
          ("Miststalker's Cinch / Whirling Dervish (lose Arcanoweave)", "+3.6 / +5.5%", ""), ("Yoke of the Charging Bear", "+5.6%", ""),
          ("Vile Vial / Fang of Umbral Malignance", "+3.9 / +18%", ""), ("Subjugator's Chilling Grips", "+3.1%", ""), ("Sickening Signet", "+3.0 to +3.2%", ""),
          ("Eyes of the Eagle on the rings", "+1.9%", ""), ("Intellect leg kit", "+3.5%", ""), ("Miststalker's Cuisses (leaves the tier set)", "+7.9%", "")]

# ---------- BALANCE
b_swaps = (
 swap("Chest", item("chest", "Lunar Raiment 334", 271531, "no enchant", "dim"),
      item("chest", "Lunar Raiment 334", 271531, "same piece") + line("e", "Mark of the Worldsoul"), "+1.45% raid · +1.44% M+", "It was missing an enchant.") +
 swap("Ring", item("ring2", "Sickening Signet of Atroxus", 252258, "321", "dim"),
      item("ring", "Charged Sandstone Band", 158366, "321 · from your bags") + line("e", "Eyes of the Eagle") + line("g", "Flawless Masterful Garnet"),
      "+0.8% raid · +0.4% M+", "Keep Band of the Swarmcaller in the other slot.") +
 swap("Hands", item("hands", "Subjugator's Chilling Grips", 193758, "321", "dim"), item("hands", "Miststalker's Grips", 272241, "334 · from your bags"),
      "+0.1% raid · +0.25% M+ (tie)", "Optional for Balance; you want it for the bear anyway.") +
 swap("Talents (raid)", item("talent", "Your current build", 0, "", "dim"), item("talent", "Raider.IO Build", 0, "saved loadout"), "+3.6% raid", "") +
 swap("Talents (M+)", item("talent", "Your current build", 0, "", "dim"), item("talent", "ra s2", 0, "saved loadout"), "+2.9% M+", ""))
b_keep = "".join([
 keep("Head", "head", "Somnolent Stare · Rune of Avoidance"), keep("Neck", "neck", "Aqirbane Reliquary 341 · Indecipherable + Quick Amethyst"),
 keep("Shoulder", "shoulder", "Plumage · Amirdrassil's Grace"), keep("Wrist", "wrist", "crafted Deflectors · Arcanoweave"), keep("Belt", "waist", "Whirling Dervish Sash"),
 keep("Legs", "legs", "Leggings · Intellect kit"), keep("Feet", "feet", "Breakwater Boots · Lynx's Dexterity"), keep("Ring", "ring", "Band of the Swarmcaller · Eyes of the Eagle"),
 keep("Trinkets", "trinket", "Vile Vial of Volatile Venom + Gebbo's Bottomless Bag"), keep("Weapons", "weapon", "Jan'thrazet 341 · Rite of the Hash'ey + Aln'hara Lantern (Ritual Stone)")])
b_lose = [("Voracious Heart / Keeper's Seething Core", "-5 to -8%", ""), ("Crafted Utility Belt (needs a 3rd embellishment; without the Lantern it is -9.5%)", "-9.5%", ""),
          ("Yoke of the Charging Bear", "-2.4%", ""), ("Bubbleband / Ritual Binder in place of Swarmcaller", "-1.8 to -2.3%", ""), ("Agility leg kit", "-1.2%", ""),
          ("Silvermoon's Alacrity on the rings", "-1.2 to -1.5%", ""), ("Miststalker's Cuisses (leaves the tier set)", "-5.4 to -5.6%", "")]

# ---------- BOTH
both_bear = (
 swap("Chest", item("chest", "Lunar Raiment 321", 271531, "", "dim"), item("chest", "Lunar Raiment 334", 271531, "Chestwrap stats") + line("e", "Mark of the Worldsoul"), "", "") +
 swap("Ring", item("ring", "Alluring Bubbleband", 268266, "", "dim"), item("ring", "Band of the Amani Warlord", 273792, "321 · from your bags") + line("e", "Eyes of the Eagle") + line("g", "Flawless Quick Lapis"), "", "") +
 swap("Ring enchant", item("ench", "Silvermoon's Alacrity", 0, "on Ritual Binder's Ring", "dim"), item("ench", "Eyes of the Eagle", 0, "same ring, keep Quick Lapis"), "", ""))
both_bal = (
 swap("Chest", item("chest", "Lunar Raiment 334", 271531, "no enchant", "dim"), item("chest", "Lunar Raiment 334", 271531, "") + line("e", "Mark of the Worldsoul"), "", "") +
 swap("Hands", item("hands", "Subjugator's Chilling Grips", 193758, "", "dim"), item("hands", "Miststalker's Grips", 272241, "334"), "", "") +
 swap("Legs", item("legs", "Leggings · Intellect kit", 271527, "", "dim"), item("legs", "Leggings · Agility &amp; Stamina kit", 271527, "the bear's pair (the 8159 copy in your bags)"), "", "") +
 swap("Ring", item("ring", "Band of the Swarmcaller", 281029, "", "dim"), item("ring", "Band of the Amani Warlord", 273792, "321") + line("e", "Eyes of the Eagle") + line("g", "Flawless Quick Lapis"), "", "") +
 swap("Ring", item("ring2", "Sickening Signet of Atroxus", 252258, "", "dim"), item("ring2", "Ritual Binder's Ring", 159459, "321") + line("e", "Eyes of the Eagle") + line("g", "Flawless Quick Lapis"), "", ""))
both_per = ("<ul class='pl'><li><b>Belt:</b> bear wears the crafted Utility Belt, Balance wears Whirling Dervish Sash. Both can't wear the crafted belt: wrist + belt + Lantern would be 3 embellishments (cap 2). "
            f"Wearing a Cinch on the bear instead costs it {bear['S_shared_noBeltSwap(Cinch)']['pull'] - SA['pull']:.1f} points more damage taken.</li>"
            "<li><b>Trinkets:</b> bear Gebbo + Keeper's, Balance Vile Vial + Gebbo (Keeper's has no Intellect, Vile Vial costs the bear +4 to +5%).</li>"
            "<li><b>Weapons:</b> bear Bardiche, Balance Jan'thrazet + Lantern.</li></ul>")

# ---------- matrix
rows = [
 ("Guardian optimum", "bear", G, f(BR['G_guardian_set_on_balance']), f(BM['G_guardian_set_on_balance']), "G set worn on Balance: Alacrity rings, Agility kit"),
 ("Balance optimum", "moon", bear["B_balance_set_on_bear"], f(BR['B_balance_optimum']), f(BM['B_balance_optimum']), "B set worn on the bear"),
 ("Both worlds (Eyes)", "both", S, f(BR['S_shared_Eyes_variant']), f(BM['S_shared_Eyes_variant']), "recommended shared set"),
 ("Both worlds (Alacrity)", "both", SA, f(BR['S_shared']), f(BM['S_shared']), "same, Alacrity on the rings"),
]
def mrow(n, ic_, b, r, m, note):
    cls = lambda v, low: "up" if (v < 0) == low else "dn"
    return (f'<tr><td><img src="{I[ic_]}" alt=""> {E(n)}</td>'
            f'<td class="n {cls(b["pull"], True)}">{f(b["pull"])}</td><td class="n {cls(b["boss"], True)}">{f(b["boss"])}</td><td class="n {cls(b["dealt"], False)}">{f(b["dealt"])}</td><td class="n">{f(b["hp"])}</td>'
            f'<td class="n {cls(float(r[:-1]), False)}">{r}</td><td class="n {cls(float(m[:-1]), False)}">{m}</td><td class="c">{E(note)}</td></tr>')
matrix = "".join(mrow(*r) for r in rows)
cost_bear = abs(G["pull"] - S["pull"]); cost_bal_r = BR["B_balance_optimum"] - BR["S_shared_Eyes_variant"]; cost_bal_m = BM["B_balance_optimum"] - BM["S_shared_Eyes_variant"]

TALKS = [("Balance raid", "Raider.IO Build", f"{f(3.54)} on the Balance sweep, {f(BR['WORN_alt_talents'])} measured on your gear; your current build ties 'm+ s2'"),
         ("Balance M+", "ra s2", f"{f(2.87)} over 'm+ s2' in the sweep, {f(BM['WORN_alt_talents'])} measured vs your current build"),
         ("Guardian", "your current build (= m+ dps)", "every other loadout takes +29% to +528% more damage; re-checked on the new patch")]
tal = "".join(f"<tr><td>{E(a)}</td><td><b>{E(b)}</b></td><td class='c'>{E(c)}</td></tr>" for a, b, c in TALKS)

CSS = open(os.path.join(HERE, "style.css"), encoding="utf-8").read()
body = f'''<title>Mergegit Gear Guide</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=Alegreya+Sans:wght@400;500;700&family=IBM+Plex+Mono:wght@500&display=swap">
<style>{CSS}</style>
<div class="wrap">
 <header><div class="forms"><img class="m" src="{I["moon"]}" alt="Balance"><img class="b" src="{I["bear"]}" alt="Guardian"></div>
  <div><h1>Mergegit · Gear Guide</h1><p class="lede">Night Elf Druid, EU-Silvermoon. Built from your 2026-10-29 exports (Guardian 02:00, Balance 02:03), simulated on SimulationCraft midnight 710c240 with game data 12.1.5.70575, the same build as your client. Everything comes from what is already in your bags and every item is at its upgrade cap. Struck-through is what you wear now; the arrow points at what to put on.</p></div></header>

 <section class="cards">
  <div class="card g"><img src="{I["bear"]}" alt=""><h3>1 · Guardian only</h3><b>{f(G["pull"])}</b><span>damage taken, 5-mob pull</span><p>One swap: the 334 Lunar Raiment chest. Everything else already beats the alternatives.</p></div>
  <div class="card m"><img src="{I["moon"]}" alt=""><h3>2 · Balance only</h3><b>{f(BR["B_balance_optimum"])} raid</b><span>{f(BM["B_balance_optimum"])} M+ · gear only</span><p>Enchant the chest, swap one ring. Raider.IO talents add {f(BR["B_balance_optimum+alt_talents"] - BR["B_balance_optimum"])} in raid, ra s2 adds {f(BM["B_balance_optimum+alt_talents"] - BM["B_balance_optimum"])} in M+.</p></div>
  <div class="card x"><img src="{I["both"]}" alt=""><h3>3 · Both specs</h3><b>{f(S["pull"])} / {f(BR["S_shared_Eyes_variant"])}</b><span>bear taken · Balance raid</span><p>One set of armour and rings for both. Sharing costs the bear {cost_bear:.1f} points of damage taken and Balance {cost_bal_r:.1f}% (raid) / {cost_bal_m:.1f}% (M+) against their own optimum.</p></div>
 </section>

 <section class="frame"><h2>The three options</h2>
  <div class="tabs" role="tablist">
   <button class="tab" role="tab" data-k="g" id="t-g" aria-controls="p-g"><img src="{I["bear"]}" alt="">1 · Guardian</button>
   <button class="tab" role="tab" data-k="m" id="t-m" aria-controls="p-m"><img src="{I["moon"]}" alt="">2 · Balance</button>
   <button class="tab" role="tab" data-k="x" id="t-x" aria-controls="p-x"><img src="{I["both"]}" alt="">3 · Both specs</button></div>

  <div class="panel" id="p-g" role="tabpanel" aria-labelledby="t-g">
   <div class="ph"><div><h3>Guardian, ignoring Balance</h3><p>Bear numbers vs your worn set: five heroic mobs attacking (pull) and one Mythic dummy (boss). Error ±0.33% on damage taken.</p></div>
    <div class="nums">{stats("g", "", [(f(G["pull"]), "taken, pull", "up"), (f(G["boss"]), "taken, boss", "up"), (f(G["dealt"]), "dealt", "up"), (f(G["hp"]), "max HP", "eq")])}</div></div>
   <h4>Change</h4>{g_swaps}
   <h4>Keep exactly as worn (tested, nothing beats it)</h4><div class="keeps">{g_keep}</div>
   <p class="small">Also tested and tied within error: Rite of the Hash'ey on the Bardiche (-0.2% taken), Versatile Peridot in the neck (-0.3%), Armor leg kit (-0.2%). Not worth a swap.</p>
   <h4>What loses on the bear (more damage taken)</h4><div class="tw"><table><tbody>{''.join(f"<tr><td>{E(a)}</td><td class='n dn'>{b}</td><td class='c'>{E(c)}</td></tr>" for a, b, c in g_lose)}</tbody></table></div>
  </div>

  <div class="panel" id="p-m" role="tabpanel" aria-labelledby="t-m" hidden>
   <div class="ph"><div><h3>Balance, ignoring the bear</h3><p>Raid on Patchwerk, M+ on DungeonSlice, vs your worn Balance set. Gear only; talents are listed separately. Error ±0.10% raid, ±0.24% M+.</p></div>
    <div class="nums">{stats("m", "", [(f(BR["B_balance_optimum"]), "raid", "up"), (f(BM["B_balance_optimum"]), "M+", "up"), (f(BR["B_balance_optimum+alt_talents"]), "raid + Raider.IO", "up"), (f(BM["B_balance_optimum+alt_talents"]), "M+ + ra s2", "up")])}</div></div>
   <h4>Change</h4>{b_swaps}
   <h4>Keep exactly as worn</h4><div class="keeps">{b_keep}</div>
   <p class="small">Ring gems are all within error. Your Masterful Peridot / Garnet gems are fine. Embellishments: wrist Arcanoweave + Lantern Ritual Stone = 2, the cap.</p>
   <h4>What loses on Balance</h4><div class="tw"><table><tbody>{''.join(f"<tr><td>{E(a)}</td><td class='n dn'>{b}</td><td class='c'>{E(c)}</td></tr>" for a, b, c in b_lose)}</tbody></table></div>
  </div>

  <div class="panel" id="p-x" role="tabpanel" aria-labelledby="t-x" hidden>
   <div class="ph"><div><h3>One set for both specs</h3><p>Shared: chest, hands, leggings with kit, rings. Per spec: belt, trinkets, weapons (see below). Vs each spec's worn set.</p></div>
    <div class="nums">{stats("x", "", [(f(S["pull"]), "bear taken, pull", "up"), (f(S["boss"]), "bear taken, boss", "up"), (f(BR["S_shared_Eyes_variant"]), "Balance raid", "dn"), (f(BM["S_shared_Eyes_variant"]), "Balance M+", "dn")])}</div></div>
   <h4><img class="inl" src="{I["bear"]}" alt=""> On the bear</h4>{both_bear}
   <h4><img class="inl" src="{I["moon"]}" alt=""> On Balance</h4>{both_bal}
   <h4>Still different per spec</h4>{both_per}
   <p class="small">Rings and leg kit are where the specs disagree. Eyes of the Eagle vs Silvermoon's Alacrity: Eyes costs the bear {f(S["pull"] - SA["pull"])} on the pull but gives it more damage ({f(S["dealt"])} vs {f(SA["dealt"])}) and gives Balance {BR["S_shared_Eyes_variant"] - BR["S_shared"]:.1f} points back in raid. The Agility kit costs Balance 1.2%; the Intellect kit would cost the bear 3.5%.</p>
  </div>
 </section>

 <section class="frame"><h2>What sharing costs</h2>
  <p class="intro">Every set on both specs, against each spec's own worn set. Bear: damage taken (lower is better), damage dealt, max HP. Balance: damage change. The cost of sharing is the gap between a spec's own optimum and the "Both worlds" row.</p>
  <div class="tw"><table class="mx"><thead><tr><th>Set</th><th colspan="4">Bear</th><th colspan="2">Balance</th><th></th></tr>
   <tr><th></th><th>taken pull</th><th>taken boss</th><th>dealt</th><th>max HP</th><th>raid</th><th>M+</th><th>note</th></tr></thead><tbody>{matrix}</tbody></table></div>
  <p class="small">Own optimum for reference: bear {f(G["pull"])} taken, Balance {f(BR["B_balance_optimum"])} raid / {f(BM["B_balance_optimum"])} M+. Swapping the rings and leg kit when you change spec recovers the difference ({cost_bear:.1f} points for the bear, {cost_bal_r:.1f}% raid and {cost_bal_m:.1f}% M+ for Balance) at the price of two swaps.</p></section>

 <section class="frame"><h2><img class="inl" src="{I["talent"]}" alt=""> Talents</h2><p class="intro">Tested separately from gear. Balance talents changed a lot since 10-21 (the patch moved them); the gear picks above hold on every talent set I tried.</p>
  <div class="tw"><table><thead><tr><th>Mode</th><th>Use</th><th>Result</th></tr></thead><tbody>{tal}</tbody></table></div></section>

 <section class="frame"><h2>How this was made</h2><ul class="notes">
  <li>SimC midnight 710c240 (2026-10-28), game data 12.1.5.70575 = your client. Exports: Guardian 2026-10-29 02:00 and Balance 02:03. Items are simmed at their upgrade cap (Hero 321, Myth 334, crafted 331; your Venomstoned 341 pieces as worn). Crafting new items and new Venomstones were out of scope: "what I have".</li>
  <li>Bear: one run per variant, 3,000 iterations to screen 88 single changes, 8,000 for the final sets, five attacking heroic mobs as the pull model. Balance: SimC profilesets, 6,000 / 3,500 iterations to screen 103 variants and 10,000 / 6,000 for the finals. All runs include a control copy that came back at 0.00%.</li>
  <li>The heroic mob strength is a stand-in for a hard key. Damage taken does not count max health, which is why Swarmcaller looks worse for the bear than it is.</li>
  <li>Your gloves carry the enchant "Ancient Hash'ey Battle Art: Eye of the Lynx". SimC does not model it, so its value is not in these numbers.</li>
  <li>Embellishment cap (2) holds in every set. Whether two Arcanoweave pieces are allowed was confirmed by you.</li>
  <li>Raw inputs and outputs: sims/mergegit/opt_1029 on branch claude/epic-cori-kqdhlt.</li></ul></section>
</div>
<script>(function(){{var tabs=[].slice.call(document.querySelectorAll('.tab'));
function show(k){{tabs.forEach(function(t){{var on=t.dataset.k===k;t.setAttribute('aria-selected',on);t.tabIndex=on?0:-1;document.getElementById('p-'+t.dataset.k).hidden=!on;}});try{{localStorage.setItem('mg3-tab',k)}}catch(e){{}}}}
tabs.forEach(function(t){{t.addEventListener('click',function(){{show(t.dataset.k)}})}});
var s='g';try{{var v=localStorage.getItem('mg3-tab');if(v&&document.getElementById('p-'+v))s=v}}catch(e){{}}
if(location.hash&&document.getElementById('p-'+location.hash.slice(1)))s=location.hash.slice(1);show(s);}})();</script>'''
open(OUT, "w", encoding="utf-8").write(body)
print(OUT, len(body))
