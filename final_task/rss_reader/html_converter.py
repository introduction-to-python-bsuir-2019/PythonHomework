"""
This module provides tools for converting news to HTML format
"""

import os
import rss_reader.templates.html_templates as templates
from rss_reader.os_funcs import create_directory, download_images
from rss_reader.news_date import get_date_pretty_str


def convert_news_to_html(news, path):
    """
    This function converts news to HTML format
    :param news: News class instance
    :param path: path to result file (str)
    :return: None
    """
    directory = os.path.dirname(path)
    src_dir_name = os.path.splitext(path)[0]
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
    with open(path, 'w', encoding='utf-8') as output_file:
        output_file.write(news_html)
