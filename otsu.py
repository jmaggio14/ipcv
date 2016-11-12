import numpy as np
from sys import exc_info
from os.path import split
import ipcv

def otsu_threshold(img, maxCount=255, verbose=False):
	"""
	:NAME:
		otsu_threshold

	:PURPOSE:
		this method generates a binary thresholded image based off of 
		Otsu's class discrimination method

	:CATEGORY:
		ipcv -- object recognition and thresholding tool

	:CALLING SEQUENCE:
		quantizedImage = quantize(img = inputImage,\
								 maxCount = max display level\
								 verbose = true or false)

	:INPUTS:
		img
			[numpy.ndarray]	input image to be quanitized
		maxCount
			[int] maximum pixel value in the output array
		verbose
			[boolean] whether or not to graph the histogram 

	:RETURN VALUE:
		tuple containing:
			returnTuple[0] -- binary numpy.array of the same shape as the input image
			returnTuple[1] -- threshold determined by otsu's method


	:ERROR CHECKING:
		TypeError
		ValueError
		RuntimeError

	:REQUIRES:
		np
		sys.exc_info
		os.path.split
		ipcv

	:MODIFICATION HISTORY:
		Engineer:	Jeff Maggio
		08/25/16:	otsu code

	"""
######################  BEGIN ERROR CHECKING  #######################
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


######################  END ERROR CHECKING  #######################

	try:

		numberCounts = maxCount + 1
		#generating the pdf and cdf
		hist,pdf,cdf = ipcv.histogram(img,histSize=numberCounts,ranges=[0,numberCounts])
		
		meanLevelArray = np.cumsum( np.arange(0,numberCounts) * pdf )
		muTotal = meanLevelArray[-1]

		sigmaSquaredBValues = np.zeros(numberCounts)
		startingK = np.where(cdf>0.0)[0][0]
		endingK = np.where(cdf<1.0)[0][-1]

		for k in range(startingK, endingK):
			muK = meanLevelArray[k]
			omegaK = cdf[k]
			sigmaSquaredB = ( ( (muTotal * omegaK) - muK )**2 ) / ( omegaK * (1-omegaK) )
			sigmaSquaredBValues[k] = sigmaSquaredB

		threshold = np.argmax(sigmaSquaredBValues)

		LUT = np.zeros( numberCounts )
		LUT[threshold+1:] = 1

		img = LUT[img]

		if verbose == True:
			values = (pdf,)
			colors = ('r',)
			filename = "image_pdf_wOtsu.eps"
			thresholdMarker = (threshold,)
			labels = ("pdf",)
			graph = ipcv.quickplot(values,colors,labels,filename=filename,verticalMarkers=thresholdMarker,\
				xLabel="Digital Counts",yLabel="probability",display=False)
			graph.annotate("otsu's Threshold", xy=(threshold, .01), xytext=(3, 1.5),arrowprops=dict(facecolor='black', shrink=0.05))
			graph.show()

		return img.astype(np.uint8), threshold


	except Exception as e:
		print("===============================================================")
		exc_type, exc_obj, tb = exc_info()
		fname = split(tb.tb_frame.f_code.co_filename)[1]
		print("\r\nfile: {0}\r\n\r\nline: {1} \r\n\r\n{2}\r\n\r\n".format(fname,tb.tb_lineno,exc_obj,e))
		print("===============================================================")


