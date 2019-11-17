import argparse
import html
import json
import feedparser
import requests
from bs4 import BeautifulSoup
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
		logging.info('RSS parsing...')
		
		rss = feedparser.parse(self.url)
		if rss.bozo == 1:
			logging.info('feedparser.bozo is set to 1. It means the feed is not well-formed XML.')
			raise Exception(f'RSS url processing error. Details are "{rss.bozo_exception}"')		
			'''Parses RSS feed and returns list of 'News' objects'''
			
		
		self.entries = []
		logging.info('Working with entry...')
		for entry in rss.entries:
			
			self.entries.append({'title':entry.title,
								'feed':rss.feed.title,
								'date':time.strftime('%Y-%m-%dT%H:%M:%SZ', entry.published_parsed),
								'link':entry.link,
								'description':NewsReader.nice_desk(entry.description)
								})
		return self.entries
	
	def nice_desk(description: str) -> str:
		'''Make xml string readable '''
		
		soup = BeautifulSoup(description, 'lxml')
		links = dict()
		for link in soup.findAll('a'):
			links.update({link.text.strip(): link.get('href')})
		try:
			image = soup.find('a').find('img').get('src')
		except AttributeError:
			image = 'no_image'
		result = ' '.join(soup.text.split())
		if image != 'no_image':
			result += f'\n\nImage: {image}'
		if links:
			result += '\n  Links: '
			for link in links:
				result += f'{link} : {links.get(link)}\n'
		return result
	
	def make_json(self):
		'''Create json output '''
		logging.info('Make readable json format...')
		for entry in self.entries[0:self.limit]:
			for x in entry:
				json_one =  json.dumps(x ,indent = 2,ensure_ascii=False)
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
			print(entry['description'])
			#Delimiter
			print("""\
				    --..,_                     _,.--.
				       `'.'.                .'`__ o  `;__.
				          '.'.            .'.'`  '---'`  `
				            '.`'--....--'`.'
				              `'--....--'`
				""")

