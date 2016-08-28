#PYTHON 2
import cv2
from numpy import unique, amax


def quantize(img, levels, qtype='uniform', maxCount=255, displayLevels):
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
		result is a quanitized numpy array of the same shape as the input image

	:SIDE EFFECTS:
		can produce very visible contouring!

	:ERROR CHECKING:
		RETURN, -1
			if incorrect data types are used

	:REQUIRES:
		numpy
		cv2

	:MODIFICATION HISTORY:
		Engineer:	Jeff Maggio
		08/25/16:	uniform code
		08/28/16:	

	"""
	try:

		#ERROR CHECKING
		if isinstance(img, numpy.ndarray) == False:
			print( "input 'img' must be a valid numpy.ndarray" )
			return -1
		if isinstance(displayLevels,int) == False: #checking to see if displayLevels is an integer
			print( "input 'displayLevels' must be an integer" )
			return -1
		if isinstance(levels,int) == False: #checking to see if levels is an integer
			print( "input 'levels' must be an integer" )
			return -1
		if qtype != "uniform" or "igs":
			print("input 'qtype' must be a string")
			return -1
		if displayLevels > ( maxCount + 1 ):
			print( "input displayLevels cannot be greater than input 'maxCount' ({0})".format( ( maxCount + 1 ) ) )
			return -1
		if levels > ( displayLevels ):
			print( "input 'levels' must be smaller than input 'displayLevels' ({0})".format( ( displayLevels ) ) )
			return -1

		#BEGIN QUANTIZATION PROCEDURE
		divsor = int(displayLevels) // levels
		if qtype == "uniform":
			img = (img // divsor) * divsor

		elif qtype == "igs":
			for band in img.shape[2]: #for each color band
				for row in range(img.rows): #for each row in the band
					error = 0
					for col in range(img.cols): #for each column in the row
						quantizedPixel = ( img[row,col,band] // divsor ) * divsor
						if pixel != maxCount: #passes if the value is at it's maximum
							img[row,col,band] = quantizedPixel + error
							error = ( img[row,col,band] % levels )


	except Exception as e:
		print("unable to compute because: {0}").format(e)

	img = numpy.array(img,dtype=np.uint8) #converting to a unsigned 8 for display purposes
	return img
