test_strings = ["hello", "world", "python", ]
def test_1_1(string_list)-> set:
	b = []
	dct = {}
	st = frozenset()
	[b.append(set(word)) for word in string_list]
	for i in b:
		if i in dct:
			dct[i]+=1
		elif dct[i] > len(string_list):
			st.add(dct[i])
		else:
			dct[i] = 1
		

		
	

test_1_1(test_strings)




