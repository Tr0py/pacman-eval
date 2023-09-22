#!/bin/bash

echo "setting ETC NOPS to $1"
sed -i "s/^NUM_OPS_PER_THREAD=[0-9]*/NUM_OPS_PER_THREAD=$1/g" ./eval_etc.sh
grep -e '^NUM_OPS_PER_THREAD=' ./eval_etc.sh
