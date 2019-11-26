import argparse

def get_args():
	parser = argparse.ArgumentParser(description = "simple rss-reader")
	parser.add_argument("URL", type = str, help = "URL to rss sourse")
	parser.add_argument("-l", "--limit", type = int, help = "set quantity of news")
	parser.add_argument("-v","--version", action = "store_true")
	parser.add_argument("--json", action = "store_true")
	parser.add_argument("--verbose", action = "store_true")
	parser.add_argument("-d", "--date", type = str, help = "set date in YMD format for searching in cashed news")
	args = parser.parse_args()
	return args

args = get_args()
