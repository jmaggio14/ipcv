import ipcv
from sys import exc_info
import numpy as np
from cv2 import COLOR_BGR2GRAY

def histogram_enhancement(img, etype='linear2', target=None, maxCount=255, pool = True):
    # try: 
    # if isinstance(img, np.ndarray) == False:
    #     print("input 'img' must be a numpy.ndarray | currently is {0}".format(type(img)))
    # elif (img.dtype != np.uint8) and (img.dtype != np.float32):
    #     print("input 'img' must either be np.uint8 or np.float32")
    #     print("currently is {0}".format(img.dtype))
    if len(img.shape) == 3:
    	bands =


    cdf = ipcv.histogram(img=img,channels=[0],histSize=[maxCount+1],\
    		ranges=[0,maxCount+1],returnType=1)[2] #2 is index of cdf from return tuple

    if "linear" in etype:
    	# generating components of the line
    	lowerBound = .01 * (float(etype.replace("linear","") ) / 2.0)
    	upperbound = ( 1 - lowerBound )
    	dcLow = np.where(cdf <= lowerBound)[0][-1]
    	dcHigh = np.where(cdf >= upperbound)[0][0]
    	m = ( maxCount / (dcHigh - dcLow) )
    	b = maxCount - ( m * dcHigh )
    	#generating the lookup table by applying a linear transform
    	LUT = ( m * np.arange(maxCount+1) ) + b
    	LUT = np.clip(LUT,0,255)
    	img = LUT[img]


    elif etype == 'equalize':
    	for band in range(bands):
	    	LUT = cdf * maxCount
	    	img = LUT[img]


    elif etype == "match":
    	if isinstance(target,np.ndarray) == True:
    		if len(target.shape) == 1:
    			tCdf = np.cumsum(target)
    		else:
		    	tCdf = ipcv.histogram(img=target,channels=[0],histSize=[maxCount+1],\
		    		ranges=[0,maxCount+1],returnType=1)[2] #only return the cdf here

    	LUT = np.zeros(maxCount+1)
    	index = 0
    	for percentage in cdf:
    		dc = np.where(tCdf>=percentage)[0][0]
    		LUT[index] = dc
    		index += 1

    	img = LUT[img]


    return img.astype(np.uint8)







if __name__ == '__main__':

	import cv2
	import ipcv
	import os.path
	import time
	import matplotlib.pyplot as plt

	home = os.path.expanduser('~')
	# filename = home + os.path.sep + 'src/python/examples/data/redhat.ppm'
	# filename = home + os.path.sep + 'src/python/examples/data/crowd.jpg'
	# filename = home + os.path.sep + 'src/python/examples/data/lenna.tif'
	filename = home + os.path.sep + 'src/python/examples/data/giza.jpg'

	# matchFilename = home + os.path.sep + 'src/python/examples/data/giza.jpg'
	# matchFilename = home + os.path.sep + 'src/python/examples/data/lenna.tif'
	# matchFilename = home + os.path.sep + 'src/python/examples/data/redhat.ppm'
	matchFilename = home + os.path.sep + 'src/python/examples/data/crowd.jpg'

	im = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
	print('Filename = {0}'.format(filename))
	print('Data type = {0}'.format(type(im)))
	print('Image shape = {0}'.format(im.shape))
	print('Image size = {0}'.format(im.size))

	cv2.namedWindow(filename, cv2.WINDOW_AUTOSIZE)
	cv2.imshow(filename, im)

	print('Linear 2% ...')
	startTime = time.time()
	enhancedImage = ipcv.histogram_enhancement(im, etype='linear2')
	print('Elapsed time = {0} [s]'.format(time.time() - startTime))
	cv2.namedWindow(filename + ' (Linear 2%)', cv2.WINDOW_AUTOSIZE)
	cv2.imshow(filename + ' (Linear 2%)', enhancedImage)

	print('Linear 1% ...')
	startTime = time.time()
	enhancedImage = ipcv.histogram_enhancement(im, etype='linear1')
	print('Elapsed time = {0} [s]'.format(time.time() - startTime))
	cv2.namedWindow(filename + ' (Linear 1%)', cv2.WINDOW_AUTOSIZE)
	cv2.imshow(filename + ' (Linear 1%)', enhancedImage)

	print('Equalized ...')
	startTime = time.time()
	enhancedImage = ipcv.histogram_enhancement(im, etype='equalize')
	print('Elapsed time = {0} [s]'.format(time.time() - startTime))
	cv2.namedWindow(filename + ' (Equalized)', cv2.WINDOW_AUTOSIZE)
	cv2.imshow(filename + ' (Equalized)', enhancedImage)

	oldImage = enhancedImage
	oldHist = ipcv.histogram(img=oldImage,channels=[0],histSize=[256],\
    		ranges=[0,256],returnType=1)[0]

	tgtIm = cv2.imread(matchFilename, cv2.IMREAD_UNCHANGED)
	print('Matched (Image) ...')
	startTime = time.time()
	enhancedImage = ipcv.histogram_enhancement(im, etype='match', target=tgtIm)
	print('Elapsed time = {0} [s]'.format(time.time() - startTime))
	cv2.namedWindow(filename + ' (Matched - Image)', cv2.WINDOW_AUTOSIZE)
	cv2.imshow(filename + ' (Matched - Image)', enhancedImage)

	



	tgtPDF = np.ones(256) / 256
	print('Matched (Distribution) ...')
	startTime = time.time()
	enhancedImage = ipcv.histogram_enhancement(im, etype='match', target=tgtPDF)
	print('Elapsed time = {0} [s]'.format(time.time() - startTime))
	cv2.namedWindow(filename + ' (Matched - Distribution)', cv2.WINDOW_AUTOSIZE)
	cv2.imshow(filename + ' (Matched - Distribution)', enhancedImage)




	newImage = enhancedImage
	newHist = ipcv.histogram(img=newImage,channels=[0],histSize=[256],\
    		ranges=[0,256],returnType=1)[0]

	plt.plot(oldHist, color='r')
	plt.plot(newHist, color='b')
	plt.show()


	action = ipcv.flush()