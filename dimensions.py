def dimensions(im,returnType = "tuple"):
	dimensions = im.shape
	numberRows = dimensions[0]
	numberColumns = dimensions[1]
	if len(dimensions) == 3:
		numberBands = dimensions[2]
	else:
		numberBands = 1
	dataType = im.dtype

	if returnType == "tuple":
		return numberRows, numberColumns, numberBands, dataType
	elif returnType == "dictionary":
		return {"rows":numberRows,"cols":numberColumns,"bands":numberBands,"dtype":dataType}

