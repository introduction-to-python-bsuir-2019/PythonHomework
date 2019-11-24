from rss_reader import arg
from rss_reader import news 
from rss_reader import version
import logging

def main():
	if arg.args.version:
		print("Current version: " + version.version)

	if (arg.args.verbose):
		logging.basicConfig(format = u' %(levelname)-8s [%(asctime)s] %(message)s', level = logging.INFO)

	captured_news = news.grab_news(arg.args.URL)

	if (arg.args.json):
		logging.info("Write news to json file")
		news.write_to_json(captured_news)
		news.caching_news(captured_news)
	else:
		logging.info("Print news to outstream")
		if arg.args.date:
			news.find_news_in_cache()
		else:
			news.caching_news(captured_news)
			news.show_news(captured_news)
	logging.info("The program is successfully completed")

if __name__ == '__main__':
	main()
