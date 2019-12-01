
def most_common_words(filepath,number_of_words=3):
	import string 
	from collections import Counter
	with open (filepath,'r') as rf:
		rf_content = rf.read()
	#Delete punctuation a
	for c in string.punctuation:
		rf_content = rf_content.replace(c,'')# Why I cant put split here 
	# WORKING WITH COUNTER POWER and delete spaces
	count = Counter(rf_content.split()).most_common(number_of_words)
	first = [i[0] for i in count]
	return first
	

print(most_common_words('lorem_ipsum.txt',8))