from rss_parser import RssParser
import json

myparser = RssParser('https://news.yahoo.com/rss/', 1)
myparser.parse_rss()
print(json.dumps(myparser.feed_to_json(), indent=2))
