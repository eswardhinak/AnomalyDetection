'''
	Script to generate a list of data points
'''

import os
import sys
from random import randint

outFile = input("Enter name of output file: ")
dimensions = input("Enter number of dimensions: ")
num_points = input("Enter number of points: ")
lower_bound = input("Input lower bound of points: ")
upper_bound = input("Input upper bound of points: ")
if (lower_bound >= upper_bound):
	print("Incorrect lower and upper bound.")
	sys.exit()


f = open(outFile, 'w')
dimensions = int(dimensions)
num_points = int(num_points)
lower_bound = int(lower_bound)
upper_bound = int(upper_bound)
for i in  range(0, num_points):
	for j in range(0, dimensions):
		random_number = randint(lower_bound, upper_bound)
		f.write('%d ' % random_number)

	f.write("\n")