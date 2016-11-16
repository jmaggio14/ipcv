import ipcv
from sys import exc_info
from os.path import split
import numpy as np

def histogram_enhancement(img, etype='linear2', target=None, maxCount=255, pool = False):
	"""
	:NAME:
		histogram_enchancement

	:PURPOSE:
		This method modifies an image using basic histogram enhancement techniques:
			linear -- removes removes extranesous pixels on outer edge of histogram and stretches
				histogram to fill entire DC range
			equalization -- a technique to even out peaks on the histogram and product a near-flat
				histogram curve
			match -- modifies an image such that it's pixel distribution mimics that of a target 
				image or distribution



	:CATEGORY:
		ipcv -- histogram enchancement tool

	:CALLING SEQUENCE:
		quantizedImage = histogram_enchancement(img,\
											etype=etype,\
											target=targer,\
											maxCount = maxCount,\
											pool = pool)


	:INPUTS:
		img
			[numpy.ndarray]	input image
		etype
			[string] type of histogram enhancement to perform
		target
			[numpy.ndarray] target image or distribution using in histogram matching
		maxCount
			[int] the largest possible DC value in the image
		pool
			[boolean] whether or not to pool all colors into one cdf or loop by band 
					

	:RETURN VALUE:
		a numpy array containing the enhanced image

	:SIDE EFFECTS:
		removes possibly pertinent data in an image

	:ERROR CHECKING:
		ValueError
		TypeError

	:REQUIRES:
		numpy
		sys.exc_info
		os.path.split

	:MODIFICATION HISTORY:
		Engineer:	Jeff Maggio
		original:	09/09/16

	"""


	#ERROR CHECKING
	if etype == "match":
		if (isinstance(target,np.ndarray) == False):
			print("-------------------------------------------------------------------")
			print("input 'target' must by a valid numpy.ndarray, currently {0}".format(type(target)))
			print("-------------------------------------------------------------------")
			print("raising TypeError...")
			raise TypeError

	if isinstance(maxCount,int) == False:
		print("-------------------------------------------------------------------")
		print("input 'maxCount' must be an int type, currently is {0}".format(type(target)))
		print("-------------------------------------------------------------------")
	elif maxCount < 0:
		print("-------------------------------------------------------------------")
		print("maxCount must be greater than 0, currently is {0}".format(maxCount))
		print("-------------------------------------------------------------------")

	if isinstance(img, np.ndarray) == True:
	    img = img.reshape(img.shape[0],img.shape[1],1) if ( len(img.shape) == 2 ) else img
	    bands = img.shape[2]
	
	if isinstance(target, np.ndarray) == True:
	    target = target.reshape(target.shape[0],target.shape[1],1) if ( len(target.shape) == 2 ) else target
	
	if etype == "match":
		if ( len(target.shape) != 1 ) and ( target.shape[2] != img.shape[2] ):
			print("-------------------------------------------------------------------")
			print("original and target images must both be of the same type (grayscale or color")
			print("raising TypeError...")
			print("-------------------------------------------------------------------")
			raise TypeError

		
	#BEGIN ACTUAL WORK
	try:
	     #2 is index of cdf from return tuple

	    if "linear" in etype:

	    	for band in range(bands):

	    		#cdf is recalculated by band
	    		cdf = ipcv.histogram(img=img,channels=band,histSize=(maxCount+1),\
		    		ranges=[0,maxCount+1],returnType=1)[2]

		    	# generating components of the line
		    	lowerBound = (float(etype.replace("linear","") ) / 200.0)
		    	upperbound = ( 1 - lowerBound )
		    	dcLow = np.where(cdf >= lowerBound)[0][0]
		    	dcHigh = np.where(cdf <= upperbound)[0][-1]
		    	m = ( maxCount / (dcHigh - dcLow) )
		    	b = maxCount - ( m * dcHigh )

		    	#generating the lookup table by applying a linear transform
		    	LUT = ( m * np.arange(maxCount+1) ) + b
		    	LUT = np.clip(LUT,0,255)
		    	print(img[:,:,band].shape)
		    	img[:,:,band] = LUT[img[:,:,band]]



	    elif etype == 'equalize':

	    	for band in range(bands):
	    		cdf = ipcv.histogram(img=img,channels=band,histSize=(maxCount+1),\
		    		ranges=[0,maxCount+1],returnType=1)[2]

		    	LUT = (cdf * maxCount).flatten()
		    	print(LUT.shape)
		    	img[:,:,band] = LUT[img[:,:,band]]



	    elif etype == "match":
	    	#Generating the target CDFs
    		tCdf = []
	    	if len(target.shape) == 1:
	    		for band in range(bands):
		    		tCdf.append( np.cumsum(target) )
	    	else:
	    		for band in range(bands):
		    		tCdf.append(ipcv.histogram(img=target,channels=band,histSize=(maxCount+1),\
			    		ranges=[0,maxCount+1],returnType=1)[2]) #only return the cdf here



	    	for band in range(bands):
	    		cdf = ipcv.histogram(img=img,channels=band,histSize=(maxCount+1),\
		    		ranges=[0,maxCount+1],returnType=1)[2]

		    	LUT = np.zeros(maxCount+1)
		    	index = 0
		    	for percentage in cdf:
		    		upperValues = np.where(tCdf[band]>=percentage)
		    		if upperValues[0].size != 0:
		    			dc = upperValues[0][0]
		    		else:
		    			dc = 0
		    		LUT[index] = dc
		    		index += 1

		    	img[:,:,band] = LUT[img[:,:,band]]



	    return img.astype(np.uint8)

	except Exception as e:
		print("===================================================================")
		exc_type, exc_obj, exc_tb = exc_info()
		fname = split(exc_tb.tb_frame.f_code.co_filename)[1]
		print("\nfile: {0}\n\nline: {1} \n\n{2}\n".format(fname,exc_tb.tb_lineno,e))
		print("===================================================================")






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
	# filename = home + os.path.sep + 'src/python/examples/data/lenna_color.tif'
	filename = home + os.path.sep + 'src/python/examples/data/giza.jpg'

	# matchFilename = home + os.path.sep + 'src/python/examples/data/giza.jpg'
	# matchFilename = home + os.path.sep + 'src/python/examples/data/lenna.tif'
	# matchFilename = home + os.path.sep + 'src/python/examples/data/lenna_color.tif'
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





	action = ipcv.flush()


