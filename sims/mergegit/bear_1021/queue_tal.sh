#!/bin/bash
# runs after the Balance talent runs finish (4 cores, one sim at a time)
S=/tmp/claude-0/-home-user-free-code-camp/59fdf9c9-147a-5585-8fde-565a69b6c2c4/scratchpad/simc_mid/build/simc
cd "$(dirname "$0")"
until [ -f ../bal_1021/tal.done ]; do sleep 15; done
for tg in 1 5; do mkdir -p out/tal$tg; for f in runs/tal${tg}_*.simc; do n=$(basename $f .simc); n=${n#tal${tg}_}; (cd runs && $S $(basename $f) > ../out/tal$tg/$n.txt 2>&1); done; done
touch tal.done
