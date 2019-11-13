#!/usr/local/opt/python/bin/python3.7

import feedparser
import bs4
import typing

from utils.RssInterface import BaseRssBot


class Bot(BaseRssBot):

    def _get_news_as_dict(self, feed: feedparser.FeedParserDict) -> typing.Dict[str, typing.Any]:

        news = {'feed': feed.get('feed').get('title'),
                'items': []}

        for i, item in enumerate(feed.get('items')[:self.limit]):
            news_item = {
                'title': item.get('title'),
                'link': item.get('link', ''),
                'published': item.get('published', ''),
                'imgs': [img.get('url') for img in item.get('media_content')],
                'links': [link.get('href') for link in item.get('links')],
                'authors': [author.get('name') for author in item.get('authors')],
                'tags': [tag.get('term') for tag in item.get('tags', '')],
                'html': item.get('summary')
            }
            self._parse_news_item(news_item)
            news['items'].append(news_item)

        return news

    def _parse_news_item(self, news_item: typing.Dict[str, typing.Any]):

        out_str = ''
        out_str += f"\nTitle: {news_item.get('title', '')}\n" \
                   f"Date: {news_item.get('published', '')}\n" \
                   f"Link: {news_item.get('link', '')}\n"
        out_str += f"Authors: {', '.join(news_item.get('authors'))}\n"
        out_str += f"Tags: {', '.join(news_item.get('tags'))}\n"

        html = bs4.BeautifulSoup(news_item.get('html'), "html.parser")

        links = news_item.get('links')
        imgs = news_item.get('imgs')

        for tag in html.descendants:
            if tag.name == 'a':
                pass
            elif tag.name == 'img':
                src = tag.attrs.get('src')
                # src = src.replace('thumbnails/', '')
                try:
                    img_idx = imgs.index(src) + len(links) + 1
                except ValueError:
                    imgs.append(src)
                    img_idx = len(imgs) + len(links)

                out_str += f'\n[image {img_idx}:  {tag.attrs.get("alt")}][{img_idx}]'
            elif tag.name == 'p':
                out_str += '\n' + tag.text
            elif tag.name == 'br':
                out_str += '\n'
        out_str += f'\n{html.getText()}\n'
        out_str += 'Links:\n'
        out_str += '\n'.join([f'[{i + 1}]: {link} (link)' for i, link in enumerate(links)]) + '\n'
        out_str += '\n'.join([f'[{i + len(links) + 1}]: {link} (image)' for i, link in enumerate(imgs)]) + '\n'

        news_item['human_text'] = out_str
