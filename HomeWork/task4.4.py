a = "I am global variable!"


def enclosing_function():
	
	a = "This is enclosing variable"
	def inner_function():
		
		global a 
		print(a)
	inner_function()

enclosing_function()

	


