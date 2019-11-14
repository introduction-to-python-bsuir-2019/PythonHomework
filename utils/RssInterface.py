from abc import ABCMeta, abstractmethod, abstractproperty
from typing import Union, Dict, List, Iterable, Optional, Any
import json
import feedparser
import logging
import bs4
from textwrap import wrap
from terminaltables import SingleTable


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
        self.news = self._get_news_as_dict(feed)  # news as dict
        self.logger.info(f'Bot initialization is completed')

    @abstractmethod
    def get_news(self) -> str:
        """
        Returns str containing formatted news from internal attr self.feed

        :return: str with news
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
    def _get_news_as_dict(self, feed: feedparser.FeedParserDict) -> Dict[str, Union[str, List[str]]]:
        """
        Returns str containing formatted news from internal attr self.feed

        :return: str with news
        """

    @abstractmethod
    def _parse_news_item(self, news_item: Dict[str, Union[str, List[str]]]):
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

        self.logger.info(f'Got feedparser object')

        if feed.get('bozo_exception'):
            #
            exception = feed.get('bozo_exception')
            raise RssException(f'Error while parsing xml: \n {exception}')
            self.logger.error(f'Bad rss feed. Check your url')

        self.logger.info(f'well formed xml = {feed["bozo"]}\n'
                         f'url= {feed["url"]}\n'
                         f'title= {feed["channel"]["title"]}\n'
                         f'description= {feed["channel"]["description"]}\n'
                         f'link to recent changes= {feed["channel"]["link"]}\n'
                         )
        return feed

    def get_news(self) -> str:
        """
        Returns str containing formatted news from internal attr self.feed

        :return: str with news
        """
        table = [['Feed', f"{self.news.get('feed', '')}\n"]]
        news_items = self.news.get('items')
        for n, item in enumerate(news_items):
            # table.append([1, item.get('human_text')])
            initial_news_item = item.get('human_text', '')
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

    def _get_news_as_dict(self, feed: feedparser.FeedParserDict) \
            -> Dict[str, Union[str, List[str]]]:
        """
        Returns str containing formatted news from internal attr self.feed

        :return: str with news
        """
        news = {'feed': feed.get('feed', '').get('title', ''),
                'items': []}

        for i, item in enumerate(feed.get('items')[:self.limit]):
            news_item = {
                'title': item.get('title', ''),
                'link': item.get('link', ''),
                'published': item.get('published', ''),
                'imgs': [img.get('url', '') for img in item.get('media_content', '')],
                'links': [link.get('href', '') for link in item.get('links', '')],
                'html': item.get('summary', '')
            }
            self._parse_news_item(news_item)
            news['items'].append(news_item)

        self.logger.info(f'Feedparser object is converted into dictionary')
        return news

    def _parse_news_item(self, news_item: Dict[str, Union[str, List[str]]]):
        """
        Forms a human readable string from news_item and adds it to the news_item dict
        :param news_item: news_item content
        :return: extend news_item dict with human readable news content
        """
        self.logger.info(f'Extending {news_item.get("title", "")}')
        out_str = ''
        out_str += f"\nTitle: {news_item.get('title', '')}\n" \
                   f"Date: {news_item.get('published', '')}\n" \
                   f"Link: {news_item.get('link', '')}\n"

        html = bs4.BeautifulSoup(news_item.get('html', ''), "html.parser")

        links = news_item.get('links', '')
        imgs = news_item.get('imgs', '')

        for tag in html.descendants:
            if tag.name == 'a':
                link = tag.attrs.get('href', '')
                if link not in links:
                    links.append(link)
                    self.logger.warning(f'Link {link} isn\'t found')
            elif tag.name == 'img':
                src = tag.attrs.get('src', '')
                try:
                    img_idx = imgs.index(src) + len(links) + 1
                except ValueError:
                    self.logger.warning(f'Img {src} isn\'t found')
                    imgs.append(src)
                    img_idx = len(imgs) + len(links)
                out_str += f'\n[image {img_idx}:  {tag.attrs.get("title")}][{img_idx}]'

        out_str += f'{html.getText()}\n'
        out_str += 'Links:\n'
        out_str += '\n'.join([f'[{i + 1}]: {link} (link)' for i, link in enumerate(links)]) + '\n'
        out_str += '\n'.join([f'[{i + len(links) + 1}]: {link} (image)' for i, link in enumerate(imgs)]) + '\n'

        news_item['human_text'] = out_str
