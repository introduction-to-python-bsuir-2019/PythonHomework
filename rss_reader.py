import argparse
import feedparser
import html
import json
from bs4 import BeautifulSoup
from PythonHomework.SourseReader import NewsReader
import logging
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

	news = NewsReader(args.url,args.limit)
	
	if args.verbose:
		logging.basicConfig(level=logging.INFO, format='%(relativeCreated)6d %(threadName)s %(message)s')

	if args.version:
		print(PROJECT_VERSION + PROJECT_STATUS, end='\n')
		return

	if args.json:
		news.parse_rss()
		news.make_json()
		print('-'*80)

	else:
		news.parse_rss()
		news.print_rss()
				


	

if __name__ == '__main__':
		Main()