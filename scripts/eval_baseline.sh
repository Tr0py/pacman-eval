#!/bin/bash

set -e

NAME=$1
CMD=$2
LOG_DIR=$NAME
SUFFIX=vpmbaseline
N_RUNS=3

if [ -z "$1" ]
then
	echo "Usage: $0 <task_name> <command-wrapped-with-\">"
	exit 1
fi

mkdir -p $LOG_DIR

echo "Got task name $NAME, command $CMD"

echo -n "Init done. Current time:"
for i in $(seq 1 $N_RUNS); do
	date
	LOG_FILE=$LOG_DIR/$SUFFIX-$i.log
	echo "Executing command, $i-th run, output written to logfile: $LOG_FILE"
	/usr/bin/time $CMD &> ./$LOG_FILE
done
