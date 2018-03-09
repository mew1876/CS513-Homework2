class Link:
	def __init__(self, csvRow):
		self.ID 				= int(csvRow[0])
		self.startNodeID 		= int(csvRow[1])
		self.endNodeID 			= int(csvRow[2])
		self.length				= float(csvRow[3])
		self.functionalClass 	= int(csvRow[4])
		self.directionOfTravel 	= csvRow[5]
		self.speedCategory 		= int(csvRow[6])
		self.fromRefSpeedLimit 	= int(csvRow[7])
		self.toRefSpeedLimit 	= int(csvRow[8])
		self.fromRefNumLanes 	= int(csvRow[9])
		self.toRefNumLanes 		= int(csvRow[10])
		self.multiDigitized 	= csvRow[11]
		self.urban 				= csvRow[12]	
		
		splitDataPoints = lambda coord: float(coord) if coord else None
		self.shapeInfo 			= [[splitDataPoints(coord) for coord in coords.split("/")] for coords in csvRow[14].split("|")]
			# [ [latitude,longitude,elevation],[lat,long,elevation]... ]
		self.curvatureInfo 		= [[splitDataPoints(coord) for coord in coords.split("/")] for coords in csvRow[15].split("|")]
			# [ [distanceFromStartNode, curvature in meters],[dist,curv]... ]
		self.slopeInfo 			= [[splitDataPoints(coord) for coord in coords.split("/")] for coords in csvRow[16].split("|")]
			# [ [distanceFromStartNode, slopeAtPoint in degrees],[dist,slope]... ]
			# after calculated slope: [ [dist,slope,calculatedSlope]]

	def __hash__(self):
		return self.ID
	def __eq__(self,other):
		return self.ID == other.ID