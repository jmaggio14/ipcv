import numpy as np
from sys import exc_info
from os.path import split
import ipcv

def otsu_threshold(img, maxCount=255, verbose=False, discriminant = 'eta'):
	
#######################  BEGIN ERROR CHECKING  #######################
	if isinstance(img,np.ndarray) == True:
		dims = ipcv.dimensions(img,"dictionary")

		if dims["bands"] == 1:

			if len(img.shape) == 3:
				#making the array two dimensional if it only has 1 band
				img = img.reshape(dims['rows'],dims['cols'])

		else:
			print("")
			print("input 'img' must be grayscale or single-banded")
			print("")
			raise RuntimeError

	else:
		print("")
		print("input 'img' must be a valid 2 dimensional numpy array, currently {0}".format(type(img)))
		print("")
		raise TypeError

	if isinstance(maxCount,int) == False:
		print("")
		print("input 'maxCount' must be an int, currently {0}".format(type(maxCount)))
		print("")
		raise TypeError
	elif maxCount <= 0:
		print("")
		print("input 'maxCount' must be greater than zero")
		print("")
		raise ValueError

	if isinstance(verbose,bool) == False:
		print("")
		print("input 'verbose' must be integer boolean , currently {0}".format(verbose))
		print("")
		raise TypeError

	if discriminant != "eta" and discriminant != 'lambda' and discriminant != 'kappa':
		print("")
		print("input 'discriminant' must equal to 'eta', 'lambda' or 'kappa'")
		print("")
		raise ValueError
#######################  END ERROR CHECKING  #######################

	try:
		hist,pdf,cdf = ipcv.histogram(img,histSize=(maxCount+1),ranges=[0,maxCount+1])
		muTotal = np.mean(cdf)
		numberCounts = len(cdf)


		sigmaSquaredBValues = []
		for k in range( numberCounts ):
			muK = np.mean(cdf[:k])
			omegaK = cdf[k]
			if omegaK != 0.0 and omegaK != 1.0:
				sigmaSquaredB = ( ( (muTotal * omegaK) - muK )**2 ) / ( omegaK * (1-omegaK) )
				sigmaSquaredBValues.append(sigmaSquaredB)

		kOptimal = np.argmax(sigmaSquaredBValues)

		LUT = np.zeros( numberCounts )
		LUT[:kOptimal] = 0
		LUT[kOptimal:] = 255

		img = LUT[img] 


		return img.astype(np.uint8), kOptimal



	except Exception as e:
		print("===============================================================")
		exc_type, exc_obj, tb = exc_info()
		fname = split(tb.tb_frame.f_code.co_filename)[1]
		print("\nfile: {0}\n\nline: {1} \n\n{2}\n".format(fname,tb.tb_lineno,e))
		print("===============================================================")


if __name__ == '__main__':

	 import cv2
	 import ipcv
	 import os.path
	 import time

	 home = os.path.expanduser('~')
	 filename = home + os.path.sep + 'src/python/examples/data/giza.jpg'

	 im = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
	 print('Filename = {0}'.format(filename))
	 print('Data type = {0}'.format(type(im)))
	 print('Image shape = {0}'.format(im.shape))
	 print('Image size = {0}'.format(im.size))

	 startTime = time.time()
	 thresholdedImage, threshold = ipcv.otsu_threshold(im, verbose=True)
	 print('Elapsed time = {0} [s]'.format(time.time() - startTime))

	 print('Threshold = {0}'.format(threshold))

	 cv2.namedWindow(filename, cv2.WINDOW_AUTOSIZE)
	 cv2.imshow(filename, im)
	 cv2.namedWindow(filename + ' (Thresholded)', cv2.WINDOW_AUTOSIZE)
	 cv2.imshow(filename + ' (Thresholded)', thresholdedImage * 255)

	 action = ipcv.flush()