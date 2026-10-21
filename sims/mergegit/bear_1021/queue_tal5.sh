#!/bin/bash
S=/tmp/claude-0/-home-user-free-code-camp/59fdf9c9-147a-5585-8fde-565a69b6c2c4/scratchpad/simc_mid/build/simc
cd "$(dirname "$0")"; mkdir -p out/tal5
for f in runs/tal5_*.simc; do n=$(basename $f .simc); n=${n#tal5_}; (cd runs && $S $(basename $f) > ../out/tal5/$n.txt 2>&1); done
touch tal5.done
