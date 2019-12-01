"""Yahoo specified rss parser bot"""
import bs4

from colorama import Fore

from ..utils.rss_interface import BaseRssBot
from ..utils.data_structures import NewsItem


class Bot(BaseRssBot):
    """Yahoo specified rss parser bot"""

    def _parse_news_item(self, news_item: NewsItem) -> str:
        """
        Forms a human readable string from news_item and adds it to the news_item dict
        :param news_item: news_item content
        :return: human readable news content
        """

        out_str = ''
        out_str += f"\n{self.colors.green}Title: {self.colors.cyan} {news_item.title} {Fore.RESET}\n" \
                   f"{self.colors.green}Date: {self.colors.cyan}{news_item.published}{Fore.RESET}\n" \
                   f"{self.colors.green}Link: {self.colors.blue}{news_item.link}{Fore.RESET}\n"

        html = bs4.BeautifulSoup(news_item.html, "html.parser")

        links = news_item.links
        imgs = news_item.imgs

        for tag in html.descendants:
            if tag.name == 'a':
                pass
            elif tag.name == 'img':
                src = tag.attrs.get('src')
                if src in imgs:
                    img_idx = imgs.index(src) + len(links) + 1
                else:
                    imgs.append(src)
                    img_idx = len(imgs) + len(links)
                out_str += f'\n[image {img_idx}:  {tag.attrs.get("title")}][{img_idx}]'
            elif tag.name == 'p':
                out_str += '\n' + tag.text
            elif tag.name == 'br':
                out_str += '\n'

        # out_str += Color('{autocyan}Links:{/autocyan}\n')
        out_str += f'{self.colors.red}Links:{Fore.RESET}\n'
        out_str += '\n'.join([f'[{i + 1}]: {link} (link)' for i, link in enumerate(links)]) + '\n'
        out_str += '\n'.join([f'[{i + len(links) + 1}]: {link} (image)' for i, link in enumerate(imgs)]) + '\n'

        return out_str
