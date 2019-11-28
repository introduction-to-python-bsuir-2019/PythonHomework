#!/usr/bin/env python3

"""
Convert RSS feed to HTML/PDF
"""

import logging
import shutil
from pathlib import Path

import requests
import pdfkit
from jinja2 import Template
from bs4 import BeautifulSoup

from rss_reader.configuration import IMAGE_DIR, TEMP_IMAGE_DIR
#  from rss_reader.exceptions import RSSFeedException


class Converter:
    """ Class for conversion RSS feed

        Attributes:
            title (str): Title of RSS feed
            entries (list): List of RSS news
            directory (str): Directory where output will be saved
    """

    def __init__(self, title, entries, directory):
        self.title = title
        self.entries = entries
        self.directory = directory

    def _download_img(self, url, img_dir):
        """ Download image in DIRECTORY/images

            Returns:
                filename: image name
        """

        logging.info("Starting image download")

        filename = url.split('/')[-1]
        response = requests.get(url, allow_redirects=True)

        out_dir = Path(self.directory)

        if not out_dir.is_dir():
            logging.info("Creating directory /%s", out_dir)
            out_dir.mkdir()

        image_dir = out_dir / img_dir
        if not image_dir.is_dir():
            logging.info("Creating directory /%s", image_dir)
            image_dir.mkdir()

        with open(image_dir / filename, 'wb') as handler:
            handler.write(response.content)

        return filename

    def _replace_urls_to_local(self, entry):
        """ Replace img URLs in entry to local file path

            Args:
                entry (dict): News dict

        """
        soup = BeautifulSoup(entry.summary, "html.parser")
        imgs = [img['src'] for img in soup.findAll('img') if img.has_attr('src')]
        for img in imgs:
            filename = self._download_img(img, IMAGE_DIR)
            downloaded_img_local_path = Path(IMAGE_DIR / filename)
            entry.summary = entry.summary.replace(img, str(downloaded_img_local_path))

        return entry

    def _replace_urls_to_absolute(self, entry):
        """ Replace img URLs in entry to local absolute file path

            Special for pdfkit (pdfkit support only absolute file path)

            Args:
                entry (dict): News dict
        """
        soup = BeautifulSoup(entry.summary, "html.parser")
        imgs = [img['src'] for img in soup.findAll('img') if img.has_attr('src')]
        for img in imgs:
            filename = self._download_img(img, TEMP_IMAGE_DIR)
            downloaded_img_absolute_path = Path(self.directory / TEMP_IMAGE_DIR / filename).absolute()
            entry.summary = entry.summary.replace(img, str(downloaded_img_absolute_path))

        return entry

    def _gen_html(self, absolute_urls=False):
        """ Generates HTML

            Args:
                absolute_urls (bool): Should we generate HTML with absolute URLs (to convert to PDF)?

            Returns:
                html: String with HTML code
        """
        template = '''<html>
            <head>
                <meta charset="utf-8">
                <title>{{title}}</title>
                
                <style type=text/css>  
                    div 
                    { 
                      margin: 50px; 
                      font-size: 20px; 
                    } 
                </style> 
            </head>
            <body>
                {% for entry in entries %}
                    <div class='entry'>
                        <h2 class='title'>{{entry.title}}</h2>
                        <p><span class='date'>{{entry.published}}</span></p>
                        <a class='link' href='{{entry.link}}'>{{entry.title}}</a>
                        <br>
                        <div class='description'>{{entry.summary}}</div>
                    </div>
                {% endfor %}
            </body>
        </html>'''
        if absolute_urls:
            entries = [self._replace_urls_to_absolute(entry) for entry in self.entries]
        else:
            entries = [self._replace_urls_to_local(entry) for entry in self.entries]

        html = Template(template).render(title=self.title, entries=entries)
        return html

    def rss_to_html(self):
        """ Generate HTML file in DIRECTORY """
        html = self._gen_html()
        with open(Path(self.directory) / 'out.html', 'w') as file_object:
            file_object.write(html)

    def rss_to_pdf(self):
        """ Generate PDF file in DIRECTORY """
        html = self._gen_html(absolute_urls=True)
        options = {'quiet': ''}
        pdfkit.from_string(html, Path(self.directory) / 'out.pdf', options=options)
        # Delete temp DIRECTORY/TEMP_IMAGE_DIR
        temp_img_dir = Path(self.directory / TEMP_IMAGE_DIR)
        logging.info("Cleaning up %s", temp_img_dir)
        shutil.rmtree(temp_img_dir)
