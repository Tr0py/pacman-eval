#!/bin/bash

~/eval_with_resizing_pm.sh vpm-50-4-2-nopdf-flatstore-ph-etc "./eval_etc.sh 2 0"

~/eval_with_resizing_pm.sh vpm-50-4-2-nopdf-flatstore-ph-pacman-etc "./eval_etc.sh 2 1"

~/eval_with_resizing_pm.sh vpm-50-4-2-nopdf-flatstore-ff-etc "./eval_etc.sh 3 0"

~/eval_with_resizing_pm.sh vpm-50-4-2-nopdf-flatstore-ff-pacman-etc "./eval_etc.sh 3 1"

~/eval_with_resizing_pm.sh vpm-50-4-2-nopdf-chameleondb-etc "./eval_etc.sh 6 0"

~/eval_with_resizing_pm.sh vpm-50-4-2-nopdf-chameleondb-pacman-etc "./eval_etc.sh 6 1"

~/eval_with_resizing_pm.sh vpm-50-4-2-nopdf-pmemrocksdb-etc "./eval_etc.sh 7 0"
