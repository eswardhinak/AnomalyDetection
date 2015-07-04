"""
	Class Cluster holds a list of points that are in that cluster and has methods
	to updates its location when the cluster includes new points
"""
import math 

class Cluster:
	dimensions = 0	#static variable (every cluster has same number of dimensions)

	"""
		updates cluster location array (called everytime a new cluster is added to this cluster)
	"""
	def updateClusterLocation(self):
		self.clusterlocation = [None] * self.dimensions	#resets cluster location
		#goes through cluster points and averages their locations to find the center
		for i in range(0, self.dimensions):
			total = 0
			print ("DIMENSIONS---%d" % self.dimensions)
			for j in self.clusterpoints:
				print ("LENTHTHTHTHT: %d" % len(j.coordinateList))
				total += j.coordinateList[i]
			self.clusterlocation[i] = total / (len(self.clusterpoints))

	"""
		constructor for cluster
	"""
	def __init__(self, clusterpoint, dimensions):
		#instantiates member variables
		self.clusterlocation = []
		self.clusterpoints = []
		self.clusterpoints.append(clusterpoint)	#adds initial point to cluster
		self.dimensions = dimensions
		self.radius = 0
		self.updateClusterLocation()	#updates location 


	"""
		method to combine this cluster instance with the specified cluster in the parameter
	"""
	def combineWithCluster(self, cluster):
		for j in cluster.clusterpoints:
			self.clusterpoints.append(j)
		self.updateClusterLocation()

	"""
		method to calculate the Euclidean distance from a cluster's center to a specified point in the cluster
	"""
	def calculateRadius(self, clusterpoint):
		tote = 0
		for i in range(0, len(clusterpoint.coordinateList)):
			diff = self.clusterlocation[i] - clusterpoint.coordinateList[i]
			diff = diff * diff
			tote += diff
		return math.sqrt(tote)

	"""
		method to define the spherical radius of a cluster (the maximum bounds)
	"""
	def defineBounds(self):
		#find point furthest away from center and define that as bounds.
		max_radius = 0
		first_point = True
		for i in self.clusterpoints:
			current_radius = self.calculateRadius(i)
			if (first_point == True):
				max_radius = current_radius
			elif(max_radius < current_radius):
				max_radius = current_radius

		self.radius = max_radius