if __name__ == '__main__':

	 import cv2
	 import ipcv
	 import os.path
	 import time

	 home = os.path.expanduser('~')
	 # filename = home + os.path.sep + 'src/python/examples/data/lenna.tif'
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



  #                                          ,╓╖╗╗╗╣╣▄╦,                          
  #                                 ,╓╦╗╬╣╬▓▓▓▓▓▓▓▓▓▓█▓▓▌⌐                        
  #                               ╣▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓█████▓▓µ                       
  #                               ▀█████▓▓▓▓▓▓▓▓▓▓▓██████▓▓▄                      
  #                                ▀███████████▓▓▓▓█████████▓µ                    
  #                                 ╙██████████████▓▓▓▓▓▓▓▓▓▓▓⌐                   
  #                                   ▓████████████████▓▓▓▓▓▓▓▌                   
  #                                    ╙█████████████████▓▓▓▓▓▓▒                  
  #                                      ▐██████████████▓▓▓▓▓▓▓▓µ                 
  #                                       ╫███████████▓▓▓▓▓▓▓▓▓▓▓⌐                
  #                                       ╫███████████▓▓▓▓▓▓▓▓▓▓█▓⌐               
  #                                      ▄████████████▓▓▓▓▓▓▓▓▓███▓               
  #                                    ╓▓▓█████████████████▓▓▓▓▓███▓              
  #                            ,,╗▄▓▓▓▓█▓███████████████████▓▓▓▓▓▓▓█▓⌐            
  #                      ,╓╓╦╬▓▓▓▓█████████▀╠████████▓▓▓██████▓▓▓▓▓▓█▓            
  #                 ╓╦╣▓▓▓▓▓▓▓▓▓▓███████▀`  ╫█████▓▓▓▓▓▓▓█▓▓████▓▓▓▓▓█▄,,╓▄       
  #             ╥╬▓▓▓▓▓▓▓▓▓▓██████▓▀▀▀      ▓████▓▓▓▓▓▓▓▓█████▓▓█▓▓▓▓▓▓▓▓▀        
  #         ,╗╣▓▓▓▓▓████████▀▀╙            ]█████▓▓▓▓▓▓▓▓█████▓▓▓▓▓▓▓██╨          
  # ╦▄▄▄▓▓▓▓▓▓███▀▀▀▀▀▀╙                   ║████▓▓▓▓▓▓▓███████▓▓▓▓▓███▓           
  # ╙╙▀▀████████▀                          ║███████▓▓▓████████▓▓▓█████▌           
  #     ╙╙`╙▀▀                             '██████████████████████▓▓▓█Ö           
  #                                         ╠█████████████████████▓▓▓▓▌⌐          
  #                                        ,▓██████████████████████▓▓▓▓▓ç         
  #                                       ╓▓███████████████████████▓▓▓▓▓▓▓╦       
  #                                      ╬██████████████████████████▓▓▓▓▓▓▓µ      
  #                                     ╫███████████████████████████▓▓▓▓▓▓█▓▄     
  #                                    ▓████████████████████████████▓▓▓▓▓▓▓██µ    
  #                                   ▓███████████████▀▀▀▓███████████▓▓▓▓▓▓▓█▌    
  #                                  ╫█████████████▀▄▓███████████████▓▓▓▓▓▓▓▓█∩   
  #                                ▄▓██████████▀▐▄████████████████████▓▓▓▓▓▓▓█▄   
  #                              ,▓███████▀▀    ╫██████▓██▓▓▀▀▀▀▀▀▀▀▓█▓▓▓▓▓███▌   
  #                              ╣██████▒               ▓▓          "▓█▓▓▓▓███▀   
  #                             ╓▓▓▓█████╕              ▓▓           `▓█▓▓▓███∩   
  #                              ▓█▓▓▓████▄             ▓▌            └▓▓▓▓███    
  #                               ▀██▓▓▓████Q          ▐▓▌            ╓▓▓▓▓██▌    
  #                                `▀▓███████▄         ╠╬▌           ║▓▓▓▓▓▓█∩    
  #                                   ╙▀██▓███▓╕     ╓╬▓▌╬╬⌐        ╔▓▓▓▓▓▓▓█∩    
  #                                      ╙▀▓████▌▄▄▄▄▓▓█▄╬╬▄,      ,▓▓▓▓▓▓███∩    
  #                                         ▐▓███████████▒▓███▓▄,  ╬█▓▓▓▓▓██▌     
  #                                       ╓▄█████████████▒▓███████▄▓▓▓▓▓▓███∩     
  #                                     ╗▓█████████████▌╠╬▓█████████▓▓▓▓▓██▓      
  #                                   ╓▓█████████▄▓██▓█▒╫╬▓▌█Ü▀████▓▓▓▓▓███∩      
  #                                  ▄█████████████▓▓██Ö╠╬▓█▀  .▓██▓▓▓▓███▌       
  #                                .▓████▓█╨  ╙██▌ ╠▓█▓ ╠╬█▓   ╫▓▓█▓▓▓▓███∩       
  #                               ╓▓███▓█▓▓,   ╙██µ╠▓▓█⌐▌╬█∩  ╬█▀▓▓▓▓▓████        
  #                              ╓▓███▓██▄▒▀▄    ██╠╬▓▓⌐▌╫▌  ▄█╨╓█▓▓▓▓████▌       
  #                              ▓███▓█▀ ╙▀▓▄▓▄   ▓▓╬╫█µ╬▌  ▄▌  ╠█▓▓▓██████∩      
  #                             ║████▓▌     ╙▓█▓⌐ ²█▓▓█▄╬▓╦▓▌  ╓▓▓▓▓▓██████▌      
  #                             ████▓█▀▄▄,     ▀█▄ ╠████╬▓█▌ ╓▓▓▓▓▓▓██▀█████      
  #                            ╓████▓█▓▄▄▓▓▓▄▄   ╙█▓▓█▓█╬▓▓▄▓╨ ╓▓▓▓██▓▓█████      
  #                            ╠███▓█▒    ╙╙▀▀▓▓▓▄▓▓████╬▓█▄▄▄▄▓▓▓▓█▓╝╝█████      
  #                            ▓███▓█           ;▓▓████▌▒▒╬╬▌╙╠▓▓▓█▓   █████      
  #                            ▓███▓█╦▄▄╣▀▓▓███▓▀▀▒▓█████▓▓▀▓▓▓▓▓▓█▒  ┌█████      
  #                            ▓███▓█▄▄╣▀▀▀`'  ,▄▓▀▓█████▒▓▄µ╠▓▓▓██▓▀▀▓████▌      
  #                            ▀███▓█▌      ,▄██▀╓▓█╢███▓▒▌ ▀█▓▓██╨╙▀▀█████▒      
  #                            ]██████   ╓▄▓▓▓╨ ╓██Ü▓█▓██▒▓▌╠▓▓▓█▒   ▄████▓       
  #                             ▓███▓█▌▓▀▀▓▓╨  ▄██∩╔█▌╫█▓╬▓█▓▓▓█▓▀▄ ╓█████∩       
  #                             ╚██████▄▓▀   ,▓▓▓  ▓█▒]█▓╫▒█▓▓▓█∩ `▓█████▀        
  #                              ▀████▓█╦   ╓▓▄▓  ╫▓▓ ]█▓╫Q╣▓▓█▀  ▄█████▀         
  #                               ▓██████▄ ╬▓▄▓  ╓█▓▌ ]█▌╫▒▓▓▓█▄╓▓█████▌          
  #                                ▀███████▌▓▓   ▓▌▓∩  ▓▒╬▄▓█▓▓▓▓▓████▀           
  #                                 ╙████████▄  ╓█╢▌   ▓▓███████████▀▀Θ           
  #                                   ▀██████████▓▓▄,╓▄████████████╨              
  #                                     ▀███████████████████████▀╨                
  #                                       ╙▀█████████████████▀╙                   
  #                                           ╙╙▀▀▓██▀▀▀▀▀                       
