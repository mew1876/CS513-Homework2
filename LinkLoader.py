import csv
import time
import shelve
import os.path

GRID_DIMENSION = 20

from Link import Link

links = []
if not os.path.isfile('LinksShelf.dat'):	# build the shelf
	# Read CSV
	start = time.perf_counter();
	print("creating link shelf...")
	with open('../Partition6467LinkData.csv', newline='') as csvFile:
		reader = csv.reader(csvFile)
		maxLatitude = None
		minLatitude = None
		maxLongitude = None
		minLongitude = None
		for row in reader:
			# print("row: " + str(row))
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

		# loop through all links and put them in their grid square's mapping
		for link in links:
			gridX = int((link.shapeInfo[0][0] - linkDB["min"][0])/linkDB["step"][0])
			gridY = int((link.shapeInfo[0][1] - linkDB["min"][0])/linkDB["step"][1])
			if f"{gridX},{gridY}" not in linkDB:
				linkDB[f"{gridX},{gridY}"] = []
			linkDB[f"{gridX},{gridY}"].append(link)
		linkDB.close()
	print("Loaded data from link CSV into a shelf", time.perf_counter() - start, "seconds")
# oops I accidentally build a shelf

