import numpy as np
from scipy import misc
import cv2



class Hologram(object):

	def __init__(self,src,autoDebug=False):
		self._autoDebug = autoDebug
		self._src = src.copy()
		self._img = misc.imresize(self._src,800,interp="nearest").astype(np.complex128)
		self._g = None
		self._tmp = None


	def compute(self):
		self.randomize()
		self.imgFFT()
		self.mag()
		self.phase()
		self.normalize()
		self.quantize_magnitude()
		self.quantize_phase()
		self.bars()


	def randomize(self):
		self._randomArray = (np.random.rand(self._img.shape[0],self._img.shape[1]) - .5) * (2 * np.pi)
		self._tmp = np.exp(1j * self._randomArray)
		self._g = self._img * self._tmp
		return self._g

	def imgFFT(self):
		self._fft = np.fft.fft(self._g)
		return self._fft

	def mag(self):
		self._mag = np.abs(self._fft)
		return self._mag

	def phase(self):
		self._phase = np.angle(self._fft)
		return self._phase

	def normalize(self):
		self._normalized = self._mag / np.max(self._fft)
		return self._normalized

	def quantize_magnitude(self):
		self._quantizedMagnitude = np.round(self._normalized * 8)
		if self._autoDebug == True:
			print(self._quantizedMagnitude)
			print( np.unique(self._quantizedMagnitude) )

		return self._quantizedMagnitude

	def quantize_phase(self):
		self._quantizedPhase = np.floor( 8 * self._phase / (2 * np.pi) )
		
		if self._autoDebug == True:
			print(self._quantizedPhase)
			print( np.unique(self._quantizedPhase) )

		return self._quantizedPhase


	def bars(self):
		blackRef = np.zeros( (8,8) )
		base = np.transpose(np.zeros( (8) ) )

		for ind,phase in enumerate( self._quantizedPhase.flatten() ):
			height = self._quantizedMagnitude.flat[ind]
			bar = blackRef.copy()
			bar[8:8-height, phase] = 1
			base = np.hstack( (base, bar) )

		self._barImg = base[:,1:].reshape( (512, 512) )
		#bars = []
		#for index,phase in enumerate( self._quantizedPhase.flatten() ):
			#height = self._quantizedMagnitude.flat[index]
			#bar = blackRef.copy()
			#bar[8:8-height,phase] = 1
			#bars.append(bar)
			# if index == 1:
			# 	print(bar.shape)
			# 	self.display(bar)

		# self._barImg = np.ones( (64*8,64*8) )
		# for i in range(512):
		# 		row = (i // 8)
		# 		col = (i % 8)
		# 		tmpBar = bars[i]
		# 		self._barImg[row:row+8,col:col+8] =  tmpBar


		if self._autoDebug == True:
			print(self._barImg.shape)
			self.display(self._barImg)


	def display(self,input1):
		cv2.imshow("test",input1)
		cv2.waitKey(100000)


if __name__ == "__main__":
	img = cv2.imread("heart.png",cv2.IMREAD_GRAYSCALE)
	hologram = Hologram(img,True)
	hologram.compute()
