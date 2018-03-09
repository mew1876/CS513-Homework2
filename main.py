import os.path
import shelve
import time
import csv
import math

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
with shelve.open('ProbePointsShelf', flag ='r', writeback=True) as probeDB:
	with shelve.open('LinksShelf', flag = 'r', writeback=True) as linkDB:
		# for group in linkDB:
		# 	if group == "min" or group == "step":
		# 		continue
		# 	for links in linkDB[group]:
		# 		print(links.slopeInfo)

		for probe in probeDB:
			for probePoint in probeDB[probe]:
				matchedLinkData = MapMatcher.mapMatch(probePoint, linkDB)
				if matchedLinkData is None:
					continue
				if matchedLinkData[0].ID not in probePointMatches:
					probePointMatches[matchedLinkData[0].ID] = []
				probePointMatches[matchedLinkData[0].ID].append([probePoint,matchedLinkData[1],matchedLinkData[2],probe,matchedLinkData[0],[]]) 
				# save probe point info linklID = [[point,distancefromPointtoLink,distanceFromStartNode, probeID],[]...] in link's dictionary entry
				# if(count <= 10):
				# 	print(matchedLinkData[0].slopeInfo)
				count += 1
				if count % 10000 == 0:
					print(count, "probe points processed after", time.perf_counter() - start, "seconds")
		for link in probePointMatches:
			if len(probePointMatches[link]) <= 1:
				continue
			prevMatchInfo = None
			linkPointIndex = 0 # todo: we need to figure out where we are all the time
			linkPointSlope = None

			# print("ORIG", probePointMatches[link])

			# print(probePointMatches[link])
			# print("BEFORE",probePointMatches[link][0][4].slopeInfo)
			probePointMatches[link].sort(key = lambda match: match[2])

			for matchInfo in probePointMatches[link]: # key = distanceFromStartNode
				currentSlopeInfo = matchInfo[4].slopeInfo

				matchInfo[5] = [None] * len(currentSlopeInfo)

				# print("CURRENT", currentSlopeInfo[0])
				# print("IN LOOP",probePointMatches[link][0][4].slopeInfo)

				if currentSlopeInfo[0][0] == None:
					continue

				slope = None
				if prevMatchInfo is None:
					prevMatchInfo = matchInfo # todo: do we need this or should we save the values we use instead?
					continue
				for v in range(linkPointIndex,len(currentSlopeInfo)):
					# print("lpi",linkPointIndex,"v",v)
					# linkPointSlope = link.slopeInfo[v][0]
					if currentSlopeInfo[v][0] < prevMatchInfo[2]:
						linkPointIndex = v+1
					elif currentSlopeInfo[v][0] > matchInfo[2]:
						# print("otherberak")
						break
					else:
						if slope is None:
							# calculate slope between the 2 matched points
							if matchInfo[2] - prevMatchInfo[2] == 0:
								# print("break")
								break
							slope = math.degrees(math.atan((matchInfo[0].altitude - prevMatchInfo[0].altitude) / (matchInfo[2] - prevMatchInfo[2])))
							# print(slope)
						# save slope!
						# if len(currentSlopeInfo[v]) < 3:
						# 	currentSlopeInfo[v].append(None)	
						# currentSlopeInfo[v][2](slope)
						# print("SET SLOPE")
						matchInfo[5][v] = slope / 90
						# print(v, len(currentSlopeInfo), matchInfo[5])
		# output to csv
		with open('mapMatches.csv', 'w', newline='') as matchedCSV:
			matchedCSVWriter = csv.writer(matchedCSV, delimiter=',', quoting=csv.QUOTE_MINIMAL)
			for link in probePointMatches:
				for match in probePointMatches[link]:
					probeID = match[3] # probePoint.probeID
					probePointLat = match[0].latitude
					probePointLong = match[0].longitude
					matchedLinkID = match[4].ID
					distanceToLink = match[1]
					matchedCSVWriter.writerow([str(probeID),str(probePointLat),str(probePointLong),str(matchedLinkID),str(distanceToLink)])
		with open('slopeMatches.csv', 'w', newline='') as slopeCSV:
			slopeCSVWriter = csv.writer(slopeCSV, delimiter=',', quoting=csv.QUOTE_MINIMAL)
			for link in probePointMatches:
				for matchInfo in probePointMatches[link]:
					# print(matchInfo[5])
					for i, slopeInfoValue in enumerate(matchInfo[4].slopeInfo):
						if len(matchInfo[5]) == 0 or slopeInfoValue[0] is None or len(slopeInfoValue)<2:
							continue
						linkID = matchInfo[4].ID
						distanceFromStartNode = slopeInfoValue[0]
						linkSlope = slopeInfoValue[1]
						# calculatedSlope = slopeInfoValue[2]
						calculatedSlope = matchInfo[5][i]
						if calculatedSlope is not None:
							slopeCSVWriter.writerow([str(linkID),str(distanceFromStartNode),str(linkSlope),str(calculatedSlope)])
		linkDB.close()
	# end linkDB with
	probeDB.close()
#end probeDB with