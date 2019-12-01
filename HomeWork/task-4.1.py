with open('unsorted_names.txt','r') as rf:
	with open('sorted_names.txt','w') as wf:
		for line in sorted(rf):
			wf.write(line)

