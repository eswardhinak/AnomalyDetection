'''
	This main module runs the cluster formation and cluster combination algorithm.
	It also handles the input that defines the data file and number of clusters to be created
'''

import os
import sys
import ClusterPoint
import Cluster
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors
from mpl_toolkits.mplot3d import Axes3D
from random import randint

'''
	This method takes a line of the data file and creates a point out of it using the point constructor
'''
def createPoint(line):
	print ("create point %s" % line)
	list_of_points = line.split(' ') #splits the coordinate points based on spaces 
	list_of_points.pop() #takes out the first empty space created by the above line
	current_point = ClusterPoint.ClusterPoint(list_of_points)
	return current_point

'''
	***DEPRECATED FUNCTION***
	This does the original naive clustering. It first creates a solo cluster for every point. Then it invokes the combine
	clusters method to combine nearest clusters. This entire approach had a pretty bad runtime
	If the number of points was V and the number of clusters to form was C. The runtime was (V-C)*(V*V) --> O(V^3)
	That runtime is comptued for the entire clusterin approach, not just the below function. This includes the call to combineClusters()
'''
def clusterify(list_points, clusterNumber, dimensions):
	count = 0
	clusterList = []

	#goes through list of points and create a cluster for each one
	for i in range(0, len(list_points)):
		new_cluster = Cluster.Cluster(list_points[i], dimensions)
		clusterList.append(new_cluster) #adds the cluster to the list of clusters 

	#combine nearest cluster until the number of clusters is equal to the user defined amount.
	while (len(clusterList) > int(clusterNumber)):
		print (count)
		combineClusters(clusterList)	
		count+=1


	return clusterList


'''
	Method to combine the nearest clusters
'''
def combineClusters(clusterList):
	first_point = True
	min_distance = 0
	cluster1_index = 0
	cluster2_index = 1

	#find the closest clusters
	for i in range(0, len(clusterList)-1):
		for j in range(i+1, len(clusterList)):
			distance = calculateDistance(clusterList[i], clusterList[j])
			#for the first pair, set its distance as minimum
			if (first_point == True):
				min_distance = distance
				first_point = False
			#compare with the minimum nearest clusters
			elif(distance < min_distance):
				min_distance = distance
				cluster1_index = i
				cluster2_index = j

	#report the nearest clusters
	print("Cluster1: %d  Cluster2: %d  Distance: %f" % (cluster1_index, cluster2_index, min_distance))

	#combine the nearest clusters and remove one of them
	clusterList[cluster1_index].combineWithCluster(clusterList[cluster2_index])
	clusterList.pop(cluster2_index)


'''
	Method to calculate the Euclidean distance between two clusters
'''
def calculateDistance(cluster1, cluster2):
	dimensions = len(cluster1.clusterlocation)
	tote = 0

	#distance formula for n dimensions
	for i in range(0, dimensions):
		temp = cluster1.clusterlocation[i] - cluster2.clusterlocation[i]
		temp = temp * temp
		tote += temp
	dist = math.sqrt(tote)
	return dist

'''
	Method to calculate the Euclidean distance between a point and a cluster
'''
def calcDistance(point, cluster):
	dimensions = len(cluster.clusterlocation)
	tote = 0
	for i in range(0, dimensions):
		temp = cluster.clusterlocation[i] - point.coordinateList[i]
		temp = temp * temp
		tote += temp
	dist = math.sqrt(tote)
	return dist

'''
	Method to find the closest cluster to a given point. (This is used by k-means clustering approach)
'''
def findClosestCluster(point, clusterList):
	closestDistance = calcDistance(point, clusterList[0])
	closestClusterIndex = 0
	for c in range(0, len(clusterList)):
		currDistance = calcDistance(point, clusterList[c])
		if (currDistance < closestDistance):
			closestDistnace = currDistance
			closestClusterIndex = c
	return closestClusterIndex

