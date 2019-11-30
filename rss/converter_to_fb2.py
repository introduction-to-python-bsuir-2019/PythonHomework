"""This module converts news to fb2 format and saves."""

import os
import logging
from base64 import b64encode
import xml.etree.ElementTree as tree
from xml.etree.ElementTree import Element
import xml.dom.minidom as minidom

import requests


class Fb2Converter:
    """Class provides work with conversation to fb2."""

    def __init__(self, path='rss-news.fb2'):
        logging.info('Fb2Converter initialization')
        self.path = path
        self.root = tree.Element('FictionBook')
        self.root.set('xmlns:l', "http://www.w3.org/1999/xlink")
        self.description = tree.SubElement(self.root, 'description')
        self.body = tree.SubElement(self.root, 'body')

    def insert_file_description(self):
        """Insert file description."""

        logging.info('Insert description')
        title_info = tree.SubElement(self.description, 'title-info')
        tree.SubElement(title_info, 'book-title').text = 'RSS news'

    def insert_body(self, list_of_news, limit):
        """Insert body."""

        logging.info("Insert body")
        for news in list_of_news[:limit]:
            self.insert_section(news)

    def insert_section(self, news):
        """Insert section."""

        logging.info('Insert describing single news section')
        section = tree.SubElement(self.body, 'section')

        self.insert_tag_p(section, news['title'], True)
        self.insert_tag_empty_line(section)
        self.insert_tag_p(section, 'Link: ' + news['link'])
        self.insert_tag_p(section, 'Date: ' + news['date'])
        self.insert_tag_empty_line(section)

        if news['description']['images']:
            try:
                for img in news['description']['images']:
                    self.insert_image(section, img['src'], img['alt'])
            except Exception as e:
                print("Errors with images: ", e)

        self.insert_tag_empty_line(section)
        self.insert_tag_p(section, news['description']['text'])

        if news['description']['links']:
            self.insert_tag_empty_line(section)
            self.insert_tag_p(section, 'Links:')
            for link in news['description']['links']:
                self.insert_tag_p(section, link)

        self.insert_tag_empty_line(section)
        self.insert_tag_p(section, '-'*50)

    def insert_tag_empty_line(self, parent):
        """Insert empty line """

        logging.info('Insert empty line')
        tree.SubElement(parent, 'empty-line')

    def insert_tag_p(self, parent, text, strong_mode=None):
        """
        Insert tag p with text.
        If strong_mode then text will be bold.
        """

        if strong_mode:
            logging.info('Insert tag p with ')
            tag_p = tree.SubElement(parent, 'p')
            tree.SubElement(tag_p, 'strong').text = text
        else:
            logging.info('Insert tag p')
            tree.SubElement(parent, 'p').text = text

    def convert_to_fb2(self, news, limit=None):
        """Return news converted into fb2."""

        logging.info('Start conversion to fb2')
        self.insert_file_description()
        self.insert_body(news, limit)

    def save_fb2(self):
        """Save fb2 converted news on the received path."""

        logging.info('Save fb2 converted news')
        with open(self.path, 'w') as file:
            file.write(tree.tostring(self.root).decode('UTF-8'))

        pretty_xml_as_string = minidom.parse(self.path).toprettyxml()

        with open(self.path, 'w') as file:
            file.write(pretty_xml_as_string)

    def insert_image(self, parent, img_url, img_name):
        """Insert image tag in format: <image l:href="#{img_name}"/>."""

        logging.info('Insert image')
        image = tree.SubElement(parent, 'image')
        image.set('l:href', '#' + img_name)
        binary = tree.SubElement(self.root, 'binary')
        binary.set('id', img_name)
        binary.set('content-type', 'image/png')
        binary.text = self.get_binary_img(img_url)

    def get_binary_img(self, src):
        """Return img as base64 in string form"""

        logging.info('Get binary img')
        resource = requests.get(src)
        return b64encode(resource.content).decode('UTF-8')
