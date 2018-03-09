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
			for i in range(0, len(link.shapeInfo) - 1):
				currentDist = distanceFromPointToSegment(link.shapeInfo[i], link.shapeInfo[i+1], [probePoint.latitude, probePoint.longitude])
				if currentDist > topScore:
					topScore = currentDist
					bestLink = link
		print("Closest road is", topScore, "away")

def distanceBetweenPointsSquared(point1, point2):
	return (point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2
def distanceFromPointToSegment(segmentStart, segmentEnd, point): # point = point, segment = segmentEnd - segmentStart
	# lengthSquared = distanceBetweenPointsSquared(segmentEnd,segmentStart)
	lengthSquared = kilometerDistanceFromPointToPoint(segmentEnd,segmentStart) ** 2
	if (lengthSquared == 0):
  		# return math.sqrt(distanceBetweenPointsSquared(point,segmentEnd))
  		return kilometerDistanceFromPointToPoint(point,segmentEnd)
	t = ((point[0] - segmentEnd[0]) * (segmentStart[0] - segmentEnd[0]) + (point[1] - segmentEnd[1]) * (segmentStart[1] - segmentEnd[1])) / lengthSquared
	t = max(0, min(1, t))
	# return math.sqrt(distanceBetweenPointsSquared(point, [segmentEnd[0] + t * (segmentStart[0] - segmentEnd[0]), segmentEnd[1] + t * (segmentStart[1] - segmentEnd[1])]))
	return kilometerDistanceFromPointToPoint(point,[segmentEnd[0] + t * (segmentStart[0] - segmentEnd[0]), segmentEnd[1] + t * (segmentStart[1] - segmentEnd[1])])

def kilometerDistanceFromPointToPoint(point1, point2):
	R = 6373.0 # approximate radius of earth in km
	lat1 = math.radians(point1[0])
	lon1 = math.radians(point1[1])
	lat2 = math.radians(point2[0])
	lon2 = math.radians(point2[1])
	dlon = lon2 - lon1
	dlat = lat2 - lat1
	a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
	c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
	distance = R * c
	return distance

def greatCircleAngle(point1,point2):
	lat1 = math.radians(point1[0])
	lon1 = math.radians(point1[1])
	lat2 = math.radians(point2[0])
	lon2 = math.radians(point2[1])
	dlon = lon2 - lon1
	dlat = lat2 - lat1
	return math.atan(math.sqrt(	(math.cos(lat2)*math.sin(dlon))**2  +  (math.cos(lat1)*math.sin(lat2) - math.sin(lat1)*math.cos(lat2)*math.cos(dlon))**2	)   /   (math.sin(lat1)*math.sin(lat2) + math.cos(lat1)*math.cos(lat2)*math.cos(dlon)))

def angleBetween(pointHeading, p1, p2): # angle between pointHeading and p4 - p3
	segmentHeading = math.degrees(math.atan2(p2[1] - p1[1], p2[0] - p1[0]))
	if segmentHeading < 0:
		segmentHeading += 360
	return abs(pointHeading - segmentHeading)

# with shelve.open('ProbePointsShelf', writeback=True) as probeDB:
# 	probePoint = probeDB["3496"][0]
# 	mapMatch(probePoint)
# 	# print(distanceFromPointToSegment([3,3],[-1,3],[0,1],))
# 	print(kilometerDistanceFromPointToPoint("",""))
print(6373.0 * greatCircleAngle([60,12],[50,9]))