import feedparser
import re
import html
import json
from arg import *

class News():
	def __init__(self, feed, link, title, date, text):
		self.feed = feed
		self.link = link
		self.title = title
		self.date = date
		self.text = text

	def show_feed(self):
		print('Feed: ', self.feed, end = "\n\n")

	def show_link(self):
		print("Link: ", self.link, end = "\n\n")

	def show_title(self):
		print("Title: ", self.title, end = "\n\n")

	def show_text(self):
		if self.text != "":
			print("Description: ", self.text, end = "\n\n")
		else:
			print("Description: No description", end = "\n\n")

	def show_date(self):
		print("Date: ", self.date, end = "\n\n")

	def show(self):
		self.show_feed()
		self.show_link()
		self.show_title()
		self.show_date()
		self.show_text()

def write_to_json(news):
    prepared_news = []
    for i in range(len(news)):
        newsdict = {
            "feed": news[i].feed,
            "link": news[i].link,
            "title": news[i].title,
            "date": news[i].date[5:len(news[i].date)-15],
            "description": news[i].text,
        }
        if args.limit and args.limit > i:
        	prepared_news.append(newsdict)
        if not args.limit:
        	prepared_news.append(newsdict)
    with open("data.json", "w") as output:
    	json.dump(prepared_news, output, indent = 3, ensure_ascii = False)
    	print(80*"_")
    	print("\nSuccessfully recorded")
    	print(80*"_")

def get_Text(str):
	start_point = str.find("</a>")
	end_point = str.rfind("<p>")
	str = str[start_point + 4 : end_point]
	return str

def clean_text(text):
  cleanr = re.compile("<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});")
  cleantext = re.sub(cleanr, '', text)
  return cleantext

def grab_news(URL):
	if (args.verbose):
		print(80*"_")
		print("\nverbose::Assemble news from URL")
		print(80*"_")
	data = feedparser.parse(URL)
	if (args.verbose):
		print(80*"_")
		print("\nverbose::Processing news from URL")
		print(80*"_")
	news = [News(data.feed.title, i.link, html.unescape(i.title), i.published,
	 clean_text(i.description)) for i in data.entries]
	return news

def show_news(news):
	for i in range(len(news)):
		if not args.limit:
			news[i].show()
			print(80*"_", end = "\n\n")
		if args.limit and args.limit > i:
			news[i].show()
			print(80*"_", end = "\n\n")
		