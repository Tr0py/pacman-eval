#!/bin/bash

# Function to extract the number and its unit from a log file
extract_number () {
    num_unit=$(grep -o -P '(?<=items_per_second=)[0-9]*\.[0-9]*[kM]?' $1)
    num=${num_unit%[kM]*}
    unit=${num_unit#${num}}

    # Check if the unit is 'M' or 'm', if so convert to k (k/s)
    if [[ $unit == "M" || $unit == "m" ]]; then
        num=$(echo "$num * 1000" | bc)
    fi

    echo $num
}

# Function to format the number (add leading zero if necessary)
format_number () {
    printf "%0.5f" $1
}

# Directory name as input
dir_name=$1

# Change the working directory to the input directory
cd $dir_name

# Initialize a variable to hold the base value for normalization
base_value=0

# Prepare the CSV file with headers
echo "Available_PMEM(MB),Throughput(kops/s),Normalized_throughput,Normalized_overhead" > results.csv

# Iterate over the log files sorted by name in reverse order
for file in $(ls *.log | sort -Vr); do
    # Extract PMEM size from the file name
    pmem_size=${file##*-}
    pmem_size=${pmem_size%.*}

    # Extract the number from the log file
    value=$(extract_number $file)

    # If base value is not set (first iteration), set it
    if (( $(echo "$base_value == 0" |bc -l) )); then
        base_value=$value
    fi

    # Calculate normalized throughput
    normalized=$(echo "scale=5; $value / $base_value" | bc -l)

    # Calculate overhead
    overhead=$(echo "scale=5; 1 - $normalized" | bc -l)

    # Format the numbers
    value=$(format_number $value)
    normalized=$(format_number $normalized)
    overhead=$(format_number $overhead)

    # Append the data to the CSV file
    echo "$pmem_size,$value,$normalized,$overhead" >> results.csv
done

# Print message about CSV file creation
real_path=$(realpath results.csv)
echo "The results file has been generated and saved to $real_path"

# Print the content of the CSV file
column -t -s, $real_path

# After generating the csv file, plot the data
gnuplot -e "workload='$dir_name'" ../../plot.gp

# Print the real path of the figures
real_path_perf=$(realpath performance.pdf)
real_path_norm=$(realpath normalized_performance.pdf)
echo -e "The figures have been generated and saved to \n raw performance: $real_path_perf and \n normalized performance: $real_path_norm"

# Change back to the previous directory
cd ..

