import feedparser
NewsFeed = feedparser.parse("https://auto.onliner.by/feed")
entry1 = NewsFeed.entries[0]
print(entry1.items)
print ('Number of RSS posts :', len(NewsFeed.entries))

for entry in NewsFeed.entries:

	print (entry.title)
	print (entry.published)
