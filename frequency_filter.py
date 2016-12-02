import numpy as np
import ipcv

def frequency_filter(img, frequencyFilter, delta=0):
	"""
	:purpose:
		applies a frequency filter to an image
	:inputs:
		img [np.ndarray]
			'--> image to be filtered
		frequencyFilter [np.ndarray]
			'--> filter to apply to image
		delta [int]
			'--> offset to be added to image at the end
	:return:
		filtered image
	"""
	try:
		#generating deep copy
		img = img.copy()
		rows,cols,bands,_ = ipcv.dimensions(img,'t')
		#preparing freq and filter arrays
		freqFiltered = np.zeros( (rows,cols,bands) ).astype(ipcv.IPCV_128C)
		spatialFiltered = np.zeros( (rows,cols,bands) ).astype(ipcv.IPCV_128C)
		x,y = np.indices( (rows,cols) )
		shifter = (-1)**(x+y)
		
		#making image 3D if necessary for computational ese
		if len(img.shape) == 2:
			img = img.reshape( (rows,cols,1) )

		for band in range(bands):
			#shifting image band by band
			spatial = (img[:,:,band] * shifter).copy()
			fft = np.fft.fft2(spatial)
			#applying frequency filter
			freqFiltered[:,:,band] = fft * frequencyFilter
			spatialFiltered[:,:,band] = np.abs( np.fft.ifft2(freqFiltered[:,:,band]) ) * shifter

		return (spatialFiltered + delta)

	except Exception as e:
		ipcv.debug(e)

if __name__ == '__main__':

	import cv2
	import ipcv
	import numpy
	import os.path
	import time

	home = os.path.expanduser('~')
	filename = home + os.path.sep + 'src/python/examples/data/lenna.tif'
	filename = home + os.path.sep + 'src/python/examples/data/giza.jpg'

	im = cv2.imread(filename,cv2.IMREAD_UNCHANGED)

	frequencyFilter = ipcv.filter_lowpass(im, 
	                                      16, 
	                                      filterShape=ipcv.IPCV_GAUSSIAN)

	startTime = time.clock()
	offset = 0
	filteredImage = ipcv.frequency_filter(im, frequencyFilter, delta=offset)
	filteredImage = numpy.abs(filteredImage)
	filteredImage = filteredImage.astype(dtype=numpy.uint8)
	elapsedTime = time.clock() - startTime
	print('Elapsed time (frequency_filter)= {0} [s]'.format(elapsedTime))

	cv2.namedWindow(filename, cv2.WINDOW_AUTOSIZE)
	cv2.imshow(filename, im)
	# cv2.imshow(filename, ipcv.histogram_enhancement(im))

	filterName = 'Filtered (' + filename + ')'
	cv2.namedWindow(filterName, cv2.WINDOW_AUTOSIZE)
	cv2.imshow(filterName, filteredImage)
	# cv2.imshow(filterName, ipcv.histogram_enhancement(filteredImage))

	ipcv.flush()
