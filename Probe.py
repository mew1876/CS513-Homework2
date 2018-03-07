from ProbePoint import ProbePoint

class Probe:
	def __init__(self, ID):
		self.ID = ID
		self.points = []

	def append(self, csvRow):
		self.points.append(ProbePoint(csvRow))
