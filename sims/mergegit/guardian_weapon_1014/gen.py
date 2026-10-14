#!/usr/bin/env python3
"""Guardian crafted weapon: Aln'hara Pikestaff 331 Q5 (4 sparks + 80 Myth crests), which embellishment and stats.
Bear has 1/2 embellishments (wrist Arcanoweave). Profile 2026-10-14 23:01, SimC on live 12.1.5.70391.
Phase 1: every Midnight embellishment SimC models, stats Haste/Vers. Phase 2 (argv 'p2 EMB1 EMB2'): stat pairs."""
import sys, os
EMB = {"DarkmoonSigilHunt":12693,"DarkmoonSigilBlood":12705,"DarkmoonSigilVoid":13640,"DarkmoonSigilRot":12692,
       "HuntersRitualStone":13771,"AdornedFang":13767,"PolishedAmmolite":13768,"SnakeskinLining":13764,
       "SunfireSilkLining":12385,"DevouringBanding":12685,"BlessedPangoCharm":12686,"PrimalSporeBinding":12687,
       "PrismaticFocusingIris":13453,"StabilizingGemstoneBandolier":13454}
BASE = "12214/13667/12497/13751/14004/8960/13836"
def pike(stats, emb=None):
    b = BASE + (f"/{emb}" if emb else "")
    return f"main_hand=,id=245771,bonus_id={b},crafted_stats={stats},crafting_quality=5,ilevel=331,enchant_id=7983"
def write(n, lines):
    open(f"runs/{n}.simc","w").write("threads=4\niterations=10000\ndeterministic=1\nfight_style=Patchwerk\ndesired_targets=1\n"
        "input=../../char_guardian_2026-10-14.simc\n" + f"name={n}\n" + "".join(l+"\n" for l in lines))
if len(sys.argv) == 1:
    write("A_current_ToxinStaff", []); write("Z_SANITY", ["trinket2=,id=270165,bonus_id=6652/13334/12854,ilevel=334"])
    write("REF_TwinStrikePolearm321", ["main_hand=,id=158370,ilevel=321,enchant_id=7983"])
    write("P_noEmb_HV", [pike("36/40")])
    for n, b in EMB.items(): write(f"E_{n}_HV", [pike("36/40", b)])
else:
    for e in sys.argv[2:]:
        for st, sn in (("36/40","HasteVers"),("32/40","CritVers"),("32/36","CritHaste"),("36/49","HasteMast"),("32/49","CritMast"),("49/40","MastVers")):
            write(f"S_{e}_{sn}", [pike(st, EMB[e])])
