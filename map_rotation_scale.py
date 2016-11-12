import numpy as np
import cv2
import ipcv
from constants import *
import time

# PYTHON METHOD DEFINITION
def map_rotation_scale(src, rotation=0, scale=[1, 1]):
	try:
		theta = np.radians(rotation)
		srcDims = ipcv.dimensions(src, returnType="dictionary")

		K = srcDims['cols']
		L = srcDims['rows']

		W = scale[0]
		H = scale[1]
		M = K * W
		N = L * H


		x = K
		y = H

		dimVector = np.asmatrix( [x,
								  y,
								  1] )

		# SCALING
		scaleMat = np.asarray( [ [W,0,0],
								 [0,H,0],
								 [0,0,1] ] ) 
		dimVector = dimVector * scaleMat



		scaledDims = np.asmatrix( [ np.arange(dimVector[0,0]),
									np.arange(dimVector[0,1]),
								  			  1				] )


		dimVector[0,0] = dimVector[0,0] - M/2
		dimVector[0,1] = N/2 - dimVector[0,1]

		# ROTATION
		sinTheta = np.sin(theta)
		cosTheta = np.cos(theta)
		rotationMat = np.asmatrix( [ [cosTheta,  -sinTheta,  0.0],
									 [sinTheta, cosTheta,  0.0],
									 [     0.,       0.,    1.0] ] )
		dimVector = dimVector * rotationMat


		#Realigning Image about corner
		dimVector[0,0] = dimVector[0,0] + K/2
		dimVector[0,1] = L/2 - dimVector[0,1]

		return dimVector[0,0].astype(IPCV_32F),dimVector[0,1].astype(IPCV_32F)

	except Exception as e:
		ipcv.debug(e)



# PYTHON TEST HARNESS
if __name__ == '__main__':

	import cv2
	import ipcv
	import os.path
	import time

	home = os.path.expanduser('~')
	filename = home + os.path.sep + 'src/python/examples/data/crowd.jpg'
	filename = home + os.path.sep + 'src/python/examples/data/lenna.tif'
	src = cv2.imread(filename)

	startTime = time.clock()
	map1, map2 = ipcv.map_rotation_scale(src, rotation=30, scale=[1.0, 0.8])
	elapsedTime = time.clock() - startTime
	print('Elapsed time (map creation) = {0} [s]'.format(elapsedTime))

	startTime = time.clock()
	dst = cv2.remap(src, map1, map2, cv2.INTER_NEAREST)
	# print(dst)
	#   dst = ipcv.remap(src, map1, map2, ipcv.INTER_NEAREST)
	elapsedTime = time.clock() - startTime
	# print('Elapsed time (remapping) = {0} [s]'.format(elapsedTime)) 

	srcName = 'Source (' + filename + ')'
	cv2.namedWindow(srcName, cv2.WINDOW_AUTOSIZE)
	cv2.imshow(srcName, src)

	dstName = 'Destination (' + filename + ')'
	cv2.namedWindow(dstName, cv2.WINDOW_AUTOSIZE)
	cv2.imshow(dstName, dst)

	ipcv.flush()


# # PYTHON METHOD DEFINITION
# def map_gcp(src, map, srcX, srcY, mapX, mapY, order=1):

# # PYTHON TEST HARNESS
# if __name__ == '__main__':

# 	import cv2
# 	import ipcv
# 	import os.path
# 	import time

# 	home = os.path.expanduser('~')
# 	imgFilename = home + os.path.sep + \
# 	           'src/python/examples/data/registration/image.tif'
# 	mapFilename = home + os.path.sep + \
# 	           'src/python/examples/data/registration/map.tif'
# 	gcpFilename = home + os.path.sep + \
# 	           'src/python/examples/data/registration/gcp.dat'
# 	src = cv2.imread(srcFilename)
# 	map = cv2.imread(mapFilename)

# 	srcX = []
# 	srcY = []
# 	mapX = []
# 	mapY = []
# 	linesRead = 0
# 	f = open(gcpFilename, 'r')
# 	for line in f:
# 	linesRead += 1
# 	if linesRead > 2:
# 	   data = line.rstrip().split()
# 	   srcX.append(float(data[0]))
# 	   srcY.append(float(data[1]))
# 	   mapX.append(float(data[2]))
# 	   mapY.append(float(data[3]))
# 	f.close()

# 	startTime = time.clock()
# 	map1, map2 = ipcv.map_gcp(src, map, srcX, srcY, mapX, mapY, order=2)
# 	elapsedTime = time.clock() - startTime
# 	print('Elapsed time (map creation) = {0} [s]'.format(elapsedTime)) 

# 	startTime = time.clock()
# 	dst = cv2.remap(src, map1, map2, cv2.INTER_NEAREST)
# 	#   dst = ipcv.remap(src, map1, map2, ipcv.INTER_NEAREST)
# 	elapsedTime = time.clock() - startTime
# 	print('Elapsed time (remap) = {0} [s]'.format(elapsedTime)) 

# 	srcName = 'Source (' + srcFilename + ')'
# 	cv2.namedWindow(srcName, cv2.WINDOW_AUTOSIZE)
# 	cv2.imshow(srcName, src)

# 	mapName = 'Map (' + mapFilename + ')'
# 	cv2.namedWindow(mapName, cv2.WINDOW_AUTOSIZE)
# 	cv2.imshow(mapName, map)

# 	dstName = 'Warped (' + mapFilename + ')'
# 	cv2.namedWindow(dstName, cv2.WINDOW_AUTOSIZE)
# 	cv2.imshow(dstName, dst)

# 	ipcv.flush()
