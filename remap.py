import numpy as np

# # PYTHON METHOD DEFINITION
def remap(src, map1, map2, interpolation=ipcv.INTER_NEAREST, borderMode=ipcv.BORDER_CONSTANT, borderValue=0):
	dst = np.zeros(src.shape)
	map1 = np.round(map1)
	map2 = np.round(map2)


	


# # PYTHON TEST HARNESS
if __name__ == '__main__':

	import cv2
	import ipcv
	import os.path
	import time

	home = os.path.expanduser('~')
	filename = home + os.path.sep + 'src/python/examples/data/crowd.jpg'
	filename = home + os.path.sep + 'src/python/examples/data/lenna.tif'
	src = cv2.imread(filename)

	map1, map2 = ipcv.map_rotation_scale(src, rotation=30, scale=[1.3, 0.8])

	startTime = time.clock()
	dst = ipcv.remap(src, map1, map2, interpolation=ipcv.INTER_NEAREST, borderMode=ipcv.BORDER_CONSTANT, borderValue=0)
	elapsedTime = time.clock() - startTime
	print('Elapsed time (remap) = {0} [s]'.format(elapsedTime))

	srcName = 'Source (' + filename + ')'
	cv2.namedWindow(srcName, cv2.WINDOW_AUTOSIZE)
	cv2.imshow(srcName, src)

	dstName = 'Destination (' + filename + ')'
	cv2.namedWindow(dstName, cv2.WINDOW_AUTOSIZE)
	cv2.imshow(dstName, dst)

	ipcv.flush()


