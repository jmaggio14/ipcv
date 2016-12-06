import numpy as np
import ipcv
import cv2
import sys

def fft_display(img, videoFilename=None):
	try:
		img = img.copy()

		dims = ipcv.dimensions(img)
		r,c = dims["rows"],dims["cols"]
		temp = np.zeros( (r,c) )

		# generating FFT
		# FFT = np.fft.fftshift(np.fft.fft(img))
		# FFT = np.fft.fftshift( np.fft.fft2(img) )
		# logFFT = np.log( np.abs( FFT / np.sqrt(FFT.size) ) ).astype(ipcv.IPCV_8U)

		FFT = np.fft.fft2(img)
		# print("AVERAGE VALUE IS EQUAL TO:",FFT.flat[0])
		FFT = np.fft.fftshift( FFT )
		FFT = np.abs( FFT )
		logFFT = np.log10( FFT )
		logFFT = ( logFFT / np.max(logFFT) ) * 255


		print("MAX IS EQUAL TO:",np.max(logFFT))
		print("MIN IS EQUAL TO:",np.min(logFFT))


		# creating array to poulate with maximum values
		maximumValues = np.flipud( np.argsort( logFFT.flatten() ) )

		used = temp.copy()
		current = temp.copy()
		currentScaled = temp.copy()
		summed = temp.copy()
		
		#creating writer and image window
		cv2.namedWindow(videoFilename)
		writer = create_video_writer(img.shape,videoFilename)


		for freqIndex in maximumValues:
			# puting frequency in 'used' array
			used.flat[freqIndex] = logFFT.flat[freqIndex]

			# returning the spatial sine wave for freq
			temp.flat[freqIndex] = logFFT.flat[freqIndex]
			current = np.fft.ifft2( temp )
			temp.flat[freqIndex] = 0


			print("MAX IS EQUAL TO:",np.max(current))
			print("MIN IS EQUAL TO:",np.min(current))
			

			#scaling the current
			currentScaled = ( (current - np.min(current) ) / np.max(current) ) * 255

			#summing up all the freq
			summed = summed + current

			#stiching all images together
			frame = stich(img,logFFT,used,current,currentScaled,summed)

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

def create_video_writer(imgShape,videoFilename):
	codec = cv2.VideoWriter_fourcc('M', 'P', 'E', 'G')
	fps = 30
	isColor = True
	videoShape = ( imgShape[1],imgShape[0] )
	writer = cv2.VideoWriter(videoFilename,codec,fps,videoShape,isColor)
	return writer

def convert_to_argand(fft):
	mag = np.abs(fft)
	imag = np.imag(fft)
	real = np.real(fft)
	phase = np.atan( imag/real )


def stich(img,logFFT,used,current,currentScaled,summed):
	# stiching together top
	top = np.hstack( (img,logFFT,used) )
	# stiching together bottom
	bottom = np.hstack( (current,currentScaled,summed) )
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