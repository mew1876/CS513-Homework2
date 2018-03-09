import csv
import time
import shelve

from Link import Link
from ProbePoint import ProbePoint

GRID_DIMENSION = 1000

def loadLinks():
	start = time.perf_counter();
	print("creating link shelf...")
	links = []
	with open('../Partition6467LinkData.csv', newline='') as csvFile:
		reader = csv.reader(csvFile)
		maxLatitude = None
		minLatitude = None
		maxLongitude = None
		minLongitude = None
		for row in reader:
			tempLink = Link(row)
			links.append(tempLink)

			# find if leading point will be the min or max for latitude or longitude
			if minLatitude is None or tempLink.shapeInfo[0][0] < minLatitude: # latitude of first point is new min
				minLatitude = tempLink.shapeInfo[0][0]
			if maxLatitude is None or tempLink.shapeInfo[0][0] > maxLatitude: # latitude of first point is new max
				maxLatitude = tempLink.shapeInfo[0][0]
			if minLongitude is None or tempLink.shapeInfo[0][1] < minLongitude: # longitude of first point is new min
				minLongitude = tempLink.shapeInfo[0][1]
			if maxLongitude is None or tempLink.shapeInfo[0][1] > maxLongitude: # longitude of first point is new max
				maxLongitude = tempLink.shapeInfo[0][1]

	# save required step and minimum values to determine grid squares probe points belong in later
	latitudeStep = (maxLatitude - minLatitude)/GRID_DIMENSION
	longitudeStep = (maxLongitude - minLongitude)/GRID_DIMENSION
	with shelve.open('LinksShelf', writeback=True) as linkDB:
		linkDB["min"] = (minLatitude,minLongitude)
		linkDB["step"] = (latitudeStep,longitudeStep)

		# # loop through all links and put them in their grid square's mapping
		# for link in links:
		# 	gridX = int((link.shapeInfo[0][0] - linkDB["min"][0])/linkDB["step"][0])
		# 	gridY = int((link.shapeInfo[0][1] - linkDB["min"][1])/linkDB["step"][1])
		# 	if f"{gridX},{gridY}" not in linkDB:
		# 		linkDB[f"{gridX},{gridY}"] = []
		# 	linkDB[f"{gridX},{gridY}"].append(link)
		
		# loop thorugh all links and put them in all of their shape points' grid square mappings
		for link in links:
			gridSquares = []
			for point in link.shapeInfo:
				gridX = int((point[0] - linkDB["min"][0])/linkDB["step"][0])
				gridY = int((point[1] - linkDB["min"][1])/linkDB["step"][1])
				gridSquare = f"{gridX},{gridY}"
				if gridSquare not in gridSquares:
					gridSquares.append(gridSquare)
					if gridSquare not in linkDB:
						linkDB[gridSquare] = []
					# print(link.slopeInfo)
					linkDB[gridSquare].append(link)
			# for gridSquare in gridSquares:
			# 	if gridSquare not in linkDB:
			# 		linkDB[gridSquare] = []
			# 	linkDB[gridSquare].append(link)



		linkDB.close()
	print("Loaded link data in ", time.perf_counter() - start, "seconds")
	# oops I accidentally build a shelf

def loadProbePoints():
	start = time.perf_counter();
	with shelve.open('ProbePointsShelf', writeback=True) as probeDB:
		print("creating probe shelf...")
		with open('../Partition6467ProbePoints.csv', newline='') as csvFile:
			reader = csv.reader(csvFile)
			for row in reader:
				rowProbeID = row[0]
				if rowProbeID not in probeDB:
					probeDB[rowProbeID] = []
				probeDB[rowProbeID].append(ProbePoint(row))
		probeDB.close()
	print("Loaded data from probe CSV into a shelf", time.perf_counter() - start, "seconds")
	# oops I accidentally build a shelf
