'''
This module provides human-readability format of rss-sources.

Inside are used modules:
	- feedparser
	- bs4 (BeautifulSoup)
'''

from feedparser import parse, FeedParserDict
from bs4 import BeautifulSoup
import logging

import json

NEWS_SEPARATOR = '=========================================================='

EN = '\n' # enter
DEN = '\n\n' # double enter

ROOT_LOGGER_NAME = 'RssReader'
MODULE_LOGGER_NAME = ROOT_LOGGER_NAME + '.rss_reader'


class RssReader:
	'''This class uses interface of feedparser, which interact with RSS-sources.
	'''

	CLASS_LOGGER_NAME = MODULE_LOGGER_NAME + '.RssReader'

	def __init__(self, link: str):
		logger = logging.getLogger(self.CLASS_LOGGER_NAME + '.__init__')
		logger.info(f'Creating object of RssReader class with link: {link}')

		self.link = link


	def _get_feed(self) -> str:
		logger = logging.getLogger(self.CLASS_LOGGER_NAME + '._get_feed')
		logger.info('Getting title of resource')

		return 'Feed: ' + self.rss.feed.title


	def _get_title(self, one_news: FeedParserDict) -> str:
		logger = logging.getLogger(self.CLASS_LOGGER_NAME + '._get_title')
		logger.info('Getting title of one news')

		return 'Title: ' + one_news.title


	def _get_date(self, one_news: FeedParserDict) -> str:
		logger = logging.getLogger(self.CLASS_LOGGER_NAME + '._get_date')
		logger.info('Getting publishing date of one news')

		return 'Date: ' + one_news.published


	def _get_link(self, one_news: FeedParserDict) -> str:
		logger = logging.getLogger(self.CLASS_LOGGER_NAME + '._get_link')
		logger.info('Getting link on one news')

		return 'Link: ' + one_news.link


	def _get_content(self, one_news: FeedParserDict) -> str:
		logger = logging.getLogger(self.CLASS_LOGGER_NAME + '._get_content')
		logger.info('Getting short content of one news')

		return self._parse_elem(one_news.summary_detail.value)


	def _get_rss(self) -> None:
		logger = logging.getLogger(self.CLASS_LOGGER_NAME + '._get_rss')
		logger.info('Parse page with rss-format')

		self.rss = parse(self.link)


	def get_news_as_string(self, limit: int=0) -> str:
		logger = logging.getLogger(self.CLASS_LOGGER_NAME + '.get_news_as_string')
		logger.info(f'Getting news with string-format with limit: {limit}')

		self._get_rss()

		feed = self._get_feed()
		
		news = ''
		for one_news in self.rss.entries:
			title = self._get_title(one_news)
			date = self._get_date(one_news)
			link = self._get_link(one_news)
			content = self._get_content(one_news)

			news += title + EN + date + EN + link + DEN + content + DEN
			news += NEWS_SEPARATOR + DEN

			limit -= 1
			if limit == 0:
				break

		return feed + DEN + news


	def get_news_as_json(self, limit: int=0) -> str:
		logger = logging.getLogger(self.CLASS_LOGGER_NAME + '._get_news_as_json')
		logger.info(f'Getting news with json-format \
					with limit: {limit}')		

		self._get_rss()
		return json.dumps(self.rss, indent=4)


	def _parse_elem(self, elem: str) -> str:
		logger = logging.getLogger(self.CLASS_LOGGER_NAME + '._parse_elem')
		logger.info('Extract short content of one news on html-format')

		soup = BeautifulSoup(elem, "html.parser")
		return soup.get_text()


	def temp_debug_func(self):
		pass
