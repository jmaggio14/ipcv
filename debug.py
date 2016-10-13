
def debug(exception):
	"""
	simple method to remove unecessary clutter in debugging
	meant to be called exclusively in a try statement

	simply prints the file,line and exeption has occured in more organized
	and easily readable fashion
	"""
	from sys import exc_info
	from os.path import split
	exc_type, exc_obj, tb = exc_info()
	fname = split(tb.tb_frame.f_code.co_filename)[1]
	line = tb.tb_lineno
	
	print("===============================================================") 		
	print("\r\nfile: {0}\r\n\r\nline: {1} \r\n\r\n{2}\r\n".format(fname,line,exception))
	print("===============================================================")


