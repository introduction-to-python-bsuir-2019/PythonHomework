import argparse
import feedparser
import html
import json
from bs4 import BeautifulSoup
from SourseReader import NewsReader
PROJECT_VERSION = 'Version 0.5 : '
PROJECT_STATUS = 'FIGHTING WITH SUMMARY'

def Main():
	parser = argparse.ArgumentParser(prog = 'RSS-READER',description=' Provide simple "one shot" RSS Reader')
	parser.add_argument('url', help = "Provide url please", type = str)
	parser.add_argument("--version", help = "Show initial version",action="store_true")
	parser.add_argument("--json", help = "Convert output to json",action="store_true")
	parser.add_argument("--verbose", help = "Outputs verbose status messages",action="store_true")
	parser.add_argument("--limit",default=3,
						 help = "Limit news topics if this parameter provided.Default value is 3",type = int)

	args = parser.parse_args()
	print(args)


	news = NewsReader(args.url,args.limit)
	news.parse_rss()
	if args.version:
		print(PROJECT_VERSION + PROJECT_STATUS, end='\n')
		return
	if args.json:
		print(news.make_json())
	else:
		news.print_rss()


				


	

if __name__ == '__main__':
		Main()