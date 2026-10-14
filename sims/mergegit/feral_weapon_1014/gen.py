#!/usr/bin/env python3
"""Feral crafted weapon (shared with Guardian): Aln'hara Pikestaff 331 Q5, embellishment + stats.
Profile 2026-10-14 23:43 (Feral active talents), SimC live 12.1.5.70391. Raid = Patchwerk, M+ = DungeonSlice.
Phase 1: all embellishments, Haste/Vers.  Phase 2 ('p2 E1 E2 ...'): 6 stat pairs."""
import sys
EMB = {"DarkmoonSigilHunt":12693,"DarkmoonSigilBlood":12705,"DarkmoonSigilVoid":13640,"DarkmoonSigilRot":12692,
       "HuntersRitualStone":13771,"AdornedFang":13767,"PolishedAmmolite":13768,"SnakeskinLining":13764,
       "SunfireSilkLining":12385,"DevouringBanding":12685,"BlessedPangoCharm":12686,"PrimalSporeBinding":12687,
       "PrismaticFocusingIris":13453}
BASE = "12214/13667/12497/13751/14004/8960/13836"
PAIRS = (("36/40","HasteVers"),("32/40","CritVers"),("32/36","CritHaste"),("36/49","HasteMast"),("32/49","CritMast"),("49/40","MastVers"))
def pike(stats, emb=None):
    return f"main_hand=,id=245771,bonus_id={BASE}{'/'+str(emb) if emb else ''},crafted_stats={stats},crafting_quality=5,ilevel=331,enchant_id=7983"
L = ["name=A_current_ToxinStaff", "copy=Z_SANITY,A_current_ToxinStaff", "trinket2=,id=270165,bonus_id=6652/13334/12854,ilevel=334"]
if len(sys.argv) == 1:
    tag = "p1"
    L += ["copy=REF_TwinStrikePolearm321,A_current_ToxinStaff", "main_hand=,id=158370,ilevel=321,enchant_id=7983",
          "copy=P_noEmb_HV,A_current_ToxinStaff", pike("36/40")]
    for n, b in EMB.items(): L += [f"copy=E_{n}_HV,A_current_ToxinStaff", pike("36/40", b)]
else:
    tag = "p2"
    for e in sys.argv[2:]:
        for st, sn in PAIRS: L += [f"copy=S_{e}_{sn},A_current_ToxinStaff", pike(st, EMB[e])]
open(f"{tag}_variants.simc", "w").write("\n".join(L) + "\n")
for fs, it in (("Patchwerk", 10000), ("DungeonSlice", 5000)):
    open(f"run_{tag}_{fs}.simc", "w").write(f"threads=4\niterations={it}\ndeterministic=1\nfight_style={fs}\n"
        f"input=../char_feral_2026-10-14.simc\ninput={tag}_variants.simc\n")
