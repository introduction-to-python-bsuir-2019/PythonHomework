"""
This module provides human-readability format of rss-sources.

Inside are used modules:
    - feedparser
    - bs4 (BeautifulSoup)
"""

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
    """This class uses interface of feedparser, which interact with RSS-sources."""

    CLASS_LOGGER_NAME = MODULE_LOGGER_NAME + '.RssReader'

    def __init__(self, link: str):
        """Initializate of RssReader.

        Required: link - url-link on rss-resource.
        """
        logger = logging.getLogger(self.CLASS_LOGGER_NAME + '.__init__')
        logger.info(f'Creating object of RssReader class with link: {link}')

        self._link = link

    def set_link(self, link: str) -> None:
        """Set link on rss-resource."""
        logger = logging.getLogger(self.CLASS_LOGGER_NAME + '.set_link')
        logger.info(f'Setting link: {link} of rss-resource')

        self._link = link

    def _get_feed_title(self) -> str:
        """Get title of rss-resource."""
        logger = logging.getLogger(self.CLASS_LOGGER_NAME + '._get_feed_title')
        logger.info('Getting title of resource')

        return self._fix_symbols(self._rss.feed.title)

    def _get_feed_subtitle(self) -> str:
        """Get subtittle of rss-resource."""
        logger = logging.getLogger(self.CLASS_LOGGER_NAME + '._get_feed_subtitle')
        logger.info('Getting subtitle of resource')

        return self._fix_symbols(self._rss.feed.subtitle)

    def _get_feed_image_url(self) -> str:
        """Get image's url of rss-resource."""
        logger = logging.getLogger(self.CLASS_LOGGER_NAME + '._get_feed_subtitle')
        logger.info('Getting cover image-url of resource')

        try:
            url = self._rss.feed.image.href
        except AttributeError:
            url = ''
        return url

    def _get_item_images_urls(self, one_news: FeedParserDict) -> list():
        """Get images's urls of piece of news."""
        logger = logging.getLogger(self.CLASS_LOGGER_NAME + '._get_item_image_url')
        logger.info('Getting image-url of one news')

        img_link = ''
        imgs_links = []
        try:
            for piece_of_media in one_news.media_content:
                if piece_of_media['type'] == 'image/jpeg' or piece_of_media == 'image/png':
                    imgs_links.append(piece_of_media['url'])
        except AttributeError:
            return []
        return imgs_links

    def _get_item_title(self, one_news: FeedParserDict) -> str:
        """Get title of piece of news."""
        logger = logging.getLogger(self.CLASS_LOGGER_NAME + '._get_item_title')
        logger.info('Getting title of one news')

        return self._fix_symbols(one_news.title)

    def _get_item_date(self, one_news: FeedParserDict) -> str:
        """Get date of publication of piece of news."""
        logger = logging.getLogger(self.CLASS_LOGGER_NAME + '._get_item_date')
        logger.info('Getting publishing date of one news')

        return self._fix_symbols(one_news.published)

    def _get_item_link(self, one_news: FeedParserDict) -> str:
        """Get link on piece of news."""
        logger = logging.getLogger(self.CLASS_LOGGER_NAME + '._get_item_link')
        logger.info('Getting link of one news')

        return self._fix_symbols(one_news.link)

    def _parse_item(self, elem: str) -> str:
        """Parse html to getting content."""
        logger = logging.getLogger(self.CLASS_LOGGER_NAME + '._parse_item')
        logger.info('Extract short content of one news on html-format')

        soup = BeautifulSoup(elem, "html.parser")
        return soup.get_text()

    def _get_item_content(self, one_news: FeedParserDict) -> str:
        """Get short content of piece of news."""
        logger = logging.getLogger(self.CLASS_LOGGER_NAME + '._get_item_content')
        logger.info('Getting short content of one news')

        return self._fix_symbols(self._parse_item(one_news.summary_detail.value))

    def _get_rss(self) -> None:
        """Get rss object of feedparser."""
        logger = logging.getLogger(self.CLASS_LOGGER_NAME + '._get_rss')
        logger.info('Parse page with rss-format')

        self._rss = parse(self._link)

    def _fix_symbols(self, item: str) -> str:
        """Replace symbols from xml to ascii."""
        return item.replace('&#39;', "'")

    def _get_news_as_list(self, limit: int=0) -> list:
        """Get list of news.

        List contains dictionaries with key:KEYWORD, value:item.
        """
        logger = logging.getLogger(self.CLASS_LOGGER_NAME + '._get_news_as_list')
        logger.info(f'Getting news as list of dicts')

        self._get_rss()

        if limit <= 0:
            limit = len(self._rss.entries)

        news = list()

        for one_news in self._rss.entries:
            piece_of_news = dict()

            piece_of_news[KEYWORD_TITLE] = self._get_item_title(one_news)
            piece_of_news[KEYWORD_DATE] = self._get_item_date(one_news)
            piece_of_news[KEYWORD_LINK] = self._get_item_link(one_news)
            piece_of_news[KEYWORD_IMGS_LINKS] = self._get_item_images_urls(one_news)
            piece_of_news[KEYWORD_CONTENT] = self._get_item_content(one_news)

            if limit > 0:
                news.append(piece_of_news.copy())

            caching_news.db_write(
                                  piece_of_news[KEYWORD_DATE],
                                  piece_of_news[KEYWORD_TITLE],
                                  piece_of_news[KEYWORD_LINK],
                                  piece_of_news[KEYWORD_CONTENT])

            piece_of_news.clear()

            limit -= 1

        return news

    def get_news_as_string(self, limit: int=0) -> str:
        """Get news as string.

        Takes a limit:int - limit of news, which will be returned.
        """
        logger = logging.getLogger(self.CLASS_LOGGER_NAME + '.get_news_as_string')
        logger.info(f'Getting news with string-format with limit: {limit}')

        news_list = self._get_news_as_list(limit)

        feed = self._get_feed_title()

        news = ''
        for one_news in news_list:
            news += EN + NEWS_SEPARATOR + DEN

            for key, value in one_news.items():
                if key == KEYWORD_IMGS_LINKS:
                    if value:  # img_links list is not empty
                        news += key + ' '
                        for img_link in value:
                            news += img_link + EN
                else:
                    if key == KEYWORD_CONTENT:
                        news += EN
                    news += key + value + EN

        return feed + DEN + news

    def get_news_as_json(self, limit: int=0, filepath: str='') -> str:
        """Get news as json-string.

        Takes a limit:int - limit of news, which will be returned.
        """
        logger = logging.getLogger(self.CLASS_LOGGER_NAME + '._get_news_as_json')
        logger.info(f'Getting news with json-format \
                    with limit: {limit}')

        news_list = self._get_news_as_list(limit)

        news = dict()
        news[KEYWORD_FEED] = self._get_feed_title()
        news['news'] = news_list

        if filepath == '':
            return json.dumps(news, indent=4, ensure_ascii=False).encode('utf8').decode()
        else:
            with open(filepath, 'w') as file:
                file.write(json.dumps(news, indent=4, ensure_ascii=False).encode('utf8').decode())

    def get_news_as_fb2(self, filepath: str, limit: int=0) -> None:
        """Get news as fb2.

        Takes arguments:
        limit:int - limit of news, which will be returned;
        filepath:str - path where news will be saved.
        """
        logger = logging.getLogger(self.CLASS_LOGGER_NAME + '.get_news_as_fb2')
        logger.info('Converting news to .fb2 format')

        news_list = self._get_news_as_list(limit)

        fb2 = to_fb2_converter.FB2()

        fb2.add_description_of_resource(self._get_feed_title(),
                                        self._get_feed_subtitle(),
                                        self._get_feed_image_url())

        for piece_of_news in news_list:
            fb2.add_section(title_info=piece_of_news[KEYWORD_TITLE],
                            date=piece_of_news[KEYWORD_DATE],
                            content=piece_of_news[KEYWORD_CONTENT],
                            link=piece_of_news[KEYWORD_LINK],
                            imgs_links=piece_of_news[KEYWORD_IMGS_LINKS])

        fb2.write_to_file(filepath)

    def get_news_as_pdf(self, filepath: str, limit: int=0) -> None:
        """Get news as pdf.

        Takes arhuments:
        limit:int - limit of news, which will be returned;
        filepath:str - path where news will be saved.
        """
        logger = logging.getLogger(self.CLASS_LOGGER_NAME + '.get_news_as_pdf')
        logger.info('Converting news to .pdf format')

        news_list = self._get_news_as_list(limit)

        pdf = to_pdf_converter.PDF()
        pdf.add_font('FreeSans', '', 'FreeSans.ttf', uni=True)

        title = self._get_feed_title()
        pdf.set_meta_info('', self._get_feed_image_url())

        for piece_of_news in news_list:
            pdf.add_piece_of_news(title=piece_of_news[KEYWORD_TITLE],
                                  date=piece_of_news[KEYWORD_DATE],
                                  link=piece_of_news[KEYWORD_LINK],
                                  imgs_urls=piece_of_news[KEYWORD_IMGS_LINKS],
                                  content=piece_of_news[KEYWORD_CONTENT])

        pdf.write_to_file(filepath)
