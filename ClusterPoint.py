'''
	Class ClusterPoint represents a point in the input data file. 
'''

class ClusterPoint:
	def __init__(self, coordinateList):
		self.coordinateList = []
		
		#add coordinates to member list
		for i in coordinateList:
			print (i)
			(self.coordinateList).append(float(i))

	def __getitem__(self, key):
		return self

