import sys
import requests
from bs4 import BeautifulSoup

# here should be argparse

def parse_description(description):
	soup = BeautifulSoup(description, "html.parser")

	for anchor in soup.find_all('a'):
		if anchor.img:
			image_link = anchor.img['src']     			# get img url 

	for anchor in soup.find_all('a', href=True):
   		link =  anchor['href']   							#get href urls

	context = description[description.rfind("</a>"):]
	context = context[:context.find("<p>")].replace("</a>", "")
   	
	return [image_link, link, context]

def parse_new(all_news):
	all_news_list = []
	for current_new in all_news:
		title = current_new.find('title').text
		date = current_new.find('pubdate').text
		description = parse_description(current_new.find('description').text)
		all_news_list.append([title, date, description])

	return all_news_list



url = 'https://news.yahoo.com/rss/'
r = requests.get(url).text
soup = BeautifulSoup(r, 'html.parser')

all_news = soup.find_all('item')  
feed = soup.find('title').text
all_news_list = parse_new(all_news)

print("FEED:", feed)
for new in all_news_list:
		print("Title:", new[0])
		print("Date", new[1])
		print("Description:", new[2][2])
		print("Links:")
		print(new[2][1], " (link)")
		print(new[2][0], "(image)")