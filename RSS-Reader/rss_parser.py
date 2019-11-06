'''
This module provides human-readability format of rss-sources.

Inside are used modules:
	- feedparser
	- bs4 (BeautifulSoup)
'''

import feedparser
from bs4 import BeautifulSoup

import json

NEWS_SEPARATOR = '=========================================================='

EN = '\n' # enter
DEN = '\n\n' # double enter


class RssReader:
	'''This class uses interface of feedparser, which interact with RSS-sources.
	'''

	def __init__(self, link):
		self.link = link


	def _get_feed(self):
		return 'Feed: ' + self.rss.feed.title


	def _get_title(self, new):
		return 'Title: ' + new.title


	def _get_date(self, new):
		return 'Date: ' + new.published


	def _get_link(self, new):
		return 'Link: ' + new.link


	def _get_content(self, new):
		return self._parse_elem(new.summary_detail.value)


	def set_link(self, link):
		self.link = link


	def _get_rss(self):
		self.rss = feedparser.parse(self.link)


	def get_news_as_string(self, limit=0):
		self._get_rss()

		feed = self._get_feed()
		
		news = ''
		for new in self.rss.entries:
			title = self._get_title(new)
			date = self._get_date(new)
			link = self._get_link(new)
			content = self._get_content(new)

			news += title + EN + date + EN + link + DEN + content + DEN
			news += NEWS_SEPARATOR + DEN

			limit -= 1
			if limit == 0:
				break

		return feed + DEN + news


	def get_news_as_json(self, limit=0):
		self._get_rss()
		return json.dumps(self.rss, indent=4)


	def _parse_elem(self, elem):
		soup = BeautifulSoup(elem, "html.parser")
		return soup.get_text()


	def temp_debug_func(self):
		pass
