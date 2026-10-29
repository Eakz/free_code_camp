#!/bin/bash
# resumable single-actor runner: run_bear.sh <model: pull|boss>  (dirs runs_<model> -> out_<model>)
S=/tmp/claude-0/-home-user-free-code-camp/59fdf9c9-147a-5585-8fde-565a69b6c2c4/scratchpad/simc_mid/build/simc
cd "$(dirname "$0")"; m=$1; mkdir -p out_$m
for f in runs_$m/*.simc; do n=$(basename $f .simc); o=out_$m/$n.txt
  grep -q "DTPS=" $o 2>/dev/null && continue
  (cd runs_$m && $S $n.simc > ../$o 2>&1)
done
touch $m.done
