import os.path
import shelve
import time

import Loader
import MapMatcher

# Load data from CSVs if not pre-loaded
if not os.path.isfile('LinksShelf.dat'):
	Loader.loadLinks()
if not os.path.isfile('ProbePointsShelf.dat'):
	Loader.loadProbePoints()

start = time.perf_counter()
count = 0
with shelve.open('ProbePointsShelf', writeback=True) as probeDB:
	with shelve.open('LinksShelf', writeback=True) as linkDB:
		for probe in probeDB:
			for probePoint in probeDB[probe]:
				matchedLinkData = MapMatcher.mapMatch(probePoint, linkDB)
				count += 1
				if count % 10000 == 0:
					print(count, "probe points processed after", time.perf_counter() - start, "seconds")