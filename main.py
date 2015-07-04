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
	list_of_points = line.split(' ')
	list_of_points.pop()
	current_point = ClusterPoint.ClusterPoint(list_of_points)
	return current_point

'''
	This does the clustering. It first creates a solo cluster for every point. Then it invokes the combine
	clusters method to combine nearest clusters
'''
def clusterify(list_points, clusterNumber, dimensions):
	count = 0
	clusterList = []

	#goes through list of points and create a cluster for each one
	for i in range(0, len(list_points)):
		new_cluster = Cluster.Cluster(list_points[i], dimensions)
		clusterList.append(new_cluster)

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


def main():
	print ("Beginning Program...")
	data_file = input("Enter name of training data file: ")
	clusterNumber = input("Enter number of clusters: ")
	f = open(data_file, 'r')
	first = False
	dimensions = 0
	list_points = []
	for line in f:
		#print (line)
		if (first != True):
			dimensions = len(line.split())
			first = True
		elif(first != False):
			if (len(line.split()) != dimensions):
				print("invalid format of data file")
				return

		current_point = createPoint(line)
		list_points.append(current_point)
	clusterList = clusterify(list_points,clusterNumber, dimensions)
	for q in clusterList:
		q.defineBounds()

	#report final clusters
	print ("Final clusters: \n")
	for i in clusterList:
		print("Radius: %f\n" % i.radius)
		for j in i.clusterlocation:
			print ("%f " % j)

		print("\n") 

	#print final cluster location and encompassing points to cluster file
	f = open("clusters", "w")
	for k in clusterList:
		f.write("%f " % k.radius)
		for m in k.clusterlocation:
			f.write("%f " % m)
		f.write("\n")
		for p in k.clusterpoints:
			f.write("$ ")
			for g in p.coordinateList:
				f.write("%f " % g)
			f.write("\n")
	print("Finished creating clusters. Cluster information in clusters file.")

	#plot the results (only for 2 dimensional analysis)
	f = open("clusters", "r")
	N = 50
	colors=np.random.rand(N)
	list_colors=['g', 'b', 'k', 'm', 'y']
	newcluster=False
	count = -1
	for line in f:
		line_array = line.split(' ')
		if (line_array[0] != "$"):
			newcluster=True
			radius=line_array[0]
			##only for two dimensional
			xcoord=line_array[1]
			ycoord=line_array[2]
			plt.plot(xcoord, ycoord, 'ro')
		else:
			if (newcluster == True):
				count += 1
			newcluster = False
			xcoord = line_array[1]
			ycoord = line_array[2]
			tuple2 = (float(randint(0,100)/100), float(randint(0,100)/100), float(randint(0,100)/100))
			print(tuple2)
			#string3 = "" % tup
			plt.plot(xcoord, ycoord, color=(0.2,0.4,0.3))
	plt.show()
	'''
	#plot the results (only for 3 dimensional analysis)
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	newcluster = False
	count = -1
	for line in f:
		line_array=line.split(' ')
		if (line_array[0] != "$"):
			newcluster=True
			radius=float(line_array[0])
			xcoord=float(line_array[1])
			ycoord=float(line_array[2])
			zcoord=float(line_array[3])
			ax.scatter(xcoord, ycoord, zcoord, c='r', marker='o')
		else:
			if (newcluster==True):
				count += 1
			newcluster= False
			xcoord = float(line_array[1])
			ycoord= float(line_array[2])
			zcoord=float(line_array[3])
			ax.scatter(xcoord, ycoord, zcoord,c=list_colors[count % 5],marker='o')
	plt.show()'''





	testData = input("Enter name of testing data file: ") 
	g = open(testData, 'r') #g is file reader to training data file 

		



if __name__ == "__main__": main()	#program start