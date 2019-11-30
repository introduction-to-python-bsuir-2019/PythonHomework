#!/usr/bin/env python3

"""
Convert RSS feed to HTML/PDF
"""

import logging
import shutil
from pathlib import Path

import requests
from lxml import etree
from xhtml2pdf import pisa
from jinja2 import Template
from bs4 import BeautifulSoup
from ebooklib import epub
from ebooklib.utils import parse_html_string

from rss_reader.exceptions import RSSFeedException


class Converter:
    """ Class for conversion RSS feed

        Attributes:
            title (str): Title of RSS feed
            entries (list): List of RSS news
            out_dir (str): Directory where output will be saved
    """

    def __init__(self, title, entries, out_dir, image_dir="images", temp_image_dir="_temp_images"):
        self.title = title
        self.entries = entries
        self.out_dir = Path(out_dir)

        self.image_dir = Path(image_dir)
        self.temp_image_dir = Path(temp_image_dir)

        self.font_path = Path(__file__).resolve().parent / 'fonts/Roboto-Regular.ttf'

    def _create_directories(self, image_dir):
        """ Create directories if not exist (self.out_dir and self.out_dir/image_dir) """
        if not self.out_dir.is_dir():
            logging.info("Creating directory /%s", self.out_dir)
            self.out_dir.mkdir(parents=True, exist_ok=True)

        if not image_dir.is_dir():
            logging.info("Creating directory /%s", image_dir)
            image_dir.mkdir(parents=True, exist_ok=True)

    def _download_image(self, url, image_dir):
        """ Download image in self.out_dir/image_dir

            Returns:
                filename: image name
        """
        logging.info("Starting image download")

        image_dir = self.out_dir / image_dir

        try:
            self._create_directories(image_dir)
        except OSError:
            raise RSSFeedException(message="Сan not create directory")

        filename = url.split('/')[-1]
        response = requests.get(url, allow_redirects=True)

        with open(image_dir / filename, 'wb') as handler:
            handler.write(response.content)

        return filename

    def _replace_urls_to_local(self, entry):
        """ Replace img URLs in entry to local file path

            Args:
                entry (dict): News dict

        """
        soup = BeautifulSoup(entry.summary, "html.parser")
        images = [img['src'] for img in soup.findAll('img') if img.has_attr('src')]
        for image in images:
            filename = self._download_image(image, self.image_dir)
            downloaded_img_local_path = Path(self.image_dir / filename)
            entry.summary = entry.summary.replace(image, str(downloaded_img_local_path))

        return entry

    def _replace_urls_to_absolute(self, entry):
        """ Replace img URLs in entry to local absolute file path

            Special for xhtml2pdf (xhtml2pdf support only absolute file path)

            Args:
                entry (dict): News dict
        """
        soup = BeautifulSoup(entry.summary, "html.parser")
        images = [img['src'] for img in soup.findAll('img') if img.has_attr('src')]
        for image in images:
            filename = self._download_image(image, self.temp_image_dir)
            downloaded_img_absolute_path = Path(self.out_dir / self.temp_image_dir / filename).absolute()
            entry.summary = entry.summary.replace(image, str(downloaded_img_absolute_path))

        return entry

    def _get_entry_html(self, entry):
        template = """<div class='entry'>
                            <h2 class='title'>{{entry.title}}</h2>
                            <p><span class='date'>{{entry.published}}</span></p>
                            <p><a class='link' href='{{entry.link}}'>{{entry.link}}</a></p>
                            <div class='description'>{{entry.summary}}</div>
                      </div>"""
        temp_entry = self._replace_urls_to_local(entry)
        html = Template(template).render(title=self.title, entry=temp_entry)
        return html

    def _gen_html(self, is_cyrillic_font=False, is_absolute_urls=False):
        """ Generates HTML

            Args:
                is_cyrillic_font (bool) Should we generate HTML with cyrillic_font (to convert to PDF)?
                is_absolute_urls (bool): Should we generate HTML with absolute URLs (to convert to PDF)?

            Returns:
                html: String with HTML code
        """
        template = '''<html>
            <head>
                <meta charset="utf-8">
                <title>{{title}}</title>
                
                <style type=text/css>
                    {% if is_cyrillic_font %}
                    @font-face { font-family: Roboto; src: url({{font_path}}), ; }
                    {% endif %}
                    body{
                      font-family: Roboto;
                    }
                    div 
                    { 
                      margin: 10px; 
                      font-size: 20px; 
                    }
                </style> 
            </head>
            <body>
                {% for entry in entries %}
                    <div class='entry'>
                        <h2 class='title'>{{entry.title}}</h2>
                        <p><span class='date'>{{entry.published}}</span></p>
                        <p><a class='link' href='{{entry.link}}'>{{entry.link}}</a></p>
                        <div class='description'>{{entry.summary}}</div>
                    </div>
                {% endfor %}
            </body>
        </html>'''
        if is_absolute_urls:
            self.entries = [self._replace_urls_to_absolute(entry) for entry in self.entries]
        else:
            self.entries = [self._replace_urls_to_local(entry) for entry in self.entries]

        html = Template(template).render(title=self.title, entries=self.entries,
                                         is_cyrillic_font=is_cyrillic_font, font_path=self.font_path)
        return html

    def entries_to_html(self):
        """ Generate HTML file in self.out_dir """
        html = self._gen_html()

        with open(Path(self.out_dir) / 'out.html', 'w') as file_object:
            file_object.write(html)

    def entries_to_pdf(self):
        """ Generate PDF file in self.out_dir """
        html = self._gen_html(is_cyrillic_font=True, is_absolute_urls=True)

        with open(Path(self.out_dir) / 'out.pdf', 'w+b') as file:
            pdf = pisa.CreatePDF(html, dest=file, encoding='UTF-8')

        # Delete temp folder (self.out_dir/self.temp_image_dir)
        temp_img_dir = Path(self.out_dir / self.temp_image_dir)
        logging.info("Cleaning up %s", temp_img_dir)
        shutil.rmtree(temp_img_dir)

        if pdf.err:
            raise RSSFeedException(message="Error during PDF generation")

    def entries_to_epub(self):
        """ Generate EPUB file in self.out_dir """
        html = self._gen_html()

        def add_images_to_book():
            html_tree = parse_html_string(chapter.content)

            for img_elem in html_tree.iterfind('.//img'):
                href = img_elem.attrib['src']
                img_local_filename = self.out_dir / href

                with open(img_local_filename, 'br') as file_object:
                    epimg = epub.EpubImage()
                    epimg.file_name = href
                    epimg.set_content(file_object.read())

                    book.add_item(epimg)

            chapter.content = etree.tostring(html_tree, pretty_print=True, encoding='utf-8')

        book = epub.EpubBook()

        # set metadata
        book.set_identifier('id1337')
        book.set_title(self.title)
        book.set_language('en, ru')

        book.add_author('DiSonDS')

        # create chapter
        chapter = epub.EpubHtml(title='Intro', file_name=f'chap_01.xhtml', lang='en, ru')
        chapter.content = html

        add_images_to_book()

        # add chapter
        book.add_item(chapter)

        # define Table Of Contents
        book.toc = (epub.Link('chap_01.xhtml', 'Introduction', 'intro'),
                    (epub.Section(self.title),
                     (chapter,))
                    )

        # add default NCX and Nav file
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())

        # define CSS style
        style = 'BODY {color: white;}'
        nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)

        # add CSS file
        book.add_item(nav_css)
        # basic spine
        book.spine = ['nav', chapter]

        # write to the file
        epub.write_epub(Path(self.out_dir) / 'out.epub', book, {})
