from rss_parser import RssParser

myparser = RssParser('https://news.yahoo.com/rss/', 1)
print(myparser.parse_rss())
