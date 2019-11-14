from utils.RssInterface import BaseRssBot
import bs4
from terminaltables import SingleTable
from colorclass import Color


class Bot(BaseRssBot):

    def table_server_timings(self):
        """Return table string to be printed."""
        table_data = [
            [Color('{autogreen}<10ms{/autogreen}'), '192.168.0.100, 192.168.0.101'],
            [Color('{autoyellow}10ms <= 100ms{/autoyellow}'), '192.168.0.102, 192.168.0.103'],
            [Color('{autored}>100ms{/autored}'), '192.168.0.105'],
        ]
        table_instance = SingleTable(table_data)
        table_instance.inner_heading_row_border = False
        return table_instance.table

    def _parse_news_item(self, news_item: dict):
        out_str = ''
        out_str += f"\nTitle: {news_item.get('title', '')}\n" \
                   f"Date: {news_item.get('published', '')}\n" \
                   f"Link: {news_item.get('link', '')}\n"

        html = bs4.BeautifulSoup(news_item.get('html'), "html.parser")

        links = news_item.get('links')
        imgs = news_item.get('imgs')

        for tag in html.descendants:
            if tag.name == 'a':
                pass
            elif tag.name == 'img':
                src = tag.attrs.get('src')
                try:
                    img_idx = imgs.index(src) + len(links) + 1
                except ValueError:
                    imgs.append(src)
                    img_idx = len(imgs) + len(links)
                out_str += f'\n[image {img_idx}:  {tag.attrs.get("title")}][{img_idx}]'
            elif tag.name == 'p':
                out_str += '\n' + tag.text
            elif tag.name == 'br':
                out_str += '\n'

        # out_str += Color('{autocyan}Links:{/autocyan}\n')
        out_str += 'Links:\n'
        out_str += '\n'.join([f'[{i + 1}]: {link} (link)' for i, link in enumerate(links)]) + '\n'
        out_str += '\n'.join([f'[{i + len(links) + 1}]: {link} (image)' for i, link in enumerate(imgs)]) + '\n'

        news_item['human_text'] = out_str
