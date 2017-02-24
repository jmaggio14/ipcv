import numpy as np
import ipcv

def frequency_filter(img, frequencyFilter, delta=0):
	try:
		rows,cols,bands,_ = ipcv.dimensions(img,'t')
		freqFiltered = np.zeros( (rows,cols,bands) ) 
		x,y = np.indices( (rows,cols) )
		shifter = np.dstack( ( (-1)**(x+y),) * bands ) if bands > 1 else (-1)**(x+y)
		src = img.copy() * shifter

		fft = np.fft.fft2(src)
		frequencyFilter = np.dstack( (frequencyFilter,) * bands ) if bands > 1 else frequencyFilter
		freqFiltered = fft * frequencyFilter

		spatialFiltered = np.abs( np.fft.ifft2(freqFiltered) )
		spatialFiltered = shifter * spatialFiltered

		return (spatialFiltered + delta).astype(ipcv.IPCV_8U)

	except Exception as e:
		ipcv.debug(e)

if __name__ == '__main__':

	import cv2
	import ipcv
	import numpy
	import os.path
	import time

	home = os.path.expanduser('~')
	# filename = home + os.path.sep + 'src/python/examples/data/lenna.tif'
	filename = home + os.path.sep + 'src/python/examples/data/giza.jpg'

	im = cv2.imread(filename)

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
	cv2.imshow(filename, ipcv.histogram_enhancement(im))

	filterName = 'Filtered (' + filename + ')'
	cv2.namedWindow(filterName, cv2.WINDOW_AUTOSIZE)
	cv2.imshow(filterName, filteredImage)
	cv2.imshow(filterName, ipcv.histogram_enhancement(filteredImage))

	ipcv.flush()
