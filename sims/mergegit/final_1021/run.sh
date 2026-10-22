#!/bin/bash
S=/tmp/claude-0/-home-user-free-code-camp/59fdf9c9-147a-5585-8fde-565a69b6c2c4/scratchpad/simc_mid/build/simc
cd "$(dirname "$0")"; mkdir -p bear/out
for f in bear/*.simc; do n=$(basename $f .simc); o=bear/out/$n.txt; grep -q "DTPS=" $o 2>/dev/null && continue; (cd bear && $S $n.simc > out/$n.txt 2>&1); done
[ -s out_bal_raid.txt ] && grep -q "DPS Ranking" out_bal_raid.txt || $S run_bal_raid.simc > out_bal_raid.txt 2>&1
touch combos.done
