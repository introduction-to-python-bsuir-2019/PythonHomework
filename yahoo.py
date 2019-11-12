#!/usr/local/opt/python/bin/python3.7

import feedparser
from html.parser import HTMLParser
import html2text
import bs4
import typing

from utils.RssInterface import BaseRssBot
# pdfkit


class Bot(BaseRssBot):

    def get_news_as_dict(self, feed: feedparser.FeedParserDict) -> typing.Dict[str, typing.Any]:

        news = {'feed': feed.get('feed').get('title'),
                'items': []}

        for i, item in enumerate(feed.get('items')[:self.limit]):
            news['items'].append({
                'title': item.get('title'),
                'link': item.get('link', ''),
                'published': item.get('published', ''),
                'imgs': [img.get('url') for img in item.get('media_content')],
                'links': [link.get('href') for link in item.get('links')],
                'html': item.get('summary')
            })

        return news

    def get_news(self):

        out_str = f"\nFeed: {self.news.get('feed', '')}\n"

        for item in self.news['items']:

            out_str += f"\nTitle: {item.get('title', '')}\n" \
                       f"Date: {item.get('published', '')}\n" \
                       f"Link: {item.get('link', '')}\n"

            html = bs4.BeautifulSoup(item.get('html'), "html.parser")

            links = item.get('links')
            imgs = item.get('imgs')

            for tag in html.descendants:
                if tag.name == 'a':
                    pass
                elif tag.name == 'img':
                    src = tag.attrs.get('src')
                    img_idx = imgs.index(src) + len(links) + 1
                    out_str += f'\n[image {img_idx}:  {tag.attrs.get("title")}][{img_idx}]'
                elif tag.name == 'p':
                    out_str += '\n' + tag.text
                elif tag.name == 'br':
                    out_str += '\n'

            out_str += 'Links:\n'
            out_str += '\n'.join([f'[{i + 1}]: {link} (link)' for i, link in enumerate(links)]) + '\n'
            out_str += '\n'.join([f'[{i + len(links) + 1}]: {link} (image)' for i, link in enumerate(imgs)]) + '\n'

        return out_str
