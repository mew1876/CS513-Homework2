import shelve
import math

def mapMatch(probePoint):
	# fetch min and step for latitude and longitude to calculate necessary grid squares
	with shelve.open('LinksShelf', writeback=True) as linkDB:
		trueX = ((probePoint.latitude - linkDB["min"][0])/linkDB["step"][0])
		trueY = ((probePoint.longitude - linkDB["min"][1])/linkDB["step"][1])

		gridX = int(trueX)
		gridY = int(trueY)
		print("Point in grid square", gridX, gridY)
		neighborX = -1
		neighborY = -1
		if (trueX - gridX) >= 0.5:
			neighborX = 1
		if (trueY - gridY) >= 0.5:
			neighborY = 1

		# TODO: add angle to scores, do calcs with segments of links
		topScore = -1
		bestLink = None
		for link in linkDB[f"{gridX},{gridY}"] + linkDB[f"{gridX+neighborX},{gridY+neighborY}"] + linkDB[f"{gridX+neighborX},{gridY}"] + linkDB[f"{gridX},{gridY+neighborY}"]:
			currentDist = distToLine(link.shapeInfo[0], link.shapeInfo[len(link.shapeInfo) - 1], [probePoint.latitude, probePoint.longitude])
			if currentDist > topScore:
				topScore = currentDist
				bestLink = link
		print("Closest road is", topScore, "away")

def distToLine(p1, p2, p3): # dist from p3 to the line p2 - p1
	return abs((p2[1] - p1[1])*p3[0] - (p2[0] - p1[0])*p3[1] + p2[0]*p1[1] - p2[1]*p1[0]) / math.sqrt((p2[1] - p1[1]) ** 2 + (p2[0] - p1[0]) ** 2)

with shelve.open('ProbePointsShelf', writeback=True) as probeDB:
	probePoint = probeDB["3496"][0]
	mapMatch(probePoint)