import ipcv
import numpy as np
import cv2
import logging

def fast(src, differenceThreshold=50, contiguousThreshold=12, nonMaximalSuppression=True,debug=True):
	img = src.copy()
	circumference = 16
	rollArray = [ [-3,0],[-3,-1],[-2,-2],[-1,-3],
				  [0,-3],[1,-3],[2,-2],[3,-1],
				  [3,0],[3,1],[2,2],[1,3],
				  [0,3],[-1,3],[-2,2],[-3,1] ]
	dims = ipcv.dimensions(img,'dict')
	
	allCorners = np.zeros(img.shape)
	maximaSum = allCorners
	points = np.zeros( (dims["rows"], dims["cols"], circumference) )
	unchanged = np.zeros( (dims["rows"], dims["cols"], circumference))

	for index,rc in enumerate(rollArray):
		points[:,:,index] = np.roll( np.roll(img,rc[0],axis=0), rc[1],axis=1)
		unchanged[:,:,index] = img

	greaterThan = (unchanged - points) > differenceThreshold
	lessThan = ( (points - unchanged) > differenceThreshold )

	for band in range(circumference):
		posOverlap = greaterThan[:,:,0:contiguousThreshold] == 1
		negOverlap = lessThan[:,:,0:contiguousThreshold] == 1
		posCornerCheck = np.sum(posOverlap,axis=2)	
		negCornerCheck = np.sum(negOverlap,axis=2)

		allCorners[np.where(posCornerCheck >= contiguousThreshold)] = 1
		allCorners[np.where(negCornerCheck >= contiguousThreshold)] = 1


		maximaSum = maximaSum + allCorners
		greaterThan = np.roll(greaterThan,1,axis=2)
		lessThan = np.roll(lessThan,1,axis=2)

	# if nonMaximalSuppression:
	# 	firstDerivative = np.gradient(maximaSum)
	# 	secondDerivative = np.gradient(maximaSum)


	finalCorners = np.clip(allCorners,0,1).astype(ipcv.IPCV_8U)
	return finalCorners






if __name__ == '__main__':

	import os.path
	import time
	import cv2
	import numpy

	home = os.path.expanduser('~')
	filename = home + os.path.sep + 'src/python/examples/data/checkerboard.tif'
	# filename = home + os.path.sep + 'src/python/examples/data/sparse_checkerboard.tif'
	# filename = home + os.path.sep + 'src/python/examples/data/lenna.tif'


	src = cv2.imread(filename, cv2.IMREAD_UNCHANGED)

	startTime = time.time()
	dst = ipcv.fast(src, differenceThreshold=50,
			              contiguousThreshold=8,
			              nonMaximalSuppression=True)
	print('Elapsed time = {0} [s]'.format(time.time() - startTime))

	cv2.imshow('raw corners',dst*255)
	cv2.namedWindow(filename, cv2.WINDOW_AUTOSIZE)
	cv2.imshow(filename, src)

	if len(src.shape) == 2:
		annotatedImage = cv2.merge((src, src, src))
		annotatedImage[dst == 1] = [0,0,255]
	else:
		annotatedImage = src
		annotatedImage[dst == 1] = [0,0,255]

	cv2.namedWindow(filename + ' (FAST Corners)', cv2.WINDOW_AUTOSIZE)
	cv2.imshow(filename + ' (FAST Corners)', annotatedImage)

	print('Corner coordinates ...')
	indices = numpy.where(dst == 1)
	numberCorners = len(indices[0])
	if numberCorners > 0:
		for corner in range(numberCorners):
			print('({0},{1})'.format(indices[0][corner], indices[1][corner]))

	action = ipcv.flush()
	# if action == "save":
		# cv2.imwrite(str(time.time(),annotatedImage):
