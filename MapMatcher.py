import shelve
import math

DISTANCE_ANGLE_WEIGHT = 0.5


# compare slopes
# 	probe point slope
# 		elevation AND elevation of next and/or previous probe point
# 	matched link shape point
# 		save link and shape point that probe point matched to
# 	link shape point slope
# 		slope from slopeInfo
# 			distance from reference node - trust slopeInfo!!!!!!

# snap to shapeInfo points? or no? -- NO
# get real distance from ref node to map matched point
# 	for every link we go to
# 	if it has 2 or more mapped points on it
# 		go to every pair of mapped points on the link and get the slope between them
# 		then any slope info point between those takes on the slope that is calculated




def mapMatch(probePoint, linkDB): # returns (link, distanceAway, relativeAngle) for the chosen link
	# fetch min and step for latitude and longitude to calculate necessary grid squares
	# with shelve.open('LinksShelf', writeback=True) as linkDB:
	trueX = ((probePoint.latitude - linkDB["min"][0])/linkDB["step"][0])
	trueY = ((probePoint.longitude - linkDB["min"][1])/linkDB["step"][1])

	gridX = int(trueX)
	gridY = int(trueY)

	neighborX = -1
	neighborY = -1
	if (trueX - gridX) >= 0.5:
		neighborX = 1
	if (trueY - gridY) >= 0.5:
		neighborY = 1

	bestScore = None
	bestLink = None

	if f"{gridX},{gridY}" not in linkDB:
		return None

	neighborhoodLinks = linkDB[f"{gridX},{gridY}"]
	for coords in [f"{gridX+neighborX},{gridY+neighborY}", f"{gridX+neighborX},{gridY}", f"{gridX},{gridY+neighborY}"]:
		if coords in linkDB:
			neighborhoodLinks = neighborhoodLinks + linkDB[coords]

	for link in neighborhoodLinks:
		distfromRefNode = 0
		for i in range(0, len(link.shapeInfo) - 1):
			currentDist = distanceFromPointToSegment(link.shapeInfo[i], link.shapeInfo[i+1], [probePoint.latitude, probePoint.longitude])
			currentAngle = angleBetween(probePoint.heading, link.shapeInfo[i], link.shapeInfo[i+1])
			score = DISTANCE_ANGLE_WEIGHT * currentDist + (1 - DISTANCE_ANGLE_WEIGHT) * currentAngle
			if bestScore is None or score < bestScore:
				bestScore = score
				bestLink = (link, currentDist, currentAngle)

	return bestLink

def distanceBetweenPointsSquared(point1, point2):
	return (point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2
def distanceFromPointToSegment(segmentStart, segmentEnd, point): # point = point, segment = segmentEnd - segmentStart
	# convert to radians
	segmentStart = [math.radians(segmentStart[0]), math.radians(segmentStart[1])]
	segmentEnd = [math.radians(segmentEnd[0]), math.radians(segmentEnd[1])]
	point = [math.radians(point[0]), math.radians(point[1])]

	# adjust longitude to be on same scale as latitude
	segmentStart[1] *= math.cos(segmentStart[0])
	segmentEnd[1] *= math.cos(segmentEnd[0])
	point[1] *= math.cos(point[0])

	latDiff = segmentStart[0] - segmentEnd[0]
	longDiff = segmentStart[1] - segmentEnd[1]

	lengthSquared = latDiff ** 2 + longDiff ** 2
	if (lengthSquared == 0):
  		return 6373.0 * math.sqrt((point[0] - segmentEnd[0]) ** 2 + (point[1] - segmentEnd[1]) ** 2)
	t = ((point[0] - segmentEnd[0]) * latDiff + (point[1] - segmentEnd[1]) * longDiff) / lengthSquared
	t = max(0, min(1, t))
	return 6373.0 * math.sqrt(distanceBetweenPointsSquared(point, [segmentEnd[0] + t * latDiff, segmentEnd[1] + t * longDiff]))

def greatCircleAngle(point1,point2):
	lat1 = math.radians(point1[0])
	lon1 = math.radians(point1[1])
	lat2 = math.radians(point2[0])
	lon2 = math.radians(point2[1])
	dlon = lon2 - lon1
	dlat = lat2 - lat1
	return math.atan(math.sqrt(	(math.cos(lat2)*math.sin(dlon))**2  +  (math.cos(lat1)*math.sin(lat2) - math.sin(lat1)*math.cos(lat2)*math.cos(dlon))**2	)   /   (math.sin(lat1)*math.sin(lat2) + math.cos(lat1)*math.cos(lat2)*math.cos(dlon)))

def angleBetween(pointHeading, p1, p2): # angle between pointHeading and p2 - p1
	segmentHeading = math.degrees(math.atan2(p2[1] - p1[1], p2[0] - p1[0]))
	if segmentHeading < 0:
		segmentHeading += 360
	return abs(pointHeading - segmentHeading)

# with shelve.open('ProbePointsShelf', writeback=True) as probeDB:
# probePoint = probeDB["3496"][0]
# mapMatch(probePoint)
# print(distanceFromPointToSegment([51,9],[51.5,9.2],[51.5,9.1]))
# print(kilometerDistanceFromPointToPoint("",""))
