import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from loguru import logger
import fire

def plot_throughput(csv_file, show_error_bars=True, rename_legend=None):
    # Read the CSV file into a dataframe
    merged_df = pd.read_csv(csv_file, index_col=0)

    # Filter the columns for averages and standard deviations
    avg_columns = merged_df.filter(like='_avg').columns
    std_columns = merged_df.filter(like='_std').columns
    configs = [col.replace('_avg', '') for col in avg_columns]  # Extract config names

    plt.style.use('seaborn-whitegrid')  # Clean grid style for conferences
    sns.set_palette('colorblind')  # Use colorblind-safe palette

    # Different styles for the two groups
    hatch_styles = ['', '', '//', '//', '//']  # First two with no hatch, last three with hatch
    colors = ['skyblue', 'lightgreen', 'orange', 'lightcoral', 'red']  # Group color scheme

    fig, ax = plt.subplots(figsize=(8, 4))  # Smaller figure size

    num_configs = len(configs)
    bar_width = 0.2  # Adjust the width of bars
    spacing_between_groups = 0.4  # Add extra spacing between different KV engines
    positions = np.arange(len(merged_df)) * (bar_width * num_configs + spacing_between_groups)

    # Plot each config's throughput with different styles for the two groups
    for idx, config in enumerate(configs):
        avg_col = f'{config}_avg'
        std_col = f'{config}_std'
        
        # Offset positions for each config to prevent overlap
        config_positions = positions + idx * bar_width  # Shift positions for each config

        ax.bar(
            config_positions,  # Shifted positions for each config
            merged_df[avg_col],
            yerr=merged_df[std_col] if show_error_bars else None,
            width=bar_width,
            capsize=4,
            color=colors[idx],  # Different color for each group
            edgecolor='black',
            label=config,
            hatch=hatch_styles[idx],  # Apply hatch style for different groups
            error_kw={'elinewidth': 1.5, 'ecolor': 'gray', 'capsize': 4}
        )

    # Customize the y-label, x-label, and rotate the x-ticks for better readability
    plt.ylabel("Throughput (ops/s)", fontsize=12)
    plt.xlabel("Key-Value Engines", fontsize=12)
    plt.xticks(positions + bar_width * (num_configs - 1) / 2, merged_df.index, rotation=30, ha='center')

    # Customizing legends and placing them in a less intrusive location
    if rename_legend:
        configs = rename_legend
        print(f"Renamed legends to: {configs}")

    # Customizing legends and placing them at the top in a single row
    plt.legend(configs, loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=len(configs))

    plt.tight_layout()

    # Saving the figure as a PDF
    pdf_name = "_".join(configs) + "_throughput.pdf"
    plt.savefig(pdf_name, format='pdf')
    logger.info(f"Figure saved to {pdf_name}")
    plt.show()

if __name__ == "__main__":
    fire.Fire()
