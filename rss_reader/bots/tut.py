#!/usr/local/opt/python/bin/python3.7
import attr
import bs4
import feedparser
import typing

from rss_reader.utils.rss_interface import BaseRssBot
from ..utils.data_structures import NewsItem, News


@attr.s
class TutNewItem(NewsItem):
    tags: typing.List[str] = attr.ib()
    authors: typing.List[str] = attr.ib()


class Bot(BaseRssBot):

    def _feed_to_news(self, feed: feedparser.FeedParserDict) -> News:
        """
        Returns str containing formatted news from internal attr self.feed

        :return: str with news
        """
        news_items = []

        for i, item in enumerate(feed.get('items')[:self.limit]):

            news_items.append(TutNewItem(
                title=item.get('title', ''),
                link=item.get('link', ''),
                published=item.get('published', ''),
                imgs=[img.get('url', '') for img in item.get('media_content', '')],
                links=[link.get('href', '') for link in item.get('links', '')],
                html=item.get('summary', ''),
                authors=[author.get('name', '') for author in item.get('authors', '')],
                tags=[tag.get('term', '') for tag in item.get('tags', '')],
            ))

        news = News(
            feed=feed.get('feed', '').get('title', ''),
            link=feed.get('feed', '').get('link', ''),
            items=news_items,
        )
        self.logger.info(f'Feedparser object is converted into news_item obj with TUT news')

        return news

    def _parse_news_item(self, news_item: TutNewItem) -> str:
        """
        Forms a human readable string from news_item and adds it to the news_item dict
        :param news_item: news_item content
        :return: human readable news content
        """
        self.logger.info(f'_parse_news_item_tut.by  Extending {news_item.title}')

        out_str = ''
        out_str += f"\nTitle: {news_item.title}\n" \
                   f"Date: {news_item.published}\n" \
                   f"Link: {news_item.link}\n"
        out_str += f"Authors: {', '.join(news_item.authors)}\n"
        out_str += f"Tags: {', '.join(news_item.tags)}\n"

        html = bs4.BeautifulSoup(news_item.html, "html.parser")

        links = news_item.links
        imgs = news_item.imgs

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

        return out_str
