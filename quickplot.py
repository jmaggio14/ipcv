import matplotlib.pyplot as plt
import ipcv
import numpy as np

def quickplot(values,colors,labels=None,filename=None,display=True,save=False,\
						xLimits=(0,255),verticalMarkers = None, horizontalMarkers = None,\
						xLabel = None,yLabel=None):
	# ERROR CHECKING
	if isinstance(values,(tuple,np.ndarray)) == False:
		print("\r\ninput 'values' must be a tuple or structured numpy array currently {0}\r\n".format(type(values)))
		raise TypeError
	if isinstance(colors,tuple) == False:
		print("\r\ninput 'colors' must be a tuple currently {0}\r\n".format(type(colors)))
		raise TypeError
	if isinstance(filename,(str,type(None))) == False:
		print("\r\ninput 'filename' must be string or NoneType, currently{0}\r\n".format(type(filename)))
		raise TypeError
	if isinstance(labels,(tuple,type(None))) == False:
		print("\r\ninput 'labels' must be tuple or NoneType, currently{0}\r\n".format(type(labels)))
		raise TypeError
	if len(values) != len(colors):
		print("\r\nvalues and colors must be a tuple of the same length\r\n")
		raise ValueError
	if isinstance(verticalMarkers,(tuple,type(None))) == False:
		print("\r\nverticalMarker must be of tuple or NoneType, currently{0}\r\n".format(type(verticalMarkers)))
		raise TypeError
	if isinstance(horizontalMarkers,(tuple,type(None))) == False:
		print("\r\nhorizontalMarker must be tuple or NoneType, currently{0}\r\n".format(type(horizontalMarkers)))
		raise TypeError
	if isinstance(xLabel,(type(None),str))==False:
		print("\r\nxLabel must be string or NoneType, currently{0}\r\n".format(type(xLabel)))
		raise TypeError
	if isinstance(yLabel,(type(None),str))==False:
		print("\r\nyLabel must be string or NoneType, currently{0}\r\n".format(type(yLabel)))
		raise TypeError
	
	try:
		#THIS IS TERRIBLE CODING AND NEEDS TO BE FIXED AT SOME POINT
		# if sArray == False:

		if isinstance(labels,type(None)):
			numberPlots = len(colors)
			labels = []

			for plotNumber in range(numberPlots):
				name = "set {0}".format(plotNumber)
				labels.append(name)

		elif len(labels) != len(colors):
			print("\r\nthere must a label for every plot, or none at all\r\n")
			raise ValueError

		#iterating through the lists to return
		plots = []
		for index in range(len(values)):
			color = colors[index]
			data = values[index]
			label = labels[index]
			axes = plt.plot(data,color=color,label=label)
			plots.append(axes)
		plt.legend(handles = plots,labels =labels)

		if isinstance(verticalMarkers,tuple):
			for verticalMarker in verticalMarkers:
				plt.axvline(verticalMarker)

		if isinstance(horizontalMarkers,tuple):
			for horizontalMarker in horizontalMarkers:
				plt.axhline(horizontalMarker)

		if isinstance(xLabel,str):
			plt.xlabel(xLabel)
		if isinstance(yLabel,str):
			plt.ylabel(yLabel)



		plt.xlim(xLimits)

		if isinstance(filename,str):
			plt.title(filename)
			if save == True:
				plt.savefig(filename)
		elif isinstance(filename,str) == False and save == True:
			print("\r\ncannot save figure without valid filename\r\n")
			raise RuntimeError

		if display == True:
			plt.show()

		return plt

	except Exception as e:
		ipcv.debug(e)


