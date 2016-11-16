#PYTHON3
import cv2
import numpy as np
from sys import exc_info


def quantize(img, levels, qtype="uniform", maxCount=255, displayLevels=None):
	"""
	:NAME:
		quantize

	:PURPOSE:
		this method generates a quantized image, that is an image in which the number
		of possible pixel values has been decreased. This can be done using two different
		quanitization techniques -- "uniform" and "igs".

		"uniform" quantizes an image by flooring all the values to a defined level.
		"igs" floors the values and then adds some calculated error to the image to reduce apparent contouring
			in addition, this will return an image with the same standard error, 

	:CATEGORY:
		ipcv -- histogram analysis tool

	:CALLING SEQUENCE:
		quantizedImage = quantize(img = inputImage,\
								 levels = numberLevels,\
								 qType = 'quanitizationType',\
								 maxCount = 255,\
								 displayLevels = 256)

	:INPUTS:
		img
			[numpy.ndarray]	input image to be quanitized
		levels
			[int] number of possible unique color levels per channel in output image
		qtype
			[string] type of quanitizatio nprodcedure to be used
		maxCount
			[int] maximum pixel value in the output array
		displayLevels
			[int] number of theoretical possible values in input image
				  (NOT THE NUMBER OF ACTUAL UNIQUE PIXEL VALUES)

	:RETURN VALUE:
		result is a quanitized np array of the same shape as the input image

	:SIDE EFFECTS:
		can produce very visible contouring!

	:ERROR CHECKING:
		RETURN, -1
			if incorrect data types are used

	:REQUIRES:
		np
		cv2

	:MODIFICATION HISTORY:
		Engineer:	Jeff Maggio
		08/25/16:	uniform code
		08/28/16:	igs addition

	"""
	try:

		#ERROR CHECKING
		if isinstance(img, np.ndarray) == False:
			print( "input 'img' must be a valid numpy.ndarray" )
			raise ValueError
		if isinstance(displayLevels,int) == False: #checking to see if displayLevels is an integer
			print( "input 'displayLevels' must be an integer" )
			raise ValueError
		if isinstance(levels,int) == False: #checking to see if levels is an integer
			print( "input 'levels' must be an integer" )
			raise ValueError
		if isinstance(maxCount,int) == False:
			print("input 'maxCount' must be an integer")
			raise ValueError
		if qtype != "uniform" and qtype != "igs":
			print("input 'qtype' must be one of the following strings: 'uniform' or 'igs'")
			raise ValueError
		if displayLevels > ( maxCount + 1 ):
			print( "input displayLevels cannot be greater than one more than input 'maxCount' ({0})".format( ( maxCount + 1 ) ) )
			raise ValueError
		elif displayLevels < 0:
			print( "input 'displayLevels' cannot be negative, currently is ({0})".format( displayLevels ))
			raise ValueError
		if levels > ( displayLevels ):
			print( "input 'levels' must be smaller than input 'displayLevels' ({0})".format( ( displayLevels ) ) )
			raise ValueError
		if maxCount < 0:
			print( "input 'maxCount' cannot be negative, currently is ({0})".format( maxCount ) )
			raise ValueError



		#BEGIN QUANTIZATION PROCEDURE
		divisor = int(displayLevels) / levels

		if qtype == "uniform":
			img = (img // divisor)
		
		elif qtype == "igs":
			error = 0
			for pixel in range(img.size): #for each column in the row
				pixelValue = img.flat[pixel]
				bigPix = pixelValue + error

				if (bigPix) < maxCount:
					img.flat[pixel] = ( bigPix // divisor ) 

				else:
					img.flat[pixel] = ( pixelValue // divisor )

				error = (bigPix) % divisor
		img = int(divisor) * img.astype(np.uint8) #converting to a unsigned 8 for display purposes

	except Exception as exception:
		print("----------------------------------------------")
		print("unable to compute because: {0} on line {1}".format(exception,exc_info()[-1].tb_lineno))
		print("----------------------------------------------")

	return img



if __name__ == '__main__':

  	import cv2
  	import ipcv
  	import os.path

  	home = os.path.expanduser('~')
  	# filename = home + os.path.sep + 'src/python/examples/data/crowd.jpg'
  	# filename = home + os.path.sep + 'src/python/examples/data/redhat.ppm'
  	filename = home + os.path.sep + 'src/python/examples/data/linear.tif'
  	# filename = home + os.path.sep + 'src/python/examples/data/lenna.tif'

  	im = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
  	print('Filename = {0}'.format(filename))
  	print('Data type = {0}'.format(type(im)))
  	print('Image shape = {0}'.format(im.shape))
  	print('Image size = {0}'.format(im.size))

  	cv2.namedWindow(filename, cv2.WINDOW_AUTOSIZE)
  	cv2.imshow(filename, im)

  	#UNIFORM TESING
  	numberLevels = 7
  	quantizedImage = ipcv.quantize(im,numberLevels,qtype="uniform",displayLevels=256)
  	cv2.namedWindow(filename + ' (Uniform Quantization)', cv2.WINDOW_AUTOSIZE)
  	cv2.imshow(filename + ' (Uniform Quantization)', quantizedImage)
  	print("uniform image size = " + str(quantizedImage.size))

  	#IGS TESTING
  	numberLevels = 7
  	quantizedImage = ipcv.quantize(im,numberLevels, qtype="igs", displayLevels=256)
  	cv2.namedWindow(filename + ' (IGS Quantization)', cv2.WINDOW_AUTOSIZE)
  	cv2.imshow(filename + ' (IGS Quantization)', quantizedImage)
  	print("igs image size = " + str(quantizedImage.size))

  	action = ipcv.flush()
