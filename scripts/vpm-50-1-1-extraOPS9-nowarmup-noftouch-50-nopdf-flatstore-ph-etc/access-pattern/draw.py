import pandas as pd
import matplotlib.pyplot as plt
import sys
from matplotlib.ticker import MultipleLocator, FormatStrFormatter, FuncFormatter
from matplotlib.ticker import MaxNLocator

def plot_from_csv(filename):
    # Read data from CSV
    data = pd.read_csv(filename, converters={"fault_address": lambda x: int(x, 16)})
    #data = pd.read_csv(filename)
    #data = data[:10000]
    data["fault_address"] = data["fault_address"].astype(int)
    print(data)

    # Filter data by fault type
    major_faults = data[data["fault_type"] == 0]
    minor_faults = data[data["fault_type"] == 1]

    plt.figure(figsize=(10,5))
    # Plot data
    plt.scatter(major_faults["timestamp(s)"], major_faults["fault_address"], color='red', label='Major Faults')
    plt.scatter(minor_faults["timestamp(s)"], minor_faults["fault_address"], color='blue', label='Minor Faults')

    # Setting labels, title, and legend
    plt.xlabel("timestamp(s)")
    plt.ylabel("page fault address")
    plt.title("Page Faults Visualization")
    plt.legend()

    # Setting maximum number of ticks on the x and y axes
    num_ticks_x = 10  # for example
    num_ticks_y = 8   # for example

    ax = plt.gca()  # Get current axes
    ax.xaxis.set_major_locator(MaxNLocator(nbins=num_ticks_x))
    ax.yaxis.set_major_locator(MaxNLocator(nbins=num_ticks_y))

    plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%.3f'))

    '''
    # Set x-axis ticks step and precision
    x_step = 0.001  # For example, every 0.05 seconds
    plt.gca().xaxis.set_major_locator(MultipleLocator(x_step))
    plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%.2f'))

    # Set y-axis ticks step and precision
    y_step = 0x1000000  # For example, every 0x100000 in hexadecimal
    plt.gca().yaxis.set_major_locator(MultipleLocator(y_step))
    '''
    plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, y: hex(int(x))))


    # Save the figure as PDF
    output_filename = filename.split('.')[0] + '.png'
    plt.savefig(output_filename)
    print(f"output fig saved to {output_filename}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script_name.py csv_filename")
        sys.exit(1)

    filename = sys.argv[1]
    plot_from_csv(filename)

