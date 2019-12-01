result = "Hutle"
def test_func():
	global  result
	result = 'hello'
	def inner():
		result = 'Hi'
	inner()

test_func()
print(result)

