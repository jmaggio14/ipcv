
import numpy as np

def type_check(var,types,varName):
	if isinstance(var,types) == False:
		print("-----------------------------------------------------------")
		print("                       TYPE ERROR                       \n")
		print("'{0}' must be one of the following types: {1}".format(varName,types))
		print("\n-----------------------------------------------------------")
		raise TypeError

def value_check(var,checkType,values,varName):
	if checkType in ["discrete","d"]:
		if var not in values:
			print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
			print("                       VALUE ERROR                       \n")
			print("'{0}' must be one of the following values {1}".format(varName,values))
			print("\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
			raise ValueError
	
	elif checkType in ["forbidden","f"]:
		if var in value:
			print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
			print("                       VALUE ERROR                       \n")
			print("'{0}' must be cannot be one of the following values {1}".format(varName,values))
			print("\n                                                          ")
			print("\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
			raise ValueError
	
	elif checkType in ["boundary","b"]:
		if values[0] == ":":
			if var > values[1]:
				print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
				print("                       VALUE ERROR                       \n")
				print("'{0}' must larger than {1}".format(varName,values[0]))
				print("\n                                                          ")
				print("\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
				raise ValueError

		elif values[1] == ":":
			if var < values[0]:
				print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
				print("                       VALUE ERROR                       \n")
				print("'{0}' must less than {1}".format(varName,values[1]))
				print("\n                                                          ")
				print("\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
				raise ValueError
		else:
			if var > values[1] or var < values[0]:
				print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
				print("                       VALUE ERROR                       \n")
				print("'{0}' must be in range {1}".format(varName,values))
				print("\n                                                          ")
				print("\n-----------------------------------------------------------")
				raise ValueError
