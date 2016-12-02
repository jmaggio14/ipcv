import numpy as np
import ipcv

def filter_bandpass(img, radialCenter, bandwidth, order=1, filterShape=ipcv.IPCV_IDEAL):
	"""
	:purpose:
		generates a bandpass filter
	:inputs:
		img [np.ndarray]
			'--> img to generate filter for
		radialCenter [np.ndarray]
			'--> size of bandpass
		bandwidth [np.ndarray]
			'--> size of bandpass
		order [int]
			'--> order for butterworth filter
		filterShape [int]
			'--> type of filter to apply
	:return:
		frequency filter [np.ndarray]

	"""

	bandReject = ipcv.filter_bandreject(img,radialCenter,bandwidth,order,filterShape)
	bandPass = 1 - bandReject
	return bandPass

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

	# frequencyFilter = ipcv.filter_bandpass(im,
	#                                    32,
	#                                    15,
	#                                    filterShape=ipcv.IPCV_IDEAL)
	frequencyFilter = ipcv.filter_bandpass(im,
	                                   100,
	                                   15,
	                                   1,
	                                   filterShape=ipcv.IPCV_BUTTERWORTH)
	# frequencyFilter = ipcv.filter_bandpass(im,
	#                                    32,
	#                                    15,
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