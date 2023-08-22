#!/usr/bin/env python3

import matplotlib.pyplot as plt
import pandas as pd
import sys

# Check if the filename is provided
if len(sys.argv) < 2:
    print("Please provide the CSV filename as a command-line argument.")
    sys.exit()

# Number of lines to read
#num_lines = 1000

# Read the CSV file
file_name = sys.argv[1]
data = pd.read_csv(file_name, header=None)

# Extract the columns
time_seconds = data[0]
throughput_ops = data[1] / 1e6  # Convert to Mops/s

# Plot the figure
plt.plot(time_seconds, throughput_ops)
plt.xlabel('time (s)')
plt.ylabel('throughput (Mops/s)')
plt.title('Application Throughput Over Time')
plt.grid(True)
plt.savefig(f'{file_name}.pdf', format='pdf')  # Save to PDF

