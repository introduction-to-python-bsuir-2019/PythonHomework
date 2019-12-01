with open('kivi.jpeg','rb') as rf:
	with open('kivi23.jpeg','wb') as wf:
		chunck_size = 2048
		rf_chunk = rf.read(chunck_size)
		while len(rf_chunk) > 0:
			wf.write(rf_chunk)
			rf_chunk = rf.read(chunck_size)
			
