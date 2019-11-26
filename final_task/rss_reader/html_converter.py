"""
THis module provides tools for converting news to HTML format
"""

import os
import rss_reader.templates.html_templates as templates
from rss_reader.os_funcs import create_directory
from rss_reader.news_date import get_date_pretty_str

src_dir_name = 'src'


def convert_news_to_html(news, path):
    """
    THis function converts news to HTML format
    :param news: News class instance
    :param path: path to result file (str)
    :return: None
    """
    directory = os.path.dirname(path)
    path_to_images = create_directory(directory, src_dir_name)
    news_items_html = []
    for item in news.items:
        images_info = zip(download_images(item, path_to_images, news.items.index(item)), item.content.images)
        images_html = [templates.img.render(src=img_path, alt=img.alt) for img_path, img in images_info]
        news_item_html = templates.news_item.render(images=images_html, title=item.title,
                                                    date=get_date_pretty_str(item.date),
                                                    text=item.content.text, link=item.link,
                                                    links=item.content.links)
        news_items_html.append(news_item_html)
    news_html = templates.news.render(news=news_items_html, title=news.feed)
    with open(path, 'w') as output_file:
        output_file.write(news_html)


def download_images(news_item, path_to_dir, item_index):
    """
    THis function downloads images from internet
    :param news_item: NewsItem class instance
    :param path_to_dir: path to destination directory (str)
    :param item_index: news_item index in news object (int)
    :return: list of image paths (list)
    """
    img_path_list = []
    img_index = 0
    for img in news_item.content.images:
        img_path = img.download(path_to_dir, f'{str(item_index)}_{str(img_index)}.jpeg')
        img_path_list.append(img_path)
        img_index += 1
    return img_path_list
