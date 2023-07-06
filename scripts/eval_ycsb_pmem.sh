#!/bin/bash

# Array of DB types for: FlatStore-PH, FlatStore-FF, and Viper
db_types=(2 3 5)

# Array of pacman settings: false, true
apply_pacman=(0 1)

# Loop over each db_type
for db_type in "${db_types[@]}"; do

  # Loop over each pacman setting
  for pacman in "${apply_pacman[@]}"; do

    # Define the log file name based on current configuration
    log_file="db_type_${db_type}_pacman_${pacman}.log"

    # Run eval_ycsb.sh with current configuration and redirect stdout and stderr to log file
    ./eval_ycsb.sh $db_type $pacman &> $log_file

    echo "Completed run for db_type: $db_type and pacman: $pacman. Log saved to $log_file."
  done
done

