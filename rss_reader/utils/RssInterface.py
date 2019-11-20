from abc import ABCMeta, abstractmethod
import bs4
import json
from typing import Union, Dict, List

import logging
import feedparser
from terminaltables import SingleTable
from textwrap import wrap

from ..utils.DataStructures import NewsItem, News


class RssException(Exception):
    """
    Custom Exception class raised by RssBots classes
    """
    pass


class RssBotInterface(metaclass=ABCMeta):
    """
    Interface for Rss reader classes. Mandatory methods are: get_news(), get_json()
    and internal parser's methods for particular cases of each bot
    """

    def __init__(self, url: str, limit: int, width: int, logger: logging.Logger):
        self.limit = limit
        self.logger = logger
        self.url = url
        self.screen_width = width
        feed = self._parse_raw_rss()
        # self.news = self._get_news_as_dict(feed)  # news as dict
        self.news = self._feed_to_news(feed)
        self.logger.info(f'Bot initialization is completed')
        self.human_text = ''

    @abstractmethod
    def get_news(self) -> str:
        """
        Returns str containing formatted news from internal attr self.feed

        :return: str with news
        """

    @abstractmethod
    def _feed_to_news(self, feed: feedparser.FeedParserDict) -> News:
        """
        Converts FeedParserDict obj to News obj

        :return: News
        """

    def get_json(self) -> str:
        """
        Return json formatted news

        :return: json formatted string
        """
        self.logger.info(f'Returning news in JSON format')
        return json.dumps(self.news, indent=4)

    @abstractmethod
    def _parse_raw_rss(self) -> feedparser.FeedParserDict:
        """
        Parsing news by url

        Result stores into internal attribute self.feed
        :return: None
        """

    @abstractmethod
    def _parse_news_item(self, news_item: NewsItem):
        pass


class BaseRssBot(RssBotInterface):
    """
    Base class for rss reader bots. Implements base interface
    """

    def _parse_raw_rss(self) -> feedparser.FeedParserDict:
        """
        Parsing news by url

        Result stores into internal attribute self.feed
        :return: FeedParserDict object with news
        """

        self.logger.info(f'Lets to grab news from {self.url}')

        feed = feedparser.parse(self.url)

        self.logger.debug(f'Got feedparser object')

        if feed.get('bozo_exception'):
            #
            exception = feed.get('bozo_exception')
            self.logger.warning(f'Having an exception while parsing xml: {exception}')

            exception_sting = f'\tError while parsing xml: \n {exception}\n\tBad rss feed. Check your url\n\n' \
                              f'\tTry to use one of this as example:\n' \
                              f'\ttut_by_rss = "https://news.tut.by/rss/index.rss"\n' \
                              f'\tgoogle_rss = "https://news.google.com/news/rss"\n' \
                              f'\tyahoo = "https://news.yahoo.com/rss/"'
            raise RssException(exception_sting)

        self.logger.info(f'well formed xml = {feed.get("bozo")}\n'
                         f'url= {feed.get("url")}\n'
                         f'title= {feed.get("channel")["title"]}\n'
                         f'description= {feed.get("channel")["description"]}\n'
                         f'link to recent changes= {feed.get("channel")["link"]}\n'
                         )
        return feed

    def get_news(self) -> str:
        """
        Returns str containing formatted news from internal attr self.feed

        :return: str with news
        """
        table = [['Feed', f"Title: {self.news.feed}\nLink: {self.news.link}"]]
        news_items = self.news.items
        for n, item in enumerate(news_items):
            # table.append([1, item.get('human_text')])
            initial_news_item = self._parse_news_item(item)
            splitted_by_paragraphs = initial_news_item.split('\n')
            for i, line in enumerate(splitted_by_paragraphs):
                if len(line) > self.screen_width:
                    wrapped = wrap(line, self.screen_width)
                    del splitted_by_paragraphs[i]
                    for wrapped_line in wrapped:
                        splitted_by_paragraphs.insert(i, wrapped_line)
                        i += 1

            table.append([str(n + 1), '\n'.join(splitted_by_paragraphs)])

        table_inst = SingleTable(table)
        table_inst.inner_heading_row_border = False
        table_inst.inner_row_border = True

        self.logger.info(f'Print formatted news')

        return table_inst.table

    def _feed_to_news(self, feed: feedparser.FeedParserDict) -> News:
        """
        Returns str containing formatted news from internal attr self.feed

        :return: str with news
        """
        news_items = []

        for i, item in enumerate(feed.get('items', '')[:self.limit]):
            news_items.append(NewsItem(
                title=item.get('title', ''),
                link=item.get('link', ''),
                published=item.get('published', ''),
                imgs=[img.get('url', '') for img in item.get('media_content', '')],
                links=[link.get('href') for link in item.get('links', '')],
                html=item.get('summary', ''),
            ))

        news = News(
            feed=feed.get('feed', '').get('title', ''),
            link=feed.get('feed', '').get('link', ''),
            items=news_items,
        )
        self.logger.info(f'_get_news(): Feedparser object is converted into news_item obj with Default news')

        return news

    def _parse_news_item(self, news_item: NewsItem) -> str:
        """
        Forms a human readable string from news_item and adds it to the news_item dict
        :param news_item: news_item content
        :return: extend news_item dict with human readable news content
        """
        self.logger.info(f'Extending {news_item.title}')
        out_str = ''
        out_str += f"\nTitle: {news_item.title}\n" \
                   f"Date: {news_item.published}\n" \
                   f"Link: {news_item.link}\n"

        html = bs4.BeautifulSoup(news_item.html, "html.parser")

        links = news_item.links
        imgs = news_item.imgs

        for tag in html.descendants:
            if tag.name == 'a':
                link = tag.attrs.get('href', '')
                if link not in links:
                    links.append(link)
                    self.logger.warning(f'Link {link} isn\'t found')
            elif tag.name == 'img':
                src = tag.attrs.get('src', '')
                if src in imgs:
                    img_idx = imgs.index(src) + len(links) + 1
                else:
                    imgs.append(src)
                    img_idx = len(imgs) + len(links)
                out_str += f'\n[image {img_idx}:  {tag.attrs.get("title")}][{img_idx}]'

        out_str += f'{html.getText()}\n'
        out_str += 'Links:\n'
        out_str += '\n'.join([f'[{i + 1}]: {link} (link)' for i, link in enumerate(links)]) + '\n'
        out_str += '\n'.join([f'[{i + len(links) + 1}]: {link} (image)' for i, link in enumerate(imgs)]) + '\n'

        return out_str
