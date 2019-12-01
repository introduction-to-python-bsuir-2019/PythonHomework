def split_by_index(s,indices):
	indices.append(None)
	parts = [s[indices[i]:indices[i+1]] if indices[i] < len(s) else print(s) for i in range(len(indices)-1)   ]
	print(parts)
split_by_index('long story bro',[42])