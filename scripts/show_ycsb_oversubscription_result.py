import os
import re
import pandas as pd
import argparse
import glob
import logging
import matplotlib.pyplot as plt

# Setup color logging
class ColorFormatter(logging.Formatter):
    yellow = "\033[33m"
    red = "\033[31m"
    reset = "\033[0m"
    format = "%(levelname)s: %(message)s"

    FORMATS = {
        logging.INFO: yellow + format + reset,
        logging.WARNING: red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(ColorFormatter())
logger.addHandler(ch)

def get_throughputs(path, filename):
    with open(os.path.join(path, filename), 'r') as file:
        contents = file.read()

    matches = re.findall('items_per_second=([0-9]*\.[0-9]*[Mk]/s)', contents)
    throughputs = ['N/A', 'N/A', 'N/A']
    for i, match in enumerate(matches):
        if 'k/s' in match:
            throughput = float(match.replace('k/s', '')) / 1000
        else:
            throughput = float(match.replace('M/s', ''))
        throughputs[i] = throughput
    if len(matches) < 3:
        logging.warning(f"Expected 3 throughputs in {os.path.join(path, filename)}, but found only {len(matches)}")
    logging.info(f"Throughputs in {os.path.join(path, filename)}: {throughputs}")
    return throughputs

def draw_figure(df, output_file, title):
    plt.figure(figsize=(10, 6))
    for i, row in df.iterrows():
        plt.plot(row.index[1:], row.values[1:], label=row.values[0])
    plt.title(title)
    plt.xlabel('Available PMEM sizes')
    plt.ylabel('Normalized Throughput')
    plt.legend()
    plt.grid(True)
    plt.savefig(output_file)
    plt.close()
    print(f"\nThe figure has been saved to: {os.path.realpath(output_file)}")

def main(config):
    base_dir = 'eval-data-ycsb'
    config_dir = os.path.join(base_dir, config)
    if not os.path.exists(config_dir):
        print(f"Directory {config_dir} does not exist.")
        return

    workloads = ["YCSB_A", "YCSB_B", "YCSB_C"]
    engines = [engine.replace('-ycsb', '') for engine in os.listdir(config_dir) if engine.endswith('-ycsb')]
    
    # Collect data
    collected_data = {}
    for engine in engines:
        engine_dir = os.path.join(config_dir, f"{engine}-ycsb")
        engine_data = {}
        for filename in os.listdir(engine_dir):
            if filename.endswith('.log'):
                size = int(filename.split('-')[0])
                engine_data[size] = get_throughputs(engine_dir, filename)
        collected_data[engine] = engine_data
    
    for workload in workloads:
        print(f"\n-------------------- {workload} --------------------")
        results = []
        results_normalized = []
        for engine, engine_data in collected_data.items():
            sizes = sorted(engine_data.keys())
            throughput_data = [engine_data[size][workloads.index(workload)] for size in sizes]
            max_throughput = max(tp for tp in throughput_data if tp != 'N/A')
            results.append([engine] + throughput_data)
            results_normalized.append([engine] + [(tp / max_throughput if tp != 'N/A' else 'N/A') for tp in throughput_data])

        # Save to csv
        sizes.insert(0, "engine")
        df = pd.DataFrame(results, columns=sizes)
        output_file = os.path.join(config_dir, f"oversubscription-{workload}.csv")
        df.to_csv(output_file, index=False)

        # Print CSV file contents
        print(df.to_string(index=False))

        print(f"\nThe CSV file has been saved to: {os.path.realpath(output_file)}")

        # Save normalized data to csv
        df_normalized = pd.DataFrame(results_normalized, columns=sizes)
        output_normalized_file = os.path.join(config_dir, f"oversubscription-normalized-{workload}.csv")
        df_normalized.to_csv(output_normalized_file, index=False)

        # Print CSV file contents
        print(df_normalized.to_string(index=False))

        print(f"\nThe normalized CSV file has been saved to: {os.path.realpath(output_normalized_file)}")

        # Draw and save figure
        figure_file = os.path.join(config_dir, f"oversubscription-{workload}.png")
        draw_figure(df_normalized, figure_file, f"Oversubscription Overhead\n{config}-{workload}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate and save virtualization overheads.")
    parser.add_argument("-c", "--config", help="The config prefix.", required=True)
    args = parser.parse_args()

    if not args.config:
        parser.print_usage()
        print("\nExample: python3 ./show_ycsb_oversubscription_result.py -c vpm-50-1-1-newdram-nopdf")
    else:
        main(args.config)

