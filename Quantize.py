#PYTHON 2
import cv2
from numpy import unique, amaxh


def quantize(img, levels, qtype='uniform', maxCount=255, displayLevels=None):
	"""
	:NAME:
		quantize

	:PURPOSE:
		this method generates a quantized image, that is an image in which the number
		of possible pixel values has been decreased. This can be done using two different
		quanitization techniques -- "uniform" and "igs".

		"uniform" quantizes an image by flooring all the values to a defined level.
		"igs" floors the values and then adds some noise effects to the image to reduce apparent contouring

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
		result is a quanitized numpy array of the same shape as the input image

	:SIDE EFFECTS:
		can produce the artifact known as contouring

	:ERROR CHECKING:
		RETURN, -1
			if incorrect data types are used

	:REQUIRES:
		numpy
		cv2

	:MODIFICATION HISTORY:
		engineer:	Jeff Maggio
		08/25/16:	original code

	"""

	#ERROR CHECKING
	if isinstance(img, numpy.ndarray) == False:
		print "input 'img' must be a valid numpy.ndarray"
		return -1
	if isinstance(displayLevels,int) == False: #checking to see if displayLevels is an integer
		print "input 'displayLevels' must be an integer"
		return -1
	if isinstance(levels,int) == False: #checking to see if levels is an integer
		print "input 'levels' must be an integer"
		return -1
	if displayLevels > ( maxCount + 1 ):
		print "input displayLevels cannot be greater than input 'maxCount' ({})".format( ( maxCount + 1 ) )
		return -1
	if levels > ( maxCount ):
		print "input 'levels' must be smaller than input 'maxCount' ({})".format( ( maxCount ) )
		return -1

	#BEGIN QUANTIZATION PROCEDURE
	if qtype == "uniform":
		divsor = int(displayLevels) // levels
		img = img // divsor
		# displayLevels = 256 if displayLevels == None else pass
		img = img * divsor
	elif qtype == "igs":
		pass #this is temporary as of 08/25/16


	return img

