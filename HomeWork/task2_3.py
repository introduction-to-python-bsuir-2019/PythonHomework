import collections
def count_values(phrase:str)->dict:
	
	d = collections.defaultdict(int)
	for letter in phrase:
		d[letter] +=1
	print(d)

print(count_values("Hello my dear friend"))

def count_values2(phrase)->dict:
	result = collections.Counter(phrase.lower())
	print(result)

print(count_values2("Hello my dear friend h"))