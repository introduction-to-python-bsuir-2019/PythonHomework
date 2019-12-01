
result = "None"

def dec_resultremember(original_function):
	
	def wrapper_function(*args,**kwargs):
		global result
		print("last result was {}".format(result))
		result =  original_function(*args,**kwargs)
		return original_function(*args,**kwargs)
	return wrapper_function





@dec_resultremember
def display_info(name,age):
	print('display_info ran with arguments ({},{})'.format(name,age))

display_info('John ',25)

display_info('Bob',256)
