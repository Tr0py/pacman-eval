import os
import re
import pandas as pd
import argparse
import glob

def get_throughput(path, filename_suffix):
    # Get all files in the path ending with the suffix, for both possible patterns
    files = glob.glob(os.path.join(path, f"*{filename_suffix}.log"))
    if len(files) == 0:
        files = glob.glob(os.path.join(path, f"{filename_suffix}.log"))
    if len(files) == 0:
        print(f"cannot find {path}/{filename_suffix}.log")
        return None

    # Assume the first file if multiple are found
    filename = files[0]
    
    # Extract throughput from file
    with open(filename, 'r') as file:
        contents = file.read()
    match = re.search('items_per_second=([0-9]*\.[0-9]*[Mk]/s)', contents)
    if match:
        throughput = match.group(1)
        # Convert to M/s if necessary
        if 'k/s' in throughput:
            throughput = float(throughput.replace('k/s', '')) / 1000
        else:
            throughput = float(throughput.replace('M/s', ''))
        
        print(f"File: {filename}, Throughput: {throughput}M/s")
        return throughput
    return None

def main(config, workload):
    engines = ["flatstore-ff", "flatstore-ff-pacman", "flatstore-ph", "flatstore-ph-pacman", "chameleondb", "chameleondb-pacman", "pmemrocksdb"]

    results = []
    for engine in engines:
        path = f"{config}-{engine}-{workload}"
        if not os.path.exists(path):
            print(f"Directory {path} does not exist. Skipping.")
            continue

        pm_throughput = get_throughput(path, 'pmbaseline')
        vp_throughput = get_throughput(path, 'vpmbaseline')
        if pm_throughput is None or vp_throughput is None:
            print(f"Could not extract throughput data from log files in {path}. Skipping.")
            continue

        overhead = 1 - (vp_throughput / pm_throughput)
        results.append([engine, pm_throughput, vp_throughput, overhead])

    # Save to csv
    df = pd.DataFrame(results, columns=["engine", "pmbaseline", "vpmbaseline", "virtualization_overhead"])
    output_file = os.path.join(os.getcwd(), f"{config}-virtualization-overhead.csv")
    df.to_csv(output_file, index=False)

    # Print CSV file contents
    print(df.to_string(index=False))

    print(f"\nThe CSV file has been saved to: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate and save virtualization overheads.")
    parser.add_argument("config", help="The config prefix.")
    parser.add_argument("workload", help="The workload suffix.")
    args = parser.parse_args()
    
    if not args.config or not args.workload:
        parser.print_usage()
    else:
        main(args.config, args.workload)

