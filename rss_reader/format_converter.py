"""Contain all RSS news convert related objects."""
import logging
import os
import shutil
from io import BytesIO
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import requests
from PIL import Image
from tqdm import tqdm
from xhtml2pdf import pisa
from yattag import Doc, indent

from rss_reader.config import FONTS
from rss_reader.exceptions import RSSConvertationException, RSSCreateImageFolderException, RSSCreateImageException


class Converter:
    """Convert news to selected format."""

    def __init__(self, news_data: Dict[str, List[Union[str, Dict[str, str]]]],
                 html_path: Optional[str] = None, pdf_path: Optional[str] = None) -> None:
        """Initialze HTML converter."""
        self._news_data = news_data
        self.html_path = os.path.abspath(html_path) if html_path else html_path
        self.pdf_path = os.path.abspath(pdf_path) if pdf_path else pdf_path
        self.img_folder = None
        self.png_extension = 'png'

    def convert_news(self):
        """Convert news to the selected format."""
        try:
            self.create_image_folder(self.html_path or self.pdf_path)
            html_document = self.get_html(True)
        except RSSCreateImageFolderException:
            print('News is not converted, because can\'t create a folder for images')
        except RSSCreateImageException:
            print('News is not converted, because can\'t save pictures to a images folder')
            self.remove_image_folder()
        else:
            if self.html_path:
                try:
                    self.conver_to_html(html_document)
                except RSSConvertationException:
                    print('News is not converted to HTML format, because can\'t save .html file')
            if self.pdf_path:
                try:
                    self.conver_to_pdf(html_document)
                except RSSConvertationException:
                    print('News is not converted to PDF format, because can\'t save .pdf file')

    def create_image_folder(self, image_path: str) -> None:
        """Create folder for news images."""
        self.img_folder = os.path.join(os.path.dirname(image_path), Path(image_path).resolve().stem)
        if not os.path.exists(self.img_folder):
            try:
                os.mkdir(self.img_folder)
            except OSError as error:
                raise RSSCreateImageFolderException(f'Can\'t create directory for image files: {self.img_folder}',
                                                    error)

    def remove_image_folder(self) -> None:
        """Remove folder for news images."""
        try:
            shutil.rmtree(self.img_folder)
        except OSError:
            logging.warning(f'Can\'t delete directory with image files: \'{self.img_folder}\' '
                            'Delete folder manually')

    def get_image_link(self, link: str, download: Optional[bool] = False,
                       image_postfix: Optional[str] = '') -> Union[str, None]:
        """Return image link or local path."""
        return self.download_image(link, image_postfix) if download else link

    def download_image(self, link: str, image_postfix: str) -> Union[str, None]:
        """Вownloads picture from the link."""
        image_path = os.path.join(self.img_folder,
                                  '.'.join([f'image_link_{image_postfix}', self.png_extension]))
        response = requests.get(link)
        if response.status_code == 200:
            try:
                Image.open(BytesIO(response.content)).convert("RGBA").save(image_path)
            except OSError as error:
                raise RSSCreateImageException(f'Can\'t create image with path \'{image_path}\'', error)
            else:
                return image_path
        else:
            return None

    def get_html(self, download_images: bool):
        """Return HTML document created from news data."""
        def add_styles() -> None:
            """Add styles to HTML stream."""
            doc.asis('''
                @page {
                    size: 21cm 200cm;
                    @frame content_frame {
                        left: 10pt;
                        right: 10pt;
                        width: 575pt;
                        top: 10pt;
                        down: 10pt;
                        height: 5650pt;
                    }
                }
                @font-face {
                    font-family:
                    Arial;
                    src: url(\"''' + FONTS + '''\");
                }
                body {
                    font-family: Arial;
                }''')

        def add_news_head() -> None:
            """Add news head to HTML stream."""
            text('[News {0}]'.format(news_number))
            doc.stag('br')
            text('Title: {0}'.format(news.get('title', '')))
            doc.stag('br')
            text('Date: {0}'.format(news.get('published', '')))
            doc.stag('br')
            text('Link: ')
            news_link = news.get('link', '')
            with tag('a', href=news_link):
                text(news_link)

        def add_news_description() -> None:
            """Add news description to HTML stream."""
            item_type = item.get('type', '')
            if item_type == 'text':
                text(item.get('text', ''))
            elif item_type == 'link':
                link = item.get('link', '')
                link_text = item.get('text', '')
                with tag('a', href=link):
                    text(link_text if link_text else link)
            elif item_type == 'image':
                image_postfix = f'{news_number}_{link_number}'
                image_path = self.get_image_link(item.get('link', ''), download_images, image_postfix)
                if not image_path:
                    return
                doc.stag('br')
                doc.stag('img', src=image_path)
                doc.stag('br')

        doc, tag, text = Doc().tagtext()
        doc.asis('<!DOCTYPE html>')
        with tag('html'):
            doc.stag('meta', **{'http-equiv': 'Content-Type', "content": 'text/html; charset=utf-8'})
            with tag('style', type="text/css"):
                add_styles()
            with tag('body'):
                with tag('p', style='font-size: 2em'):
                    text('Feed: {0}'.format(self._news_data.get('feed', '')))
                news_list = self._news_data.get('news', [])
                for news_number, news in enumerate(tqdm(news_list, desc='Converting: ', leave=False), start=1):
                    with tag('p'):
                        add_news_head()
                    for link_number, item in enumerate(news.get('description', ''), start=1):
                        add_news_description()
                    doc.stag('br')
                    doc.stag('br')
        return indent(doc.getvalue(), indent_text=True)

    def conver_to_html(self, source_html: str):
        """Convert news to HTML format."""
        try:
            with open(self.html_path, 'w') as file_obj:
                file_obj.write(source_html)
        except OSError as error:
            raise RSSConvertationException(f'Can\'t create HTML file: {self.img_folder}', error)
        logging.info('Successful conversion to HTML')

    def conver_to_pdf(self, source_html: str):
        """Convert news to PDF format."""
        try:
            with open(self.pdf_path, 'w+b') as result_file:
                pisa_status = pisa.CreatePDF(source_html, dest=result_file, encoding='UTF-8')
        except OSError as error:
            raise RSSConvertationException(f'Can\'t create FDP file: {self.img_folder}', error)
        if not self.html_path:
            self.remove_image_folder()
        if pisa_status.err:
            raise RSSConvertationException('Can\'t create PDF file', pisa_status.err)
        logging.info('Successful conversion to PDF')


def format_to_convert(data: List[Dict[Any, Any]]) -> Dict[str, List[Dict[str, Union[str, List[Dict[str, str]]]]]]:
    """Format cache data do convert data."""
    convert_data = {'feed': '', 'news': []}
    news_temp = {'title': '', 'published': '', 'link': '', 'description': []}
    if data:
        convert_data.update({'feed': next(iter(data)).get('feed', '')})
    news_list = []
    for feed_data in data:
        news_data = feed_data.get('news', {})
        news = news_temp.copy()
        news.update({'title': news_data.get('title', ''),
                     'published': news_data.get('published', ''),
                     'link': news_data.get('link', ''),
                     'description': news_data.get('description', [])})
        news_list.append(news)
    convert_data.update({'news': news_list})
    return convert_data
