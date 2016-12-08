import numpy as np
import ipcv
import cv2
import sys

def fft_display(img, videoFilename=None):
	try:
		img = img.copy().astype(ipcv.IPCV_64F)

		dims = ipcv.dimensions(img)
		r,c = dims["rows"],dims["cols"]
		template = np.zeros( (r,c) ).astype(ipcv.IPCV_64F)
		temp = template.copy().astype(ipcv.IPCV_128C)

		# generating FFT
		# FFT = np.fft.fftshift(np.fft.fft(img))
		# FFT = np.fft.fftshift( np.fft.fft2(img) )
		# logFFT = np.log( np.abs( FFT / np.sqrt(FFT.size) ) ).astype(ipcv.IPCV_8U)

		FFT = np.fft.fft2(img)
		# print("AVERAGE VALUE IS EQUAL TO:",FFT.flat[0])
		FFTsrc = np.fft.fftshift( FFT )
		FFT = np.abs( FFTsrc )

		print("FFT MAX IS EQUAL TO:",np.max(FFT))
		print("FFT MIN IS EQUAL TO:",np.min(FFT))

		logFFT = np.log10( FFT ) 

		# logFFT = FFT
		logFFT = logFFT - np.min(logFFT)
		logFFT = (( logFFT / np.max(logFFT) ) * 255).astype(ipcv.IPCV_64F)




		# creating array to populate with maximum value indices
		sortedArray = np.argsort( FFT.flatten() )
		maximumIndices = np.flipud( sortedArray )

		used = template.copy()
		current = template.copy()
		currentScaled = template.copy()
		summed = template.copy()
		
		#creating writer and image window
		cv2.namedWindow(videoFilename)
		writer = create_video_writer(img.shape,videoFilename)

		avgValue = FFT[0]



		for freqIndex in maximumIndices:
			# puting frequency in 'used' array
			used.flat[freqIndex] = logFFT.flat[freqIndex]


			# returning the spatial sine wave for freq
			temp.flat[freqIndex] = FFTsrc.flat[freqIndex]
			current = np.fft.ifft2( temp )
			temp.flat[freqIndex] = 0

			print("MAX IS EQUAL TO:",np.max(current))
			print("MIN IS EQUAL TO:",np.min(current))

			#scaling the current
			c = np.abs(current.real)
			currentScaled = ( (c - np.min(c) ) )
			currentScaled = (currentScaled / np.max(currentScaled) ) * 255

			#summing up all the freq
			summed = (summed + current)

			#stiching all images together
			frame = stich(img,logFFT,used,np.abs(current.real)+avgValue,currentScaled, np.abs( summed.real ) )

			print("frame dataType =",frame.dtype)
			#writing frame
			if writer.isOpened():
				writer.write(frame)

			#displaying image
			cv2.imshow(videoFilename,frame)


			action = ipcv.flush()
			if action == "pause":
				action = ipcv.flush()
				if action == "pause":
					continue

			elif action == "exit":
				writer.release()
				sys.exit()

	except Exception as e:
		ipcv.debug(e)

def get_key(waitTime):
	pass

def create_video_writer(imgShape,videoFilename):
	codec = cv2.VideoWriter_fourcc('M', 'P', 'E', 'G')
	fps = 30
	isColor = True
	videoShape = ( imgShape[1],imgShape[0] )
	writer = cv2.VideoWriter(videoFilename,codec,fps,videoShape,isColor)
	return writer

def stich(img,logFFT,used,current,currentScaled,summed):
	# stiching together top
	top = np.hstack( (img,logFFT,used) )
	# stiching together bottom
	bottom = np.hstack( (summed,current,currentScaled) )
	# final collage
	final = np.vstack( (top,bottom) ).astype(ipcv.IPCV_8U)
	return final



if __name__ == '__main__':

	import cv2
	import ipcv
	import os.path

	home = os.path.expanduser('~')
	filename = home + os.path.sep + 'src/python/examples/data/lenna.tif'

	im = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)

	print("AVERAGE IS EQUAL TO: ",np.mean(im))
	if im is None:
		print('ERROR: Specified file did not contain a valid image type.')
		sys.exit(1)

	# ipcv.fft_display(im)
	ipcv.fft_display(im, videoFilename='fft_display.mpg')
