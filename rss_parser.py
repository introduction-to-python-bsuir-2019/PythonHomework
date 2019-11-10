#!/usr/local/opt/python/bin/python3.7

import feedparser
from html.parser import HTMLParser
import html2text
import bs4
# pdfkit


class RssException(Exception):
    pass


class RssParser():

    def __init__(self, limit, logger):
        self.limit = limit
        self.logger = logger
        self.feed = feedparser.FeedParserDict()


    def parse_rss(self, url: str):
        self.logger.info(f'Lets to grab news from {url}')

        self.feed = feedparser.parse(url)

        if self.feed.get('bozo_exception'):
            #
            exception = self.feed.get('bozo_exception').getMessage()
            raise RssException(f'Error while parsing xml: \n {exception}')

        self.logger.info(f'well formed xml = {self.feed["bozo"]}\n'
                         f'url= {self.feed["url"]}\n'
                         f'title= {self.feed["channel"]["title"]}\n'
                         f'description= {self.feed["channel"]["description"]}\n'
                         f'link to recent changes= {self.feed["channel"]["link"]}\n'
                         )
        # return self.feed

    def get_news(self):
        news = self.feed['items'][:self.limit]
        html_parser = HTMLParser()
        title = self.feed.get('feed').get('title')
        news_out = []

        text_maker = html2text.HTML2Text()
        text_maker.ignore_links = True
        text_maker.bypass_tables = False

        for i, item in enumerate(news):
            id = item['id']
            tags = [tag.get('term') for tag in item.get('tags', '')]

            imgs = [img.get('url') for img in item.get('media_content')]
            links = [link.get('href') for link in item.get('links')]

            html = bs4.BeautifulSoup(item.get('summary'), "html.parser")
            out_str = ''
            for tag in html.descendants:
                if tag.name == 'a':
                    attr = tag.attrs.get('href')
                    link_idx = links.index(attr) + 1
                    out_str += f'\n[link {link_idx}: {tag.text}][{link_idx}]'
                elif tag.name == 'img':
                    src = tag.attrs.get('src')
                    img_idx = imgs.index(src) + len(links) + 1
                    out_str += f'\n[image {img_idx}:  {tag.attrs.get("title")}][{img_idx}]'
                elif tag.name == 'p':
                    out_str += '\n\t' + tag.text
                elif tag.name == 'br':
                    out_str += '\n'

            out_str += '\n'.join([f'[{i + 1}]: {link} (link)' for i, link in enumerate(links)])
            out_str += '\n'.join([f'[{i + len(links) + 1}]: {link} (image)' for i, link in enumerate(imgs)])

            news_text = html.getText()

            news_out.append({
                'title': html_parser.unescape(item.get('title', '')),
                'link': item.get('link', ''),
                # 'author': item.get('author', ''),
                'published': item.get('published', ''),
                'imgs': imgs,
                'out_str': out_str,
                'links': links,

            })
        return news_out