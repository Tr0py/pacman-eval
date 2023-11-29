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
plt.figure(figsize=(2.5, 2.5),  constrained_layout=True)
plt.ylim(ymin=1.2, ymax=1.7)
plt.xlim(xmin=0, xmax=60)
plt.plot(time_seconds, throughput_ops)
plt.xlabel('Time (s)')
plt.ylabel('Throughput (Mops/s)')
# plt.title('Application Throughput Over Time')
plt.grid(True)
plt.savefig(f'{file_name}.pdf', format='pdf')  # Save to PDF

