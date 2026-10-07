#!/bin/bash
# Runs every queued sim for the 2026-10-07 21:24 profile, in order. Usage: run_queue.sh <path-to-simc>
S=$1; cd "$(dirname "$0")"
for job in topgear/run_p1 dungeons/run_jewel dungeons/run_trinket dungeons/run_armor dungeons/run_tier dungeons/run_weapon consumables/run_cons; do
  for fs in Patchwerk DungeonSlice; do
    d=$(dirname $job); b=$(basename $job)
    (cd $d && $S ${b}_${fs}.simc > out_${b#run_}_${fs}.txt 2>&1); echo "$job $fs $?" >> queue.log
  done
done
