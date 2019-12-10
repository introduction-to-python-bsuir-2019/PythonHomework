from pathlib import Path
import os
import logging
from base64 import b64encode
from xml.etree.ElementTree import ElementTree, Element, SubElement

import requests
import jinja2


class FormatsConverter:
    """Class for convert feed in html and fb2 formats"""
    def __init__(self):
        self.logger = logging.getLogger('rss_reader.FormatsConverter')

    def convert_to_html(self, feed, file_path, limit):
        self.logger.info("Converting feed to html")
        """Convert feed in html format and write to file_path"""
        articles = ''
        html_feed = '''\
        <html>
            <head>
                <title>{title}</title>
            </head>
            <body>
              {articles}
            </body>
        </html>'''
        article_template = '''\
        <div>
            <h2>{{ article_title }}</h2>
            <h4>{{ article_date }}</h4>
            <a href="{{article_link}}" target="_blank">Original article</a>
            {% for image in images %}
                <div><a href="{{ image['source'] }}" target="_blank">\
                         <img src="data:image/jpeg;base64,{{ image['binary'] }}" alt="{{ image['description'] }}"\
                              style="width: 400; height: 300; border: 1;">\
                     </a></div>
            {% endfor %}
            <p>{{ content }}<p>
            <div>
                <h4>Links:</h4>
                <ul>
                    {% for link in links %}
                        <li><a href="{{ link }}" target="_blank">{{ link }}</a></li>
                    {% endfor %}
                </ul>
            </div>
        </div>'''
        jtemplate = jinja2.Template(article_template)
        self.logger.info("Processing articles")
        for article in feed['articles'][:limit]:
            images = []
            for image in article.media['images']:
                bin_image = self._handle_image(image['source_url'])
                images.append({'description': image['description'], 'binary': bin_image, 'source': image['source_url']})
            articles += jtemplate.render(article_date=article.date.date(),
                                         article_title=article.title,
                                         article_link=article.link,
                                         images=images,
                                         content=article.content,
                                         links=article.media['links'])

        self.html_feed = html_feed.format(title=feed['feed_name'], articles=articles)
        self.logger.info(f"Write feed to html file {file_path}")
        with open(file_path, 'w') as html_file:
            html_file.write(self.html_feed)

    def convert_to_fb2(self, feed, file_path, limit):
        """Convert feed in fb2 format and write to file_path"""
        self.logger.info("Converting feed to fb2")
        fbook = Element('FictionBook')
        fbook.set('xmlns', 'http://www.gribuser.ru/xml/fictionbook/2.0')
        fbook.set('xmlns:l', 'http://www.w3.org/1999/xlink')

        description = SubElement(fbook, 'description')

        title_info = SubElement(description, 'title-info')
        SubElement(title_info, 'genre').text = feed['feed_name']
        author = SubElement(title_info, 'author')
        SubElement(author, 'first_name').text = 'RSS reader'
        SubElement(title_info, 'book-title').text = feed['feed_name']

        document_info = SubElement(description, 'document-info')
        SubElement(document_info, 'program-used').text = 'rss_reader v 4.0'
        SubElement(document_info, 'version').text = '1.0'

        body = SubElement(fbook, 'body')

        self.logger.info("Processing articles")
        image_counter = 0
        for art_num, article in enumerate(feed['articles'][:limit]):
            fb_article = SubElement(body, 'section')
            fb_article.set('id', str(art_num))
            title = SubElement(fb_article, 'title')
            SubElement(title, 'p').text = article.title
            date = SubElement(fb_article, 'p')
            SubElement(date, 'emphasis').text = article.date.strftime("%d-%m-%Y")
            lnk = SubElement(fb_article, 'p')
            source_link = SubElement(lnk, 'a')
            source_link.text = 'Original article\n'
            source_link.set('l:href', article.link)

            for image in article.media['images']:
                fb_image = SubElement(fb_article, 'image')
                fb_image.set('l:href', f'#picture-{image_counter}.jpg')
                binary = SubElement(fbook, 'binary')
                binary.set('id', f'picture-{image_counter}.jpg')
                binary.set('content-type', 'image/jpeg')
                binary.text = self._handle_image(image['source_url'])
                image_counter += 1
            SubElement(fb_article, 'p').text = '\n' + article.content
            links = SubElement(fb_article, 'p')
            links.text = 'Links:\n'
            if article.media['links']:
                for link in article.media['links']:
                    fb_link = SubElement(links, 'a')
                    fb_link.set('l:href', link)
                    fb_link.text = link
            else:
                links.text += 'No links'

        fbook_r = ElementTree(fbook)
        self.logger.info(f"Write feed to fb2 file {file_path}")
        with open(file_path, 'wb') as fb2_file:
            fbook_r.write(fb2_file)

    def _handle_image(self, image_url):
        """Download image from image_url and return image base64 binary"""
        self.logger.info(f"Download image {image_url}")
        try:
            image = requests.get(image_url)
        except Exception:
            self.logger.warning('Image not founded.')
        else:
            return b64encode(image.content).decode()
