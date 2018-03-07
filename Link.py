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
		self.shapeInfo 			= [[(lambda coord: float(coord) if coord else -1)(coord) for coord in coords.split("/")] for coords in csvRow[14].split("|")]
		self.curvatureInfo 		= [[(lambda coord: float(coord) if coord else -1)(coord) for coord in coords.split("/")] for coords in csvRow[15].split("|")]
		self.slopeInfo 			= [[(lambda coord: float(coord) if coord else -1)(coord) for coord in coords.split("/")] for coords in csvRow[16].split("|")]