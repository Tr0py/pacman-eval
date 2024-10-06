#!/usr/bin/env python

import os
import re
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from loguru import logger
import seaborn as sns

# Regular expression to capture throughput in the format 'items_per_second=x.xM/s or x.xk/s'
throughput_pattern = re.compile(r'items_per_second=([\d.]+)([Mk])/s')

def parse_throughput(log_file):
    with open(log_file, 'r') as f:
        for line in f:
            match = throughput_pattern.search(line)
            if match:
                value = float(match.group(1))
                unit = match.group(2)
                if unit == 'M':
                    return value * 1e6  # Convert to operations per second
                elif unit == 'k':
                    return value * 1e3  # Convert to operations per second
    return None

def collect_data(config):
    engines_data = {}
    logger.info(f"Processing config: {config}")

    for engine_dir in os.listdir(config):
        engine_path = os.path.join(config, engine_dir)
        if os.path.isdir(engine_path):
            throughputs = []
            logger.info(f"Processing engine: {engine_dir}")
            for log_file in os.listdir(engine_path):
                if log_file.endswith('.log'):
                    log_path = os.path.join(engine_path, log_file)
                    throughput = parse_throughput(log_path)
                    if throughput:
                        throughputs.append(throughput)
                        logger.debug(f"Found throughput: {throughput} ops/s in {log_file}")
            
            if throughputs:
                avg_throughput = np.mean(throughputs)
                std_throughput = np.std(throughputs)
                engines_data[engine_dir] = {'avg_throughput': avg_throughput, 'std_throughput': std_throughput}
                logger.info(f"Engine: {engine_dir}, Avg throughput: {avg_throughput:.2f}, Std: {std_throughput:.2f}")
            else:
                logger.warning(f"No valid throughput data found for {engine_dir}")
    
    return engines_data

def merge_dataframes(all_data, configs):
    merged_data = pd.DataFrame()

    for config in configs:
        # Extract data from all_data for this config
        config_data = all_data[config]
        df_config = pd.DataFrame(config_data).T
        df_config.columns = [f'{config}_avg', f'{config}_std']
        
        # Merge with the existing dataframe
        if merged_data.empty:
            merged_data = df_config
        else:
            merged_data = pd.concat([merged_data, df_config], axis=1)
    
    return merged_data


def plot_throughput(merged_df, configs, show_error_bars=True, rename_legend=None):
    # Filter the columns for averages and standard deviations
    avg_columns = merged_df.filter(like='_avg').columns
    std_columns = merged_df.filter(like='_std').columns

    plt.style.use('seaborn-whitegrid')  # Clean grid style for conferences
    sns.set_palette('colorblind')  # Use colorblind-safe palette

    # Plotting the throughput with error bars
    ax = merged_df[avg_columns].plot(
        kind='bar',
        yerr=merged_df[std_columns] if show_error_bars else None,
        capsize=4,
        figsize=(8, 5),  # Smaller figure size
        legend=True,
        edgecolor='black',  # Add borders around bars
        error_kw={'elinewidth': 1.5, 'ecolor': 'gray', 'capsize': 4}  # Thinner error bars
    )

    # Adding data labels with a slight x-offset to avoid overlap
    # bar_width = 0.8 / len(configs)  # Adjust width for multiple configs
    # for idx, config in enumerate(configs):
    #     avg_col = f'{config}_avg'
    #     for i, avg in enumerate(merged_df[avg_col]):
    #         # Add x-offset to separate labels for each config
    #         ax.text(i + idx * bar_width - bar_width / 2, avg + merged_df[std_columns[idx]].iloc[i] * 0.05, 
    #                 f'{avg/1e6:.1f}M', ha='center', va='bottom', fontsize=9)

    plt.ylabel("Throughput (ops/s)", fontsize=12)
    plt.xlabel("Key-Value Engines", fontsize=12)
    plt.xticks(rotation=45, ha='center')

    # Customizing legends and placing them in a less intrusive location
    if rename_legend:
        configs = rename_legend
    plt.legend(configs, loc='upper right')
    plt.tight_layout()

    # Saving the figure as a PDF
    pdf_name = "_".join(configs) + "_throughput.pdf"
    plt.savefig(pdf_name, format='pdf')
    logger.info(f"Figure saved to {pdf_name}")
    plt.show()

def main(configs):
    all_data = {}

    for config in configs:
        logger.info(f"Processing config: {config}")
        config_data = collect_data(config)
        all_data[config] = config_data

    # Merge dataframes from all configs
    merged_df = merge_dataframes(all_data, configs)
    
    # Save the merged dataframe to CSV
    csv_name = "_".join(configs) + "_throughput.csv"
    merged_df.to_csv(csv_name)
    logger.info(f"Data saved to {csv_name}")
    
    # Plotting the merged dataframe
    plot_throughput(merged_df, configs)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <config1> <config2> ...")
        sys.exit(1)

    configs = sys.argv[1:]
    logger.info("Starting throughput analysis")
    main(configs)

