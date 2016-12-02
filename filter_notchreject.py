import numpy as np 
import ipcv


def filter_notchreject(img, notchCenter, notchRadius, order=1, filterShape=ipcv.IPCV_IDEAL):
	"""
	:purpose:
		generates a notch reject filter
	:inputs:
		img [np.ndarray]
			'--> img to generate filter for
		notchCenter [tuple]
			'--> notch offset
		notchRadius 
			'--> radius of the notch
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

		uCenter = notchCenter[0]
		vCenter = notchCenter[1]

		D1 = np.sqrt( (u-r/2-uCenter)**2 + (v-c/2-vCenter)**2 ) 
		D2 = np.sqrt( (u-r/2+uCenter)**2 + (v-c/2+vCenter)**2 ) 


		if filterShape == ipcv.IPCV_IDEAL:
			H = np.zeros( (r,c) )
			H[D1 <= notchRadius] = 1
			H[D2 <= notchRadius] = 1

		elif filterShape == ipcv.IPCV_GAUSSIAN:
			xp = -.5 * ( (D1 * D2)/(notchRadius**2) )
			H = 1 - np.exp( xp )

		elif filterShape == ipcv.IPCV_BUTTERWORTH:
			denom = 1 + ( (notchRadius**2) / (D1 * D2) )**order
			H = 1 / denom

		return H

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

	frequencyFilter = ipcv.filter_notchreject(im,
	                                   (50,50),
	                                   32,
	                                   1,
	                                   filterShape=ipcv.IPCV_IDEAL)
	frequencyFilter = ipcv.filter_notchreject(im,
	                                   (50,50),
	                                   32,
	                                   1,
	                                   filterShape=ipcv.IPCV_BUTTERWORTH)
	frequencyFilter = ipcv.filter_notchreject(im,
	                                   (50,50),
	                                   32,
	                                   1,
	                                   filterShape=ipcv.IPCV_GAUSSIAN)
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
