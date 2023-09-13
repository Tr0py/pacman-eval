#!/bin/bash

# Evaluate page fault count per second
sudo ~/bin/perf stat -e page-faults,major-faults,minor-faults -I 1000 ./eval_etc.sh 2 1

# Trace page fault reasons and addresses
sudo ~/bin/perf trace -F all ./eval_etc.sh 2 1
