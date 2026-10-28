#!/bin/bash
# resumable single-actor runner. usage: run.sh <stage dir prefix: runs> ; runs both models
S=/tmp/claude-0/-home-user-free-code-camp/59fdf9c9-147a-5585-8fde-565a69b6c2c4/scratchpad/simc_mid/build/simc
cd "$(dirname "$0")"
for m in pull boss; do mkdir -p out_$m
  for f in runs_$m/*.simc; do n=$(basename $f .simc); o=out_$m/$n.txt
    grep -q "DTPS=" $o 2>/dev/null && continue
    (cd runs_$m && $S $n.simc > ../$o 2>&1)
  done
done
touch stage.done
