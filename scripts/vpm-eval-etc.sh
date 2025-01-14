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

$script_name  ${task_name}-flatstore-ph-etc "./eval_etc.sh 2 0"
$script_name  ${task_name}-flatstore-ph-pacman-etc "./eval_etc.sh 2 1"
$script_name  ${task_name}-flatstore-ff-etc "./eval_etc.sh 3 0"
$script_name  ${task_name}-flatstore-ff-pacman-etc "./eval_etc.sh 3 1"
#$script_name  ${task_name}-chameleondb-etc "./eval_etc.sh 6 0"
#$script_name  ${task_name}-chameleondb-pacman-etc "./eval_etc.sh 6 1"
#$script_name  ${task_name}-pmemrocksdb-etc "./eval_etc.sh 7 0"

