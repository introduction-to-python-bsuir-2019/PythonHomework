"""Module that get a rss from the news portal"""

import feedparser
import logging
from bs4 import BeautifulSoup
from colored import fore, style

from rssreader.exceptions import all_exceptions


class RssParser:
    """The class that receives the news in rss format"""
    def __init__(self, url: str, limit: int = None) -> None:
        self.url = url
        self.limit = limit
        self.articles = []

    @property
    def limit(self) -> int:
        """A property that returns the limit value"""
        return self.__limit

    @limit.setter
    def limit(self, value) -> None:
        """A property that checks for a negative value"""
        self.__limit = value if value is None or value > 0 else 0

    def _check_limit(self, enrtries: list) -> int:
        """Function that checks the maximum limit value"""
        self.count_news = len(enrtries)

        if self.limit is not None:
            return min(self.limit, self.count_news)
        else:
            return self.count_news

    def _get_rss_from_url(self) -> dict:
        """
        Function that checks the possibility of receiving news and,
        if successful, receives them
        """
        html_news = feedparser.parse(self.url)

        if html_news.bozo == 1:
            err_msg = "Check your link or internet connection"
            raise all_exceptions.InvalidLinkOrInternetConnectionError(err_msg)

        return html_news

    def parse_news(self) -> list:
        """
        Function that returns a list of news that was received by parsing rss
        """
        self.html_news = self._get_rss_from_url()
        self.limit = self._check_limit(self.html_news.entries)

        parsing_news = []
        try:
            feed = self.html_news.feed.title

            for entry in self.html_news.entries[:self.limit]:
                temp_dict = {
                    'Feed': feed,
                    'Title': entry.title.replace("&#39;", "'"),
                    'Date': entry.published,
                    'Link': entry.link,
                    'Description': BeautifulSoup(
                        entry.summary, features="html.parser"
                        ).text,
                    'Links': [link.get("src") for link in BeautifulSoup(
                        entry.summary, features="html.parser"
                        ).find_all("img") if link.get("src")]
                }
                parsing_news.append(temp_dict)

            return parsing_news
        except AttributeError as e:
            logging.error(e)
            err_msg = "Сan't get rss, because the news has an incorrect format"
            raise all_exceptions.ParsingNewsError(err_msg)

    def __find_type_link(self, link) -> str:
        """
        Function that determines the type of file that is located at the link
        """
        return "(image)" if link.find(".mp4") == -1 else "(video)"

    def __make_pretty_links(self, link, links) -> str:
        """
        The function that returns the string in which the numeric
        representation of all links from the news is located
        """
        links_list = []
        len_list = 0

        if isinstance(link, list):
            len_list = len(link)
            for index, element in enumerate(link):
                if element:
                    links_list.append(f"[{(index + 1)}]: {element}(link)")
        elif link:
            len_list = 1
            links_list.append(f"[1]: {link}(link)")

        if isinstance(links, list):
            for index, element in enumerate(links):
                if element:
                    type_link = self.__find_type_link(element)
                    links_list.append(
                        f"[{(index+1+len_list)}]: {element}{type_link}"
                        )
        elif links:
            type_link = self.__find_type_link(links)
            links_list.append(f"[{len_list + 1}]: {links}{type_link}")

        return "\n".join(links_list)

    def make_pretty_rss(self, news) -> str:
        """
        Function that returns the final representation
        of news that was obtained from the rss link
        """
        pretty_string = []

        for article in news:
            links = self.__make_pretty_links(
                        article['Link'],
                        article['Links']
                        )

            pretty_string.append(
                f"\nFeed: {article['Feed']}\n\nTitle: {article['Title']} \
                \nDate: {article['Date']}\nLink: {article['Link']} \
                \n\n{article['Description']}\n\nLinks:\n{links}\n\n"
            )
        return "".join(pretty_string)

    def make_pretty_rss_colorize(self, news) -> str:
        """
        Function that returns the final color presentation
        of news that was obtained from the rss link
        """
        pretty_string = []

        for article in news:
            links = self.__make_pretty_links(
                        article['Link'],
                        article['Links']
                        )

            pretty_string.append(
                fore.RED + style.BOLD +
                f"\nFeed: {article['Feed']}\n\nTitle: {article['Title']}" +
                style.RESET + fore.GREEN + style.BOLD +
                f"\nDate: {article['Date']}\nLink: {article['Link']}" +
                style.RESET + fore.BLUE + style.BOLD +
                f"\n\n{article['Description']}" +
                style.RESET + fore.MAGENTA + style.BOLD +
                f"\n\nLinks:\n{links}\n\n" + style.RESET
            )
        logging.info("Text painted in RGBM")
        return "".join(pretty_string)
