
result = "None"

def dec_resultremember(original_function):
	
	def wrapper_function(*args,**kwargs):
		global result
		print("last result was {}".format(result))
		result =  original_function(*args,**kwargs)
		return original_function(*args,**kwargs)
	return wrapper_function





@dec_resultremember
def display_info(a,b):
	return a + b

display_info(36,25)

display_info(48,256)
display_info(44,256)
