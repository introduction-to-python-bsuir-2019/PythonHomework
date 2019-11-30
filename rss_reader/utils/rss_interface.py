import bs4
import json
import logging
import feedparser

from abc import ABCMeta, abstractmethod
from colorama import Fore, Back, Style, init
from pathlib import Path
from terminaltables import SingleTable
from textwrap import wrap

from ..utils.data_structures import NewsItem, News, ConsoleArgs
from ..utils.decorators import call_save_news_after_method
from ..utils.exceptions import RssException
from ..utils.sqlite import RssDB
from ..utils.rss_utils import parse_date_from_console
from ..utils.pdf import PdfWriter
from ..utils.html_writer import HtmlWriter


class RssBotInterface(metaclass=ABCMeta):
    """
    Interface for Rss reader classes. Mandatory methods are: get_news(), get_json()
    and internal parser's methods for particular cases of each bot
    """

    STORAGE = Path.cwd().joinpath('storage')

    def __init__(self, args: ConsoleArgs, logger: logging.Logger):

        self.logger = logger
        self.logger.debug(f'Bot initialization starts')
        self.limit = args.limit
        self.screen_width = args.width

        if not args.date:  # Load news from url
            self.logger.debug(f'Downloading news from {args.url}')
            self.url = args.url
            feed = self._parse_raw_rss()
            self.news = self._feed_to_news(feed)
        else:  # load from storage
            self.logger.debug(f'Loading news from storage')
            self.news = self._load_news(args.date)
        if args.to_pdf:
            self._print_news_to_pdf(args.to_pdf)
        if args.to_html:
            self._print_news_to_html(args.to_html)
        self.logger.info(f'Bot initialization is completed')

    @abstractmethod
    def print_news(self) -> str:
        """
        Returns str containing formatted news

        :return: str with news
        """

    def _print_news_to_pdf(self, path_to_pdf: str) -> None:
        pdf_writer = PdfWriter(self.logger)
        pdf_writer.store_news(self.news, path_to_pdf)

    def _print_news_to_html(self, path_to_html: str) -> None:
        html_writer = HtmlWriter(self.logger)
        html_writer.store_news(self.news, path_to_html)

    @call_save_news_after_method
    def get_json(self) -> str:
        """
        Return json formatted news

        :return: json formatted string
        """
        self.logger.info(f'Returning news in JSON format')

        return json.dumps(self.news, indent=4)

    @abstractmethod
    def _feed_to_news(self, feed: feedparser.FeedParserDict) -> News:
        """
        Converts FeedParserDict obj to News obj

        :return: News
        """

    def store_news(self) -> None:
        """Method stores news to DB"""
        if self.news.feed.find('Stored news from date') >= 0:
            return
        db = RssDB(self.logger)
        db.insert_news(self.news)

        # clear DB object
        del db

    def _load_news(self, news_date: str) -> News:
        """
        Load new from storage and convert them into NEWS class

        :param date: date string in %Y%m%d format
        :return: NEWS object with loaded news
        """
        # Check if the news_date with correct format:
        news_date = parse_date_from_console(news_date)

        db = RssDB(self.logger)

        loaded_news = db.load_news(news_date)
        if len(loaded_news) == 0:
            raise RssException(f'There is no news published with the {news_date} date. Try another one.')
        # return news
        return News(
            feed=f'Stored news from date: {news_date}',
            link=db._DB,
            items=loaded_news,
        )

    @abstractmethod
    def _parse_raw_rss(self) -> feedparser.FeedParserDict:
        """
        Parsing news by url

        Result stores into internal attribute self.feed
        :return: None
        """

    @abstractmethod
    def _parse_news_item(self, news_item: NewsItem) -> str:
        """
        Forms a human readable string from news_item and adds it to the news_item dict

        :param news_item: news_item content
        :return: human readable news content
        """
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

    @call_save_news_after_method
    def print_news(self) -> str:
        """
        Returns str containing formatted news

        :return: str with news
        """
        table = [[f'{Fore.GREEN}Feed',
                  f"{Fore.GREEN}Title: {self.news.feed}{Fore.RESET}\n"
                  f"{Fore.GREEN}Link: {Fore.BLUE}{self.news.link}{Fore.RESET}"]]
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

            table.append([f'{Fore.GREEN}{n + 1}{Fore.RESET}', '\n'.join(splitted_by_paragraphs)])

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
        out_str += f"\n{Fore.GREEN}Title: {Fore.CYAN} {news_item.title} {Fore.RESET}\n" \
                   f"{Fore.GREEN}Date: {Fore.CYAN}{news_item.published}{Fore.RESET}\n" \
                   f"{Fore.GREEN}Link: {Fore.BLUE}{news_item.link}{Fore.RESET}\n"

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
        out_str += f'{Fore.RED}Links:{Fore.RESET}\n'
        out_str += '\n'.join([f'{Fore.LIGHTMAGENTA_EX}[{i + 1}]{Fore.RESET}: '
                              f'{Fore.BLUE}{link}{Fore.RESET} (link)' for i, link in enumerate(links)]) + '\n'
        out_str += '\n'.join([f'{Fore.LIGHTMAGENTA_EX}[{i + len(links) + 1}]{Fore.RESET}: '
                              f'{link} (image)' for i, link in enumerate(imgs)]) + '\n'

        return out_str
