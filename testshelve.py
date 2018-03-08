import csv
import time
import shelve
import os.path
import sys

from Probe import Probe
from ProbePoint import ProbePoint

probes = []
if not os.path.isfile('ProbePointsShelf.dat'):	# build the shelf
	# Read CSV
	start = time.perf_counter();
	with shelve.open('ProbePointsShelf', writeback=True) as probeDB:
		print("creating shelf...")
		with open('../Partition6467ProbePoints.csv', newline='') as csvFile:
			reader = csv.reader(csvFile)
			for row in reader:
				# print("row: " + str(row))
				rowProbeID = row[0]
				if rowProbeID not in probeDB:
					probeDB[rowProbeID] = []
				probeDB[rowProbeID].append(row)
		probeDB.close()
	print("Loaded data from CSV into a shelf", time.perf_counter() - start, "seconds")
# oops I accidentally build a shelf

