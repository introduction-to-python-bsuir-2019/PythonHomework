import argparse
import html
import json
import feedparser
import requests
from bs4 import BeautifulSoup as bs4
import time
import logging


class NewsReader():
	'CLass for RSS parsing  '
	def __init__(self,url,limit = None	):
		self.title = None
		self.entries = None
		self.url = url
		self.description = None
		self.limit = limit
	

	def parse_rss(self):
		'''Parses RSS feed and returns list of 'News' objects'''

		logging.info('RSS parsing...')
		rss = feedparser.parse(self.url)
		if rss.bozo == 1:
			logging.info('feedparser.bozo is set to 1. It means the feed is not well-formed XML.')
			raise Exception(f'RSS url processing error. Details are "{rss.bozo_exception}"')		
			

		self.entries = []
		logging.info('Working with entry...')
		for entry in rss.entries:
			soup = bs4(entry['description'])
			links = ''
			for link in soup.findAll('a'):
				links +=f"{link.get('href')}\n"
			if links == '':
				links = 'There is no provided links'
			try:
				image = soup.find('a').find('img').get('src')
			except AttributeError:	
				image = 'No image'
			nice_desk = ' '.join(soup.text.split())

			
			self.entries.append({'title':entry.title,
								'feed':rss.feed.title,
								'date':time.strftime('%d-%m-%YT%H:%M:%SZ', entry.published_parsed),
								'simple_date':time.strftime('%d-%m-%Y', entry.published_parsed),
								'link':entry.link,
								'description':nice_desk,
								'image':image,
								'links':links
								})
		return self.entries
	

	def make_json(self):
		'''Create json output '''
		logging.info('Make readable json format...')
		for entry in self.entries[0:self.limit]:
			for key in entry:
				json_one =  json.dumps(key ,indent = 2,ensure_ascii=False)
				print (json_one)

			
	def print_rss(self):
		logging.info('Show rss in readable format...')		
		for entry in self.entries[0:self.limit]:
			print(f"Feed : ({entry['feed']})")
			print(f"Title : {entry['title']}\n")

			try:
				print(f"Date: {entry['date']}\n")
			except IndexError:
				print('Date: Date has not been provided')

			print(f"{entry['link']}\n")
			print(f"Description: {entry['description']}\n")
			print(f"Provided links: {entry['links']}\nProvided image: {entry['image']}")
			#Delimiter
			print('-'*80)


