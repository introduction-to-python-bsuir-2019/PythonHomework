import json
import feedparser
NewsFeed = feedparser.parse("http://feeds.foxnews.com/foxnews/entertainment")
print("\n Feed: FOX NEWS - leatest news and headlines")
print (' Number of RSS posts :', len(NewsFeed.entries),"\n")
jsonObject = []

for entry in NewsFeed.entries:	
	print (entry.title)
	print (entry.published)
	print ("\n",entry.link)
	print(f"  Media url: {entry.media_content[0]['url']}")
	print("_________________")
	jsonEntry = {}
	jsonEntry['title'] = entry.title
	jsonEntry['published'] = entry.published
	jsonEntry['link'] = entry.link
	jsonEntry['media_content'] = entry.media_content
	jsonObject.append(jsonEntry)

print(json.dumps(jsonObject))
