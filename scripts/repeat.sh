#!/bin/bash

run_parallel_cmds() {
    # Check if the correct number of arguments are provided
    # if [ "$#" -ne 2 ]; then
    #     echo "Usage: run_parallel_cmds <command> <repetitions>"
    #     return 1
    # fi

    local cmd="$1"
    local reps="$2"
    echo "cmd=$cmd reps=$reps"


    # Validate that repetitions is a positive integer
    if ! [[ "$reps" =~ ^[0-9]+$ ]] || [ "$reps" -le 0 ]; then
        echo "Error: <repetitions> must be a positive integer."
        return 1
    fi

    # Measure the total execution time
    time {
        for ((i=1; i<=reps; i++)); do
            $cmd &
        done

        # Wait for all background processes to complete
        wait
    }
}

# Example usage:
run_parallel_cmds "$1" "$2"

