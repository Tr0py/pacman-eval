#!/bin/bash

# Directory name as input
dir_name=$1

# Change the working directory to the input directory
cd $dir_name

for workload in $(ls); do
	echo "===============Results for $workload================"
	../show_etc_results_single.sh $workload
done

