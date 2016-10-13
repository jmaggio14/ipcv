import numpy as np
from constants import *
import ipcv


def map_quad_to_quad(img, map, imgX, imgY, mapX, mapY):
	u1=mapX[0]; u2=mapX[1]; u3=mapX[2]; u4=mapX[3]
	v1=mapY[0]; v2=mapY[1]; v3=mapY[2]; v4=mapY[3]
	x1=imgX[0]; x2=imgX[1]; x3=imgX[2]; x4=imgX[3]
	y1=imgY[0]; y2=imgY[1]; y3=imgY[3]; y4=imgY[3]

	try:
		bigMat = np.linalg.inv(np.asmatrix([[  u1,    u2,    u3,    u4,     0,     0,     0,     0  ],
							  				[  v1,    v2,    v3,    v4,     0,     0,     0,     0  ],
										    [   1,     1,     1,     1,     0,     0,     0,     0  ],
										    [  	0,     0,     0,     0,    u1,    u2,    u3,    u4  ],
										    [  	0,     0,     0,     0,    v1,    v2,    v3,    v4  ],
										    [   0,     0,     0,     0,     1,     1,     1,     1  ],
											[-x1*u1,-u2*x2,-u3*x3,-u4*x4,-u1*y1,-u2*y2,-u3*y3,-u4*y4],
											[-x1*v1,-v2*x2,-v3*x3,-v4*x4,-v1*y1,-v2*y2,-v3*y3,-v4*y4] ]))
		cordinatesVector = np.asmatrix((np.hstack((mapX,mapY))))
		shifted = cordinatesVector * bigMat
		shifted = np.hstack((shifted,np.ones((1,1))))
		# shifted = np.transpose(np.hstack((shifted,[1])))
		shifted = np.reshape(shifted,(3,3))
		maps = shifted * np.transpose(np.asmatrix([ mapX, mapY, 1] ))
		maps = maps / maps[2]
		return maps[0],maps[1]

	except Exception as e:
		ipcv.debug(e)



if __name__ == '__main__':

	import cv2
	import ipcv
	import os.path
	import time


	home = os.path.expanduser('~')
	imgFilename = home + os.path.sep + 'src/python/examples/data/lenna.tif'
	mapFilename = home + os.path.sep + 'src/python/examples/data/gecko.jpg'
	img = cv2.imread(imgFilename)
	map = cv2.imread(mapFilename)

	mapName = 'Select corners for the target area (CW)'
	cv2.namedWindow(mapName, cv2.WINDOW_AUTOSIZE)
	cv2.imshow(mapName, map)

	print('')
	print('--------------------------------------------------------------')
	print('  Select the corners for the target area of the source image')
	print('  in clockwise order beginning in the upper left hand corner')
	print('--------------------------------------------------------------')
	p = ipcv.PointsSelected(mapName, verbose=True)
	while p.number() < 4:
		cv2.waitKey(100)
	cv2.destroyWindow(mapName)

	imgX = [0, img.shape[1]-1, img.shape[1]-1, 0]
	imgY = [0, 0, img.shape[0]-1, img.shape[0]-1]
	mapX = p.x()
	mapY = p.y()

	print('')
	print('Image coordinates ...')
	print('   x -> {0}'.format(imgX))
	print('   y -> {0}'.format(imgY))
	print('Target (map) coordinates ...')
	print('   u -> {0}'.format(mapX))
	print('   v -> {0}'.format(mapY))
	print('')

	startTime = time.clock()
	map1, map2 = ipcv.map_quad_to_quad(img, map, imgX, imgY, mapX, mapY)
	elapsedTime = time.clock() - startTime
	print('Elapsed time (map creation) = {0} [s]'.format(elapsedTime)) 

	startTime = time.clock()
	dst = cv2.remap(img, map1, map2, cv2.INTER_NEAREST)
	elapsedTime = time.clock() - startTime
	print('Elapsed time (remap) = {0} [s]'.format(elapsedTime)) 
	print('')

	compositedImage = map
	mask = numpy.where(dst != 0)
	if len(mask) > 0:
		compositedImage[mask] = dst[mask]

	compositedName = 'Composited Image'
	cv2.namedWindow(compositedName, cv2.WINDOW_AUTOSIZE)
	cv2.imshow(compositedName, compositedImage)

	ipcv.flush()

