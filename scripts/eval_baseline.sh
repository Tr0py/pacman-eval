#!/bin/bash

set -e

NAME=$1
CMD=$2
LOG_DIR=$NAME
SUFFIX=vpmbaseline

if [ -z "$1" ]
then
	echo "Usage: $0 <task_name> <command-wrapped-with-\">"
	exit 1
fi

mkdir -p $LOG_DIR

echo "Got task name $NAME, command $CMD"

LOG_FILE=$LOG_DIR/$NAME-$SUFFIX.log
echo -n "Init done. Current time:"
date
echo "Executing commands, output written to logfile: $LOG_FILE"
/usr/bin/time $CMD &> ./$LOG_FILE
