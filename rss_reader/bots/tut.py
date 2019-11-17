#!/usr/local/opt/python/bin/python3.7

import bs4
import feedparser
import typing

from rss_reader.utils.RssInterface import BaseRssBot


class Bot(BaseRssBot):

    def _get_news_as_dict(self, feed: feedparser.FeedParserDict) -> typing.Dict[str, typing.Any]:
        """
        Returns str containing formatted news from internal attr self.feed

        :return: str with news
        """
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
        self.logger.info(f'Feedparser object is converted into dictionary')
        return news

    def _parse_news_item(self, news_item: typing.Dict[str, typing.Any]) -> None:
        """
        Forms a human readable string from news_item and adds it to the news_item dict
        :param news_item: news_item content
        :return: extend news_item dict with human readable news content
        """
        self.logger.info(f'Extending {news_item.get("title")}')

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
                if src in imgs:
                    img_idx = imgs.index(src) + len(links) + 1
                else:
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
