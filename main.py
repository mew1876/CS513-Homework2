import os.path
import shelve
import time
import csv

import Loader
import MapMatcher

# Load data from CSVs if not pre-loaded
if not os.path.isfile('LinksShelf.dat'):
	Loader.loadLinks()
if not os.path.isfile('ProbePointsShelf.dat'):
	Loader.loadProbePoints()

start = time.perf_counter()
count = 0
probePointMatches = {}
with shelve.open('ProbePointsShelf', writeback=True) as probeDB:
	with shelve.open('LinksShelf', writeback=True) as linkDB:
		for probe in probeDB:
			for probePoint in probeDB[probe]:
				matchedLinkData = MapMatcher.mapMatch(probePoint, linkDB)
				if matchedLinkData is None:
					continue
				if matchedLinkData[0].ID not in probePointMatches:
					probePointMatches[matchedLinkData[0].ID] = []
				probePointMatches[matchedLinkData[0].ID].append([probePoint,matchedLinkData[1],matchedLinkData[2],probe]) # save probe point info [point,distancefromPointtoLink,distanceFromStartNode, probeID] in link's dictionary entry
				count += 1
				if count % 10000 == 0:
					print(count, "probe points processed after", time.perf_counter() - start, "seconds")
		for link in probePointMatches:
			if len(probePointMatches[link]) <= 1:
				continue
			prevMatchInfo = None
			linkPointIndex = 0 # todo: we need to figure out where we are all the time
			linkPointSlope = None
			lenLinkPoints = len(link.slopeInfo)
			for matchInfo in sort(probePointMatches[link], key = lambda match: match[2]): # key = distanceFromStartNode
				slope = None
				if prevMatchInfo is None:
					prevMatchInfo = matchInfo # todo: do we need this or should we save the values we use instead?
					continue
				for i in range(linkPointIndex,lenLinkPoints):
					# linkPointSlope = link.slopeInfo[i][0]
					if link.slopeInfo[i][0] < prevMatchInfo[2]:
						linkPointIndex = i+1
					elif link.slopeInfo[i][0] > matchInfo[2]:
						break
					else:
						if slope is None:
							# calculate slope between the 2 matched points
							slope = (matchInfo[0].altitude - prevMatchInfo[0].altitude) / (matchInfo[2] - prevMatchInfo[2])
						# save slope!
						link.slopeInfo[i].append(slope)
		# output to csv
		with open('mapMatches.csv', 'w', newline='') as matchedCSV:
			matchedCSVWriter = csv.writer(matchedCSV, delimiter=',', quoting=csv.QUOTE_MINIMAL)
			for link in probePointMatches:
				for match in probePointMatches[link]:
					probeID = match[3] # probePoint.probeID
					probePointLat = match[0].latitude
					probePointLong = match[1].longitude
					matchedLinkID = link.ID
					distanceToLink = match[1]
					matchedCSVWriter.writerow([str(probeID),str(probePointLat),str(probePointLong),str(matchedLinkID),str(distanceToLink)])
		with open('slopeMatches.csv', 'w', newline='') as slopeCSV:
			slopeCSVWriter = csv.writer(slopeCSV, delimiter=',', quoting=csv.QUOTE_MINIMAL)
			for link in linkDB:
				for slopeInfoValue in link.slopeInfo:
					if len(slopeInfoValue) < 3: 
						continue
					linkID = link.ID
					distanceFromStartNode = slopeInfoValue[0]
					linkSlope = slopeInfoValue[1]
					calculatedSlope = slopeInfoValue[2]
					distancefromPointtoLink = probePointMatches[link][1]
					slopeCSVWriter.writerow([str(linkID),str(distanceFromStartNode),str(linkSlope),str(calculatedSlope),str(distanceFromPointtoLink)])
		linkDB.close()						
	probeDB.close()