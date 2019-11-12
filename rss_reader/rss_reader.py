from arg import *
from news import * 
import version

def main():
	if args.version:
		print("Current version: " + version.version)

	if (args.verbose):
		print(80*"_")
		print("\nverbose::Receiving and processing news")
		print(80*"_")

	news = grab_news(args.URL)

	if (args.json):
		if (args.verbose):
			print(80*"_")
			print("\nverbose::Write news to json file")
			print(80*"_")
		write_to_json(news)
	else:
		show_news(news)

if __name__ == '__main__':
	main()