import collections 
dict_1 = {'a': 100, 'b': 200}
dict_2 = {'a': 200, 'c': 300}
dict_3 = {'a': 300, 'd': 100}
def combine_dicts(*args):
	counter = collections.Counter()
	for v in args:
		counter.update(v)
	result = dict(counter)

	print("result:", str(counter))


print(combine_dicts(dict_1, dict_2, dict_3))