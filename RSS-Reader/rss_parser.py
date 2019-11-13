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

from rss_reader_consts import *

import caching_news
import to_fb2_converter
import to_pdf_converter


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


	def _get_feed_title(self) -> str:
		logger = logging.getLogger(self.CLASS_LOGGER_NAME + '._get_feed_title')
		logger.info('Getting title of resource')

		return self._fix_symbols(self.rss.feed.title)


	def _get_feed_subtitle(self) -> str:
		logger = logging.getLogger(self.CLASS_LOGGER_NAME + '._get_feed_subtitle')
		logger.info('Getting subtitle of resource')

		return self._fix_symbols(self.rss.feed.subtitle)


	def _get_feed_image_url(self) -> str:
		logger = logging.getLogger(self.CLASS_LOGGER_NAME + '._get_feed_subtitle')
		logger.info('Getting cover image-url of resource')		

		return self.rss.feed.image.href


	def _get_item_image_url(self, one_news: FeedParserDict) -> str:
		logger = logging.getLogger(self.CLASS_LOGGER_NAME + '._get_item_image_url')
		logger.info('Getting image-url of one news')		

		return one_news.media_content[0]['url']


	def _get_item_title(self, one_news: FeedParserDict) -> str:
		logger = logging.getLogger(self.CLASS_LOGGER_NAME + '._get_item_title')
		logger.info('Getting title of one news')

		return self._fix_symbols(one_news.title)


	def _get_item_date(self, one_news: FeedParserDict) -> str:
		logger = logging.getLogger(self.CLASS_LOGGER_NAME + '._get_item_date')
		logger.info('Getting publishing date of one news')

		return self._fix_symbols(one_news.published)


	def _get_item_link(self, one_news: FeedParserDict) -> str:
		logger = logging.getLogger(self.CLASS_LOGGER_NAME + '._get_item_link')
		logger.info('Getting link of one news')

		return self._fix_symbols(one_news.link)


	def _parse_item(self, elem: str) -> str:
		logger = logging.getLogger(self.CLASS_LOGGER_NAME + '._parse_item')
		logger.info('Extract short content of one news on html-format')

		soup = BeautifulSoup(elem, "html.parser")
		return soup.get_text()


	def _get_item_content(self, one_news: FeedParserDict) -> str:
		logger = logging.getLogger(self.CLASS_LOGGER_NAME + '._get_item_content')
		logger.info('Getting short content of one news')

		return self._fix_symbols(self._parse_item(one_news.summary_detail.value))


	def _get_rss(self) -> None:
		logger = logging.getLogger(self.CLASS_LOGGER_NAME + '._get_rss')
		logger.info('Parse page with rss-format')

		self.rss = parse(self.link)


	def _fix_symbols(self, item: str) -> str:
		return item.replace('&#39;', "'")


	def _get_news_as_list(self, limit: int=0) -> list:
		logger = logging.getLogger(self.CLASS_LOGGER_NAME + '._get_news_as_list')
		logger.info(f'Getting news as list of dicts')
		
		self._get_rss()

		if limit == 0:
			limit = len(self.rss.entries)

		news = list()

		for one_news in self.rss.entries:
			piece_of_news = dict()

			# print(one_news.media_content[0]['url']) !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! GETTING IMAGE !!!!!!!!!!!!!!!!!!!!!!!!!!!!

			piece_of_news[KEYWORD_TITLE] = self._get_item_title(one_news)
			piece_of_news[KEYWORD_DATE] = self._get_item_date(one_news)
			piece_of_news[KEYWORD_LINK] = self._get_item_link(one_news)
			piece_of_news[KEYWORD_IMG_LINK] = self._get_item_image_url(one_news)
			piece_of_news[KEYWORD_CONTENT] = self._get_item_content(one_news)
	
			if limit > 0:
				news.append(piece_of_news.copy())

			caching_news.db_write(self._convert_date_to_YYYYMMDD(piece_of_news[KEYWORD_DATE]),
 						piece_of_news[KEYWORD_TITLE],
 						piece_of_news[KEYWORD_LINK],
 						piece_of_news[KEYWORD_CONTENT]
 						)

			piece_of_news.clear()

			limit -= 1

		return news


	def get_news_as_string(self, limit: int=0) -> str:
		logger = logging.getLogger(self.CLASS_LOGGER_NAME + '.get_news_as_string')
		logger.info(f'Getting news with string-format with limit: {limit}')

		news_list = self._get_news_as_list(limit)

		feed = self._get_feed_title()
		
		news = ''
		for one_news in news_list:	
			news += EN + NEWS_SEPARATOR + DEN

			for key_word in one_news:
				if key_word == KEYWORD_CONTENT:
					news += EN
				news += key_word + one_news[key_word] + EN

		return feed + DEN + news


	def _convert_date_to_YYYYMMDD(self, date : str) -> str:
		logger = logging.getLogger(self.CLASS_LOGGER_NAME + '.convert_date_to_YYYYMMDD')
		logger.info('Converting date to YYYYMMDD format')

		return (''.join(date.split()[3:0:-1])).replace(date.split()[2], MONTHS[date.split()[2]])


	def get_news_as_json(self, limit: int=0) -> str:
		logger = logging.getLogger(self.CLASS_LOGGER_NAME + '._get_news_as_json')
		logger.info(f'Getting news with json-format \
					with limit: {limit}')		

		self._get_rss()
		return json.dumps(self.rss, indent=4)


	def get_news_as_fb2(self, filepath: str, limit: int=0) -> None:
		logger = logging.getLogger(self.CLASS_LOGGER_NAME + '.get_news_as_fb2')
		logger.info('Converting news to .fb2 format')		
		
		news_list = self._get_news_as_list(limit)

		fb2 = to_fb2_converter.FB2()

		fb2.add_description_of_resource(self._get_feed_title(),
										self._get_feed_subtitle(),
										self._get_feed_image_url()
										)

		for piece_of_news in news_list:
			fb2.add_section(
			title_info=piece_of_news[KEYWORD_TITLE],
			date=piece_of_news[KEYWORD_DATE],
			content=piece_of_news[KEYWORD_CONTENT],
			link=piece_of_news[KEYWORD_LINK],
			img_link=piece_of_news[KEYWORD_IMG_LINK]
			)

		fb2.write_to_file(filepath)


	def get_news_as_pdf(self, filepath: str, limit: int=0) -> None:
		
		news_list = self._get_news_as_list(limit)

		pdf = to_pdf_converter.PDF()
		pdf.set_meta_info(self._get_feed_title(), self._get_feed_image_url())

		for piece_of_news in news_list:
			pdf.add_piece_of_news(	title=piece_of_news[KEYWORD_TITLE].encode('latin-1', 'replace').decode('latin-1'),
									date=piece_of_news[KEYWORD_DATE].encode('latin-1', 'replace').decode('latin-1'),
									link=piece_of_news[KEYWORD_LINK].encode('latin-1', 'replace').decode('latin-1'),
									img_url=piece_of_news[KEYWORD_IMG_LINK].encode('latin-1', 'replace').decode('latin-1'),
									content=piece_of_news[KEYWORD_CONTENT].encode('latin-1', 'replace').decode('latin-1')
								)

		pdf.write_to_file(filepath)