'''
	This is the better approach to clustering. It randomly picks a first cluster. Then it chooses the rest of the clusters, by choosing points
	that are the furthest away from each of the rest of the already chosen clusters. 
'''
def kMeansClustering(pointList, clusterNumber, dimensions):
	clusterList = [] #list of clusters
	indexSet = set()
	count = 0
	#find the information about the first cluster
	length=len(pointList)
	firstpoint=randint(0,length-1)	#get a random first cluster
	clusterList.append(Cluster.Cluster(pointList[firstpoint], dimensions))	#add random first cluster to list of clusters
	indexSet.add(firstpoint)	#add its index to our hashset of indices (points that we won't be adding to clusters anymore)
	count+=1

	#build the correct number of clusters
	while (count < clusterNumber):
		bestDistance = 0
		bestIndex = 0
		#go through the point list
		for j in range(0, len(pointList)):
			#j is not already a cluster
			if (j not in indexSet):
				averageDistance = 0	#average distance to all the already created clusters (want to find the longest distance)
				total = 0

				#calculate distance to each of the already existing clusters
				for f in clusterList:
					averageDistance += calcDistance(pointList[j], f)
					total += 1
				averageDistance /= total	#find average distance

				#if this is bigger than our current biggest one
				if (averageDistance > bestDistance):
					bestDistance = averageDistance
					bestIndex = j
		clusterList.append(Cluster.Cluster(pointList[bestIndex], dimensions))	#create a cluster for the best point and add it to cluster list
		indexSet.add(bestIndex)
		count+=1

	#add the remaining points to their nearest cluster
	for k in pointList:
		if (k not in indexSet):
			closestIndex = findClosestCluster(k, clusterList)	#find the nearest cluster for each point
			clusterList[closestIndex].addPoint(k)				#add the point ot its nearest cluster

	return clusterList

def main():
	print ("Beginning Program...")
	data_file = input("Enter name of training data file: ")
	clusterNumber = input("Enter number of clusters: ")
	f = open(data_file, 'r')
	first = False
	dimensions = 0
	list_points = []

	#read in all the points in the file
	for line in f:
		#print (line)
		if (first != True):
			dimensions = len(line.split())
			first = True
		elif(first != False):
			if (len(line.split()) != dimensions):
				print("invalid format of data file")
				return
		#create a point based on location
		current_point = createPoint(line)
		list_points.append(current_point)
	#create clusters
	clusterList1 = kMeansClustering(list_points, int(clusterNumber), dimensions)

	#find radius of each cluster
	for q in clusterList1:
		q.defineBounds()

	#report final clusters
	print ("Final clusters: \n")
	for i in clusterList1:
		print("Radius: %f\n" % i.radius)
		print("Number of points: %d\n" % len(i.clusterpoints))

	#print final cluster location and encompassing points to cluster file
	f = open("clusters", "w")
	for k in clusterList1:
		f.write("%f " % k.radius)
		for m in k.clusterlocation:
			f.write("%f " % m)
		f.write("\n")
		for p in range(1, len(k.clusterpoints)):
			f.write("$ ")
			for g in k.clusterpoints[p].coordinateList:
				f.write("%f " % g)
			f.write("\n")
	print("Finished creating clusters. Cluster information in clusters file.")

	#plot the results (only for 2d)
	f = open("clusters", "r")
	newcluster=False
	count = -1
	tuple2 = (float(randint(0,100)/100), float(randint(0,100)/100), float(randint(0,100)/100))
	#go through clusters and their points to plot them
	for line in f:
		line_array = line.split(' ')
		if (line_array[0] != "$"):
			#change color for new cluster
			tuple2 = (float(randint(0,100)/100), float(randint(0,100)/100), float(randint(0,100)/100))
			newcluster=True
			radius=line_array[0]
			xcoord=line_array[1]
			ycoord=line_array[2]
			plt.scatter(xcoord, ycoord,c='r') #plot the center of the cluster in red
		else:
			if (newcluster == True):
				count += 1
			newcluster = False
			xcoord = line_array[1]
			ycoord = line_array[2]
			plt.scatter(xcoord, ycoord,c=tuple2) #plot the cluster point
	plt.show()

	#plot the results (only for 3 dimensional analysis)
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	newcluster = False
	count = -1
	f = open("clusters", "r")
	for line in f:
		line_array=line.split(' ')
		if (line_array[0] != "$"):
			tuple2 = (float(randint(0,100)/100), float(randint(0,100)/100), float(randint(0,100)/100))
			newcluster=True
			radius=float(line_array[0])
			xcoord=float(line_array[1])
			ycoord=float(line_array[2])
			zcoord=float(line_array[3])
			ax.scatter(xcoord, ycoord, zcoord, c='r')
		else:
			if (newcluster==True):
				count += 1
			newcluster= False
			xcoord = float(line_array[1])
			ycoord= float(line_array[2])
			zcoord=float(line_array[3])
			ax.scatter(xcoord, ycoord, zcoord,c=tuple2)
	plt.show()





if __name__ == "__main__": main()	#program start
