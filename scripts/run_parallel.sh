#!/bin/bash

set -ex

#for ((i=1; i<6; i++)); do
for ((i=7; i<9; i++)); do
	~/clean-up-pmem.sh
	#./repeat.sh "numactl --cpunodebind=0   ../build/benchmarks/pacman_bench --benchmark_repetitions=1 --benchmark_filter=/(50)/.*/threads:(4)$   --benchmark_out=../results/etc_3_0 --benchmark_out_format=json" $i &> log_parallel_pmbaseline_$i.log
	./repeat.sh "numactl --physcpubind=0-7,16-23,24-31,32-39,48-55,56-63   ../build/benchmarks/pacman_bench --benchmark_repetitions=1 --benchmark_filter=/(50)/.*/threads:(1)$   --benchmark_out=../results/etc_3_0 --benchmark_out_format=json" $i &> log_parallel_vpm_$i.log
done
