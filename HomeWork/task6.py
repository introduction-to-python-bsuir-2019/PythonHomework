def longest_word(entry) -> str:
	word_list = entry.split() 
	longest_word = ''
	for word in word_list:
		if len(word) > len(longest_word):
			longest_word = word
	print (longest_word)
longest_word("YEs it's pink")
