def int_tuple(number):
	empty_list = []
	str_num = str(number)
	[empty_list.append(i) for i in str_num]
	
	print(tuple(empty_list))

	

int_tuple(132542356)

