import os.path
import shelve

import Loader
import MapMatcher

# Load data from CSVs if not pre-loaded
if not os.path.isfile('LinksShelf.dat'):
	Loader.loadLinks()
if not os.path.isfile('ProbePointsShelf.dat'):
	Loader.loadProbePoints()

with shelve.open('ProbePointsShelf', writeback=True) as probeDB:
	for probe in probeDB:
		for probePoint in probeDB[probe]:
			matchedLink = MapMatcher.mapMatch(probePoint)
