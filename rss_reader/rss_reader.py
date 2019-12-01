"""RSS-reader module"""

import re
import logging
import feedparser
import lxml.html
import lxml.html.clean

from tldextract import extract
from colorama import Fore, Back, Style

from news_cacher import NewsCacher
from json_formatter import NewsJsonFormatter
from pdf_converter import PDFConverter
from html_converter import HTMLConverter


class NewsReader:
    def __init__(self, link, limit, json, date, convert_to_pdf, convert_to_html):
        self.link = link
        self.limit = limit
        self.json = json
        self.hrefs = []
        self.news = []
        self.date = date
        self.json_object = NewsJsonFormatter()
        self.convert_to_pdf = convert_to_pdf
        self.convert_to_html = convert_to_html

        ext_site_name = extract(self.link)
        site_name = f'{ext_site_name.domain}.{ext_site_name.suffix}'
        
        self.cacher_object = NewsCacher('cached_news.json', site_name)

        self.DATE_KEYS = ['published', 'updated', 'pubDate']
        self.MEDIA_KEYS = ['media_thumbnail', 'media_content']

    def parse_url(self):
        """Get RSS xml-file from url"""
        logging.info('Get RSS XML-file from url')

        self.feed = feedparser.parse(self.link)
        self.parse_xml(self.feed.entries[:self.limit])

    def parse_xml(self, source):
        """Parse xml-file to news array"""
        logging.info('Parse XML-file to news array')

        for item in source:
            content = []
            pub_date = ''

            for key in self.DATE_KEYS:
                if key in item:
                    pub_date = key

            for key in self.MEDIA_KEYS:
                if key in item:
                    for element in item[key]:
                        content.append(element['url'])

            self.news.append({"title": self.clean_html_text(item.title), "date": item[pub_date], 
                "text": self.clean_html_text(self.strip_html_string(item.description)), "link": item.link.split('?')[0], "hrefs": content})

        if self.date == None:
            self.cacher_object.cache(self.news)

        if self.json is True:
            self.json_object.format(self.news)

        if self.convert_to_html == True:
            if self.date != None:
                try:
                    news = self.cacher_object.get_cached_news(self.date, self.limit)
                except ValueError:
                    logging.error("News for this date not found")
                    exit()
                except FileNotFoundError:
                    logging.error("Cache file not found")
                    exit()

                html = HTMLConverter(news, 'rss_reader_news')
            else:
                html = HTMLConverter(self.news, 'rss_reader_news')
            html.dump()
            print('HTML file created in current directory')

        if self.convert_to_pdf == True:
            if self.date != None:
                try:
                    news = self.cacher_object.get_cached_news(self.date, self.limit)
                except ValueError:
                    logging.error("News for this date not found")
                    exit()
                except FileNotFoundError:
                    logging.error("Cache file not found")
                    exit()

                pdf = PDFConverter(news, 'rss_reader_news')
            else:
                pdf = PDFConverter(self.news, 'rss_reader_news')
            
            pdf.dump()
            print('PDF file created in current directory')

    def print_news(self):
        """Print news to console"""
        logging.info('Print news to console')

        if self.date != None:
            try:
                news = self.cacher_object.get_cached_news(self.date, self.limit)
            except ValueError:
                logging.error("News for this date not found")
                exit()
            except FileNotFoundError:
                logging.error("Cache file not found")
                exit()

            if self.json is True:
                self.json_object.format(news)
                print(self.json_object)
            else:
                for element in news:
                    self.print_one_news(element)
                    print('\n'*5)
        elif self.json is True:
            print(self.json_object)
        else:
            for element in self.news:
                self.print_one_news(element)
                print('\n'*5)

    def print_one_news(self, element):
        """Print one news to console"""

        print(f'{Fore.YELLOW + Back.BLACK + Style.BRIGHT}Title:{Fore.GREEN + Back.BLACK} {element["title"]}')
        print(f'{Fore.YELLOW + Back.BLACK}Date: {Fore.RED + Back.BLACK} {element["date"]}')
        print(f'{Fore.YELLOW + Back.BLACK}Link: {Fore.CYAN} {element["link"]}')
        print(f'{Fore.YELLOW + Back.BLACK}News text:')
        print(f'{Fore.WHITE + Back.BLACK}{element["text"]}')
        print(f'{Fore.YELLOW + Back.BLACK}Hrefs:')
        for href in element["hrefs"]:
            print(f'{Fore.CYAN}| {href}')

    def strip_html_string(self, string):
        """Remove html tags from a string"""
        logging.info("Remove html tags from a string")

        strip_string = re.compile('<.*?>')
        return re.sub(strip_string, '', string)

    def clean_html_text(self, string):
        """Clean html string"""

        doc = lxml.html.fromstring(string)
        cleaner = lxml.html.clean.Cleaner(style=True)
        doc = cleaner.clean_html(doc)
        return doc.text_content()