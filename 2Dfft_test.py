import numpy as np
import cv2
import os.path
import ipcv

def display(img,name='test'):
	cv2.namedWindow(name,cv2.WINDOW_AUTOSIZE)
	cv2.imshow(name,img)
	ipcv.flush()


if __name__ == "__main__":

	home = os.path.expanduser('~')
	filename = home + os.path.sep + 'src/python/examples/data/lenna.tif'
	# filename = home + os.path.sep + 'src/python/examples/data/giza.jpg'
	img = cv2.imread(filename)


	# display(img)
	F = np.fft.fft(img)
	F = np.fft.fftshift(F)
	F = np.sqrt( np.real(F)**2 + np.imag(F)**2 )
	display(F)

	maxes = np.flipud( np.argsort( fft.flatten() ) )
	print(maxes)
	np.savetxt(maxes,'test.txt')


	# freqIndex = maxes[5]
	# freq = fft.flat[]

