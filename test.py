import csv
import time
import pickle
import os.path
import sys

from Probe import Probe
from ProbePoint import ProbePoint

probes = []
if os.path.isfile('ProbePoints.pickle'):
	# Read RAW
	start = time.perf_counter();
	with open('ProbePoints.pickle', 'rb') as rawFile:
		probes = pickle.load(rawFile)
	print("Loaded data from RAW in", time.perf_counter() - start, "seconds")
else:
	# Read CSV
	start = time.perf_counter();
	with open('../Partition6467ProbePoints.csv', newline='') as csvFile:
		reader = csv.reader(csvFile)
		currentProbeID = -1
		currentProbeIndex = -1
		for row in reader:
			rowProbeID = int(row[0])
			if rowProbeID != currentProbeID:
				currentProbeIndex += 1
				currentProbeID = rowProbeID
				probes.append(Probe(rowProbeID))
			probes[currentProbeIndex].append(row)
	print("Loaded data from CSV in", time.perf_counter() - start, "seconds")
	# Write RAW
	start = time.perf_counter();
	with open('ProbePoints.pickle', 'wb') as rawFile:
		pickle.dump(probes, rawFile, protocol=pickle.HIGHEST_PROTOCOL)
	print("Wrote data to RAW in", time.perf_counter() - start, "seconds")

print(len(probes))
print(len(probes[0].points))
print(sys.getsizeof(probes))
sum = sys.getsizeof(probes)
for probe in probes:
	sum += sys.getsizeof(probe)
	for point in probe.points:
		sum += sys.getsizeof(point)
print(sum)