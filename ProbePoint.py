import time

class ProbePoint:
	def __init__(self, csvRow):
		self.timeStamp = time.strptime(csvRow[1], "%m/%d/%Y %H:%M:%S %p")
		self.latitude = float(csvRow[3])
		self.longitude = float(csvRow[4])
		self.altitude = int(csvRow[5])
		self.speed = int(csvRow[6])
		self.heading = int(csvRow[7])