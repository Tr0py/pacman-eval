#!/bin/bash

set_etc_nops() {
	echo "setting ETC NOPS to $1"
	sed -i "s/^NUM_OPS_PER_THREAD=[0-9]*/NUM_OPS_PER_THREAD=$1/g" ./eval_etc.sh
	grep -e '^NUM_OPS_PER_THREAD=' ./eval_etc.sh
}

mkdir -p ./warmup

for nops in $(seq 9 11); do
	nop=$((10**$nops))
	set_etc_nops $nop
	./eval_etc.sh 2 1 &> warmup/log-$nops
done
