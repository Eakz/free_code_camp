#!/bin/bash
S=/tmp/claude-0/-home-user-free-code-camp/59fdf9c9-147a-5585-8fde-565a69b6c2c4/scratchpad/simc_mid/build/simc
cd "$(dirname "$0")"
until [ -f ../bear_1021/tal.done ]; do sleep 15; done
$S run_gear_raid.simc > out_gear_raid.txt 2>&1
$S run_gear_mplus.simc > out_gear_mplus.txt 2>&1
touch gear.done
