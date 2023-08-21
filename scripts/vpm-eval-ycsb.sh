#!/bin/bash

# Check if exactly two arguments are given
if [ "$#" -ne 2 ]; then
    echo "Error: You must enter exactly 2 arguments"
    echo "This script requires a script name and a task name."
    echo "Usage: $0 [script_name] [task_name]"
    echo "Example: $0 ./eval_baseline.sh vpm-50-4-2-nopdf"
    echo "Example: $0 ~/eval_with_resizing_pm.sh vpm-50-4-2-nopdf"
    exit 1
fi

# Assigning arguments to variables
script_name=$1
task_name=$2
data_folder="eval-data-ycsb"
log_folder=${data_folder}/${task_name}

mkdir -p ${log_folder}
cp ./eval_ycsb.sh ${log_folder}/config.cfg

# $ ./eval_ycsb.sh
# Usage: ./eval_ycsb.sh <db_type> <apply_pacman>
#   <db_type>: 1: FlatStore-H, 2: FlatStore-PH, 3: FlatStore-FF, 4: FlatStore-M,
#   5: Viper
#     <apply_pacman>: 0: false, 1: true


$script_name  ${log_folder}/flatstore-h-ycsb "./eval_ycsb.sh 1 0"
$script_name  ${log_folder}/flatstore-h-pacman-ycsb "./eval_ycsb.sh 1 1"
$script_name  ${log_folder}/flatstore-ph-ycsb "./eval_ycsb.sh 2 0"
$script_name  ${log_folder}/flatstore-ph-pacman-ycsb "./eval_ycsb.sh 2 1"
$script_name  ${log_folder}/flatstore-ff-ycsb "./eval_ycsb.sh 3 0"
$script_name  ${log_folder}/flatstore-ff-pacman-ycsb "./eval_ycsb.sh 3 1"
$script_name  ${log_folder}/viper-ycsb "./eval_ycsb.sh 5 0"
$script_name  ${log_folder}/viper-pacman-ycsb "./eval_ycsb.sh 5 1"
