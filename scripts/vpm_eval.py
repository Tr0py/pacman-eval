#!/usr/bin/env python3

import fire
import subprocess
import csv
import os
import pandas as pd

def shell(cmd) -> [int, str]:
    """
    Execute a shell command
    :param cmd: Command to execute
    :return: A list with the return code and the output (stdout + stderr)
    """
    cp = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return [cp.returncode, cp.stdout]

class eval:

	class init:
		def run(self) -> None:
			"""
			Run experiments that collect init phase data.
			"""
			# TODO: rewrite baseline name
			# TODO: use logging for debug / info
			shell("./vpm-eval-etc.sh ./eval_baseline.sh eval_init")
			return

		def draw(self) -> None:
			"""
			Generate csv and figre based on init evaluation logs in eval_init*/*.log.
			"""
			self.gen_log()
			self.gen_csv('init.log')
			return

		def gen_log(self) -> None:
			shell("grep -oE 'DB .* finished in .* seconds' eval_init*/*.log > init.log")
			return

		def gen_csv(self, filepath):
			"""
			Generate a CSV file from a log file
			:param filepath: Path to the log file
			:return: None
			"""
			# Data structure to hold the extracted information
			db_data = {}

			# Open the file and read its contents
			with open(filepath, 'r') as file:
				for line in file:
					parts = line.split(':')
					log_filename = parts[0].split('/')[-1]
					operation = parts[1].split(' ')[1]
					time_taken = float(parts[1].split(' ')[-2])
					db_name = '-'.join(parts[0].split('-')[1:-1])
					#print(f"Log: {log_filename}, Operation: {operation}, Time taken: {time_taken}, DB Name: {db_name}")

					if db_name not in db_data:
						db_data[db_name] = {}

					# Checking if the log is for pm or vpm
					if 'pmbaseline.log' == log_filename:
						db_data[db_name][operation + '_pm'] = time_taken
					elif 'vpmbaseline.log' == log_filename:
						db_data[db_name][operation + '_vpm'] = time_taken
			#print(db_data)

			# Organize data for DataFrame
			data = []
			for db_name, values in db_data.items():
				row = [db_name]
				for phase in ['init', 'load', 'warmup']:
					pm = values.get(phase + '_pm', 0)
					vpm = values.get(phase + '_vpm', 0)
					#print(f"{values=} pm: {pm}, vpm: {vpm}")
					diff_s = vpm - pm
					diff_percent = (diff_s / pm) * 100 if pm != 0 else 0
					row.extend([pm, vpm, diff_s, diff_percent])
				data.append(row)

			# Define columns for DataFrame
			columns = ['DB Name']
			for phase in ['init', 'load', 'warmup']:
				columns.extend([phase + ' pm', phase + ' vpm', phase + ' diff(s)', phase + ' diff(%)'])

			# Create DataFrame and write to CSV
			df = pd.DataFrame(data, columns=columns)
			csv_filepath = filepath.replace('.log', '.csv')
			df.to_csv(csv_filepath, index=False)

			print("CSV generated at:", os.path.realpath(csv_filepath))

if __name__ == "__main__":
    fire.Fire()
