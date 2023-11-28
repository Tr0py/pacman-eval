#!/bin/bash

for folder in $(ls); do
	pushd ./$folder
	for file in *.log; do mv "$file" "${file##*-}"; done
	rm *.pdf *.csv
	popd
done;
