import csv
import sys

def process_log_file(input_file, output_file):
    with open(input_file, 'r') as f, open(output_file, 'w', newline='') as out:
        writer = csv.writer(out)
        writer.writerow(["timestamp(s)", "fault_type", "fault_address"])

        for line in f:
            # Split by space and strip leading/trailing whitespaces
            parts = line.strip().split()

            # Convert timestamp to seconds
            timestamp = float(parts[0]) / 1000

            # Check fault type
            fault_type = 0 if parts[5] == "majfault" else 1

            # Extract fault address
            fault_address = parts[8].split('@')[1]

            # Write the processed data to CSV
            writer.writerow([timestamp, fault_type, fault_address])

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python script_name.py input_filename output_filename")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    process_log_file(input_file, output_file)

