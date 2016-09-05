from sys import exc_info
from os.path import split
import cv2
import numpy as np
import matplotlib.pyplot as plt


def histogram(img,channels=[0],histSize=[256],mask=None,ranges=[0,256],returnType=0):
	"""
	:NAME:
		histogram

	:PURPOSE:
		This method returns an image histogram, pdf and cdf. working for both color and grayscale imagery


	:CATEGORY:
		ipcv -- histogram generation tool

	:CALLING SEQUENCE:
		quantizedImage = histogram(img,\
									channels=channels,\
									histSize=histSize,\
									mask=mask,\
									ranges=ranges)


	:INPUTS:
		img
			[numpy.ndarray]	input image
		channels
			[list] list of channels to compute
		histSize
			[int] maximum number of histogram bins
		mask
			[numpy.ndarray] section of image to compute
		ranges
			[list] range of values that are computed in the histogram
		returnType
			[int] modifies manner in which the histogram,pdf and cdf are returned
				if returnType == 0
					# return all arrays in one numpy.ndarray #
				elif returnType == 1
					# return all values sequentially #
					return 
					

	:RETURN VALUE:
		a numpy array containing 
	:SIDE EFFECTS:
		can produce very visible contouring!

	:ERROR CHECKING:
		ValueError
		TypeError

	:REQUIRES:
		np
		cv2
		sys.exc_info
		matplotlib.pyplot

	:MODIFICATION HISTORY:
		Engineer:	Jeff Maggio
		original:	09/06/2016

	"""



	try: 
		histogram = cv2.calcHist([img],channels=channels,mask=mask,histSize=histSize,ranges=ranges)
		pdf = histogram / img.size
		cdf = np.cumsum(pdf); cdf = np.reshape(cdf,histogram.shape)
		if returnType == 0: # return all arrays in one numpy.ndarray
			hpc = np.hstack((histogram,pdf,cdf))
			return hpc
		elif returnType == 1: # return all arrays sequentially
			return histogram,pdf,cdf

	except Exception as e:
		print("-------------------------------------------------------------------")
		exc_type, exc_obj, exc_tb = exc_info()
		fname = split(exc_tb.tb_frame.f_code.co_filename)[1]
		print("unable to compute because: {0} on line {1} in file {2}".format(e,exc_tb.tb_lineno,fname))
		print("-------------------------------------------------------------------")

		#Error checking img
		if isinstance(img, np.ndarray) == False:
			print("input 'img' must be a numpy.ndarray | currently is {0}".format(type(img)))
		elif (img.dtype != np.uint8) and (img.dtype != np.float32):
			print("input 'img' must either be np.uint8 or np.float32")
			print("currently is {0}".format(img.dtype))
		#Error checking channels
		if isinstance(channels, list) == False:
			print("input 'channels' must be a python list")
			print("currently is {0}".format(type(channels)))
		#error checking Mask
		if isinstance(mask, np.ndarray) == False and isinstance(mask, type(None)) == False:
			print("input 'mask' must be a numpy.ndarray or NoneType")
			print("currently is {0}".format(type(mask)))
		#Error checking histSize
		if isinstance(histSize, list) == False:
			print("input 'histSize' must be a python list of 1 value")
			print("currently is {0}".format(type(histSize)))
		elif len(histSize) != 1:
			print("input 'histSize' must be a python list of 1 value")
			print("currently is {0}".format(len(histSize)))


if __name__ == "__main__":
	import os.path
	import matplotlib.pyplot as plt

	home = os.path.expanduser('~')
	filename = home + os.path.sep + 'src/python/examples/data/redhat.ppm'

	img = cv2.imread(filename)
	hpc = histogram(img,channels=[0],histSize=[256],mask=None,ranges=[0,256])
	print(hpc)
	print(hpc.shape)
	legendList = ['histogram','pdf','cdf']
	for i in [1,2]:
		plt.plot(hpc[:,i], label = legendList)
	plt.show()