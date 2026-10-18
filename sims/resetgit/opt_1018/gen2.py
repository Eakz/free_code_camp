#!/usr/bin/env python3
"""Resetgit BM: dungeon sweep (S2 M+ pool, all items at Hero 6/6 321) + projected BiS (raid at Myth 334,
crafted 331). Enchants/gems copied from the replaced slot. Tier slots (head/shoulder/chest/hands) are also simmed
with Skulking Viper's tier legs (271491) so 4pc survives. Item->dungeon from web research 2026-10-18."""
EN = {"head":8017,"chest":7987,"legs":8161,"feet":7963,"finger1":7967,"finger2":7967,"main_hand":8689}
GEM = {"neck":"240967","finger1":"240898","finger2":"240898"}
TIERLEGS = lambda il: f"legs=,id=271491,ilevel={il},enchant_id=8161"
def line(slot, iid, il):
    s = f"{slot}=,id={iid},ilevel={il}"
    if slot in EN: s += f",enchant_id={EN[slot]}"
    if slot in GEM: s += f",gem_id={GEM[slot]}"
    return s
D = [  # (dungeon, slot, id, name)
 ("Altar","wrist",273775,"HydraScaleWristguards"),("Altar","chest",273789,"ChestguardCorrodedScales"),("Altar","main_hand",273784,"AncestralAmaniRecurve"),
 ("Altar","neck",273781,"StrandWardingFangs"),("Altar","trinket",273796,"VileVial"),
 ("MurderRow","shoulder",251131,"JanglingFelpaulets"),("MurderRow","legs",251141,"LithielsLinkedLeggings"),("MurderRow","main_hand",271680,"SinsearedRepeater"),
 ("MurderRow","neck",251142,"PendantMaleficFury"),("MurderRow","ring",251136,"SignetSnarlingServitude"),("MurderRow","trinket",250243,"ManaheartsBindingFlame"),
 ("Nalorakk","waist",251155,"TribalDefendersCord"),("Nalorakk","feet",251145,"ForgottenTribeFootguards"),("Nalorakk","head",251158,"NalorakksNightmare"),
 ("Nalorakk","ring",251148,"PilferedPreciousBand"),("Nalorakk","trinket",250229,"IdolOfTheWarLoa"),
 ("BlindingVale","shoulder",251184,"IronrootCollar"),("BlindingVale","hands",251165,"PulverizingPads"),("BlindingVale","wrist",251200,"SaptorbaneGuards"),
 ("BlindingVale","main_hand",251187,"AmirdrassilsReach"),("BlindingVale","back",251190,"BloodthornBurnous"),("BlindingVale","trinket",250214,"LightspireCore"),
 ("BlindingVale","trinket",250259,"SaplingDawnroot"),
 ("Voidscar","waist",251228,"BehemothWaistband"),("Voidscar","chest",251233,"ManipulatorsVest"),("Voidscar","neck",251234,"GraftDomanaar"),
 ("Voidscar","trinket",250225,"VoidExecutionMandate"),("Voidscar","trinket",250245,"TumorOfTheSwarm"),
 ("RubyLife","legs",193759,"EggTendersLeggings"),("RubyLife","head",193765,"BlazeboundLieutenantsHelm"),("RubyLife","hands",193752,"GalerattleGauntlets"),
 ("RubyLife","back",193763,"FireproofDrape"),("RubyLife","trinket",193757,"RubyWhelpShell"),("RubyLife","trinket",193762,"BlazebindersHoof"),
 ("RubyLife","trinket",193748,"KyrakkasSearingEmbers"),
 ("KingsRest","waist",159369,"BeltConsecratedTomb"),("KingsRest","hands",160213,"SepulchralConstructsGloves"),("KingsRest","feet",159371,"BootsHeadlongConqueror"),
 ("KingsRest","chest",239046,"LoaBlessedChestguard"),("KingsRest","shoulder",239049,"SpauldersPrimeEmperor"),("KingsRest","back",159288,"CloakRestlessTribes"),
 ("KingsRest","ring",159459,"RitualBindersRing"),("KingsRest","trinket",159617,"LustrousGoldenPlumage"),("KingsRest","trinket",159618,"MchimbasRitualBandages"),
 ("Sethraliss","wrist",159380,"ArcGlassBindings"),("Sethraliss","feet",159388,"SabatonsCoruscatingEnergy"),("Sethraliss","legs",159375,"LegguardsAwakeningBrood"),
 ("Sethraliss","head",239035,"SethralissFangedHelm"),("Sethraliss","chest",239034,"CorruptedHexxersVestments"),("Sethraliss","ring",162544,"JadeOphidianBand"),
 ("Sethraliss","ring",158366,"ChargedSandstoneBand"),("Sethraliss","trinket",158374,"TinyElectromental"),
]
P = [  # projected: (source, slot, id, name, ilvl)
 ("Ulatek","main_hand",268207,"CausticReposeGreatbow",334),("Ulatek","neck",268265,"AqirbaneReliquary",334),
 ("Raid","head",268230,"CrownEternalFang",334),("Raid","feet",268233,"FerociousScaleboots",334),("Raid","legs",268237,"CuissesUncoiledUnion",334),
 ("Raid","waist",268216,"CursedReliquaryCincture",334),("Raid","wrist",268217,"RisingTideWristguards",334),("Raid","waist",268254,"SerpentineMixingBelt",334),
 ("Raid","feet",268258,"BootsRecklessWayfarer",334),("Raid","neck",268251,"AmuletTwinFangs",334),("Raid","neck",268250,"SentinelsVitriolicChain",334),
 ("Raid","ring",268249,"VileAlchemistsBand",334),("Raid","ring",268252,"ApexBrutesClawRing",334),("Raid","ring",268266,"AlluringBubbleband",334),
 ("Kithix","ring",281029,"BandSwarmcaller",334),("Raid","back",268248,"AmaniSummoningShawl",334),("Raid","back",268253,"SilkenVoodooDrape",334),
 ("Kithix","trinket",281215,"TwistedHorrorsTendril",334),("Ulatek","trinket",270168,"FontVenomousRage",334),("Ulatek","trinket",270175,"VoraciousHeart",334),
 ("Raid","trinket",270173,"ZuljinsGuillotine",334),("Raid","trinket",270166,"VashniksSanguineRancor",334),("Raid","trinket",270165,"KeepersSeethingCore",334),
 ("Raid","trinket",270169,"HexLordsDoomingIdol",334),("Raid","trinket",270174,"IdolHowlingNexus",334),("Raid","trinket",270171,"PreternaturalAntivenom",334),
 ("Raid","trinket",270167,"WavecallersSeastone",334),("Raid","trinket",270160,"FirstMatesShellward",334),("Raid","main_hand",268200,"GebbosBackupBlaster",334),
 ("Kithix","hands",281238,"AberrantCommandersGauntlets",334),("Tier","legs",271491,"SkulkingViperTierLegs",334),
]
def variants(rows, prefix):
    V = []
    for src, slot, iid, name, il in rows:
        if slot == "ring":
            for f in ("finger1","finger2"): V.append((f"{prefix}{f[-1]}R_{name}_{src}", [line(f, iid, il)]))
        elif slot == "trinket":
            for t in ("trinket1","trinket2"): V.append((f"{prefix}{t[-1]}T_{name}_{src}", [line(t, iid, il)]))
        elif slot in ("head","shoulder","chest","hands"):
            V.append((f"{prefix}{slot[:2].upper()}_{name}_{src}+TierLegs", [line(slot, iid, il), TIERLEGS(321 if prefix=="D_" else 334)]))
        elif slot == "neck" and iid == 268265:
            V.append((f"{prefix}NE_{name}_{src}", [f"neck=,id=268265,ilevel={il},gem_id=240967/240898"]))
        else:
            V.append((f"{prefix}{slot[:2].upper()}_{name}_{src}", [line(slot, iid, il)]))
    return V
DV = variants([(a,b,c,d,321) for a,b,c,d in D], "D_"); DV.insert(0, ("D_REF_TierLegs321", [TIERLEGS(321)]))
PV = variants(P, "P_")
PV.append(("P_WR_FarstridersPlatedBracers331_MastCrit", ["wrist=,id=244584,bonus_id=12214/13667/12497/13751/14001/8960/13836,crafted_stats=49/32,crafting_quality=5,ilevel=331"]))
for tag, V in (("dung", DV), ("proj", PV)):
    L = ["name=A_current", "copy=Z_SANITY,A_current", "trinket2=,id=250228,bonus_id=13440/6652/12699/12846,ilevel=321"]
    for n, lines in V: L += [f"copy={n},A_current"] + lines
    open(f"{tag}_variants.simc","w").write("\n".join(L)+"\n")
    for fs, it in (("DungeonSlice",3000),("Patchwerk",5000)):
        open(f"run_{tag}_{fs}.simc","w").write(f"threads=4\niterations={it}\ndeterministic=1\nfight_style={fs}\n"
            f"input=../char_bm_2026-10-18.simc\ninput={tag}_variants.simc\n")
print(len(DV), len(PV))
