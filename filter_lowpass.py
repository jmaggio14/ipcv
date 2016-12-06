import numpy as np
import ipcv
import cv2
def filter_lowpass(img, cutoffFrequency, order=1, filterShape=ipcv.IPCV_IDEAL):
	"""
	:purpose:
		generates a lowpass filter
	:inputs:
		img [np.ndarray]
			'--> img to generate filter for
		cutoffFrequency [np.ndarray]
			'--> notch offset
		order
			'--> order for butterworth filter
		filterShape
			'--> type of filter to apply
	:return:
		frequency filter [np.ndarray]

	"""

	try:
		dims = ipcv.dimensions(img)
		r = dims["rows"]
		c = dims["cols"]
		u = np.arange(r)
		v = np.arange(c)
		u, v = np.meshgrid(u, v)
		lowPass = np.sqrt( (u-r/2)**2 + (v-c/2)**2 )

		if filterShape == ipcv.IPCV_IDEAL:
			lowPass[lowPass <= cutoffFrequency] = 1
			lowPass[lowPass >= cutoffFrequency] = 0

		elif filterShape == ipcv.IPCV_GAUSSIAN:
			xp = -1*(lowPass**2) / (2* cutoffFrequency**2)
			lowPass = np.exp( xp )
			lowPass = np.clip(lowPass,0,1)

		elif filterShape == ipcv.IPCV_BUTTERWORTH:
			denom = 1.0 + (lowPass / cutoffFrequency)**(2 * order)
			lowPass = 1.0 / denom
			

		return lowPass

	except Exception as e:
		ipcv.debug(e)

if __name__ == '__main__':
	import cv2
	import ipcv
	import numpy
	import matplotlib.pyplot
	import matplotlib.cm
	import mpl_toolkits.mplot3d
	import os.path

	home = os.path.expanduser('~')
	filename = home + os.path.sep + 'src/python/examples/data/lenna.tif'
	im = cv2.imread(filename)

	# frequencyFilter = ipcv.filter_lowpass(im,
	#                                    16,
	#                                    filterShape=ipcv.IPCV_IDEAL)
	frequencyFilter = ipcv.filter_lowpass(im,
	                                   16,
	                                   order=4,
	                                   filterShape=ipcv.IPCV_BUTTERWORTH)
	# frequencyFilter = ipcv.filter_lowpass(im,
	#                                    16,
	#                                    filterShape=ipcv.IPCV_GAUSSIAN)

	# Create a 3D plot and image visualization of the frequency domain filter
	rows = im.shape[0]
	columns = im.shape[1]
	u = numpy.arange(-columns/2, columns/2, 1)
	v = numpy.arange(-rows/2, rows/2, 1)
	u, v = numpy.meshgrid(u, v)

	figure = matplotlib.pyplot.figure('Frequency Domain Filter', (14, 6))
	p = figure.add_subplot(1, 2, 1, projection='3d')
	p.set_xlabel('u')
	p.set_xlim3d(-columns/2, columns/2)
	p.set_ylabel('v')
	p.set_ylim3d(-rows/2, rows/2)
	p.set_zlabel('Weight')
	p.set_zlim3d(0, 1)
	p.plot_surface(u, v, frequencyFilter)
	i = figure.add_subplot(1, 2, 2)
	i.imshow(frequencyFilter, cmap=matplotlib.cm.Greys_r)
	matplotlib.pyplot.show()
