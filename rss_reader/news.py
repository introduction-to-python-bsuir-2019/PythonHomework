import feedparser
import logging
import re
import html
import json
from rss_reader import arg
from bs4 import BeautifulSoup

class News():
	def __init__(self, feed, link, title, date, text, images):
		self.feed = feed
		self.link = link
		self.title = title
		self.date = date
		self.text = text
		self.url_images = images

	def show_feed(self):
		print('Feed: ', self.feed, end = "\n\n")

	def show_link(self):
		print("Link: ", self.link, end = "\n\n")

	def show_title(self):
		print("Title: ", self.title, end = "\n\n")

	def show_text(self):
		if self.text != "" and self.text != " ":
			print("Description: ", self.text, end = "\n\n")
		else:
			print("Description: No description", end = "\n\n")

	def show_date(self):
		print("Date: ", self.date, end = "\n\n")

	def show_images(self):
		if self.url_images != [''] and self.url_images != None and self.url_images != []:
			print("URL Images: ")
			for i in range(len(self.url_images)):
				print("[%d]: %s" %(i + 1, self.url_images[i]))
		else:
			print("URL Images: No Images")			

	def show(self):
		self.show_feed()
		self.show_link()
		self.show_title()
		self.show_date()
		self.show_text()
		self.show_images()

def write_to_json(news):
    prepared_news = []

    for i in range(len(news)):
        logging.info("Processing news")
        newsdict = {
        "feed": news[i].feed,
        "link": news[i].link,
        "title": news[i].title,
        "date": news[i].date[5:len(news[i].date)-15],
        "description": news[i].text,
        "url_images":news[i].url_images
        }
        if arg.args.limit and arg.args.limit > i:
        	prepared_news.append(newsdict)
        if not arg.args.limit:
        	prepared_news.append(newsdict)

    with open("data.json", "w") as output:
    	logging.info("Dump news to news.json in your working directory")
    	json.dump(prepared_news, output, indent = 3, ensure_ascii = False)
    	print(80*"_")
    	print("\nSuccessfully recorded")
    	print(80*"_")

def find_url_images(entries):
	bs = html.unescape(BeautifulSoup(entries.summary, "html.parser"))
	images = []

	logging.info("Searching url links in news")

	for img in bs.findAll("img"):
		if "src" in img.attrs:
			src = img["src"]
			images.append(src)
			bs.find("img").replace_with("image")

	for img in bs.findAll("a"):
		if "href" in bs.attrs:
			src = img["href"]
			images.append(src)

	for img in bs.findAll("iframe"):
		if "src" in img.attrs:
			src = img["src"]
			images.append(src)

	return images

def get_Text(str):
	logging.info("Processing description text in news")
	start_point = str.find("</a>")
	end_point = str.rfind("<p>")
	str = str[start_point + 4 : end_point]
	return str

def clean_text(text):
  cleanr = re.compile("<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});")
  cleantext = re.sub(cleanr, '', text)
  return cleantext

def grab_news(URL):
	logging.info("Assemble news from URL")
	data = feedparser.parse(URL)

	logging.info("Processing news from URL")
	news = [News(data.feed.title, i.link, html.unescape(i.title), i.published,
	 clean_text(i.description), find_url_images(i)) for i in data.entries]

	return news

def show_news(news):
	for i in range(len(news)):
		if not arg.args.limit:
			news[i].show()
			print(80*"_", end = "\n\n")
		if arg.args.limit and arg.args.limit > i:
			news[i].show()
			print(80*"_", end = "\n\n")
		
