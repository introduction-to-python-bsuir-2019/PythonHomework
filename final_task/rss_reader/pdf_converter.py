"""
This module provides tools for converting news to PDF format
"""

import os
from fpdf import FPDF
from rss_reader.news_date import get_date_pretty_str
from rss_reader.os_funcs import get_project_directory_path, download_images, create_directory

src_dir_name = 'images'


def convert_news_to_pdf(news, path):
    """
    This function converts news to PDF format
    :param news: News class instance
    :param path: path to result file (str)
    :return: None
    """
    line_height = 5
    project_directory_path = get_project_directory_path()
    path_to_images = create_directory(project_directory_path, src_dir_name)

    document = FPDF()
    document.add_page()
    document.set_right_margin(margin=10)
    path_to_font = os.path.join(os.path.dirname(__file__), 'fonts', 'ttf', 'DejaVuSansCondensed.ttf')
    document.add_font('DejaVu', '', path_to_font, uni=True)
    document.set_font('DejaVu', size=14)

    document.multi_cell(w=0, ln=1, h=line_height, txt=news.feed, align='C')
    document.ln(line_height * 2)

    for item in news.items:
        document.set_font_size(12)
        document.multi_cell(w=0, ln=1, h=line_height, txt=item.title)
        document.ln(h=line_height + 3)
        document.set_font_size(10)

        images_paths = download_images(item, path_to_images, news.items.index(item))

        for image_path in images_paths:
            document.image(image_path, w=100)

        document.ln(h=line_height)
        document.multi_cell(w=0, ln=1, h=line_height, txt=get_date_pretty_str(item.date))
        document.ln(h=line_height)
        document.multi_cell(w=0, ln=1, h=line_height, txt=item.content.text)
        document.ln(h=line_height)
        document.cell(w=0, ln=1, h=line_height, txt='Links: ')

        for link in item.content.links:
            document.write(h=line_height, txt=link, link=link)

        document.ln(h=line_height)
        document.cell(w=0, h=line_height, txt='Source: ')
        document.write(h=line_height, txt=item.link, link=item.link)
        document.ln(h=line_height * 2)

    document.output(path, 'F')
