
import numpy as np
import sys
import os.path

def debug(exception):
	"""
	simple method to remove unecessary clutter in debugging
	meant to be called exclusively in a try statement

	simply prints the file,line and exeption has occured in more organized
	and easily readable fashion
	"""
	exc_type, exc_obj, tb = sys.exc_info()
	fname = os.path.split(tb.tb_frame.f_code.co_filename)[1]
	line = tb.tb_lineno
	
	print("===============================================================") 		
	print("\r\nfile: {0}\r\n\r\nline: {1} \r\n\r\n{2}\r\n".format(fname,line,exception))
	print("===============================================================")
	raise SystemExit





def type_check(var,types,varName="var"):
	types = tuple(types)
	if isinstance(var,types) == False:
		print("-----------------------------------------------------------")
		print("                       TYPE ERROR                       \n")
		print("'{0}' must be one of the following types: {1}".format(varName,types))
		print("\n-----------------------------------------------------------")
		raise TypeError

def value_check(var,values,checkType,varName="var"):

	if checkType in ["discrete","d"]:
		"""
		Discrete -- check whether to see if the 'var' is in the 'values' set
		"""
		if var not in values:
			print("-----------------------------------------------------------")
			print("                       VALUE ERROR                       \n")
			print("'{0}' must be one of the following values {1}".format(varName,values))
			print("\n-----------------------------------------------------------")
			raise ValueError
	
	elif checkType in ["forbidden","f"]:
		values = (values,) if ( (type(values) in [list,tuple]) == False ) else values 
		"""
		Forbidden -- checks whether the 'var' is in the set of forbidden 'values'
		"""
		if var in values:
			print("-----------------------------------------------------------")
			print("                       VALUE ERROR                       \n")
			print("'{0}' must be cannot be one of the following values {1}".format(varName,values))
			print("\n                                                          ")
			print("\n-----------------------------------------------------------")
			raise ValueError
	
	elif checkType in ["boundary","b"]:
		"""
		Boundry -- checks whether the 'var' is in the range (value[0] , value[1])
		"""
		if values[0] == ":":
			if var > values[1]:
				print("-----------------------------------------------------------")
				print("                       VALUE ERROR                       \n")
				print("'{0}' must larger than {1}".format(varName,values[0]))
				print("\n                                                          ")
				print("\n-----------------------------------------------------------")
				raise ValueError

		elif values[1] == ":":
			if var < values[0]:
				print("-----------------------------------------------------------")
				print("                       VALUE ERROR                       \n")
				print("'{0}' must less than {1}".format(varName,values[1]))
				print("\n                                                          ")
				print("\n-----------------------------------------------------------")
				raise ValueError
		else:
			if var > values[1] or var < values[0]:
				print("-----------------------------------------------------------")
				print("                       VALUE ERROR                       \n")
				print("'{0}' must be in range {1}".format(varName,values))
				print("\n                                                          ")
				print("\n-----------------------------------------------------------")
				raise ValueError

	elif checkType in ["greater than","greater",">","g"]:
		"""
		Greater than -- checks to see if the 'var' is greater than 'values'
		"""
		values = values[0] if type(values) in (tuple,list) else values
		if var < values:
			print("-----------------------------------------------------------")
			print("                       VALUE ERROR                       \n")
			print("'{0}' must be greater than {1}".format(varName,values))
			print("\n                                                          ")
			print("\n-----------------------------------------------------------")
			raise ValueError

	elif checkType in ["less than","less","<",'l']:
		values = values[0] if type(values) in (tuple,list) else values
		if var > values:
			print("-----------------------------------------------------------")
			print("                       VALUE ERROR                       \n")
			print("'{0}' must be less than {1}".format(varName,values))
			print("\n                                                          ")
			print("\n-----------------------------------------------------------")
			raise ValueError


	elif checkType in ["equals","e","="]:
		if var != values:
			print("-----------------------------------------------------------")
			print("                       VALUE ERROR                       \n")
			print("'{0}' must be equal to {1}".format(varName,values))
			print("\n                                                          ")
			print("\n-----------------------------------------------------------")
			raise ValueError			
"""
---------------------------------------------------------------------------------
           UNABLE TO EFFECTIVELY CREATE CUSTOM ERRORS --> come back later     
---------------------------------------------------------------------------------     
"""

# def array_type_check(array1,array2,array1Name="array1",array2Name="array2"):
# 	if array1.dtype != array2.dtype:
# 		raise ArrayTypeError(array1,array2)
# 		print("Is this working")


# class ArrayTypeError(Exception):
# 	"""
# 	Raise in the event that two arrays are not of the same Type

# 	This must be called after the arrays have already be validated to be numpy arrays
# 	"""
# 	def __init__(self,array1,array2,message="array types incompatible"):
# 		self._a1Type = array1.dtype
# 		self._a2Type = array2.dtype
# 		self.message = message
		# super(ArrayTypeError,self).__init__(message,array1,array2)


# class ArrayShapeError(Exception):
# """
# Raise in the event that two arrays are not the same size

# This must be called after the arrays have already be validated to be numpy arrays
# """
# 	def __init__(self,message="array ",array1,array2):
# 		self._array1Shape = array1.shape
# 		self._array2Shape = array2.shape
# 		self._message = "arrays sizes incompatible\r\n\r\narray1:{0}\r\narray2{2}".format(self._array1Shape,self._array2Shape)

# 		super(ArrayShapeError,self).__init__(message,array1,array2)



# if __name__ == "__main__":
# 	import numpy as np
# 	a = np.asarray( [1,2,3,4,5] )
# 	b = np.asarray( [1.0,2.0,3.0,4.0,5.0] )

# 	array_type_check(a,b)