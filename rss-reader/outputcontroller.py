"""
Module for output the result of the utility and printing in different formats.
Recommend use only class OutputController with parameters:
    * to_json: bool - output in JSON or not
    * to_pdf: str - string filename for output
    * to_html: str - string filename for output
    * colorize: bool - print the result in colorized mode
Default start sample output.

"""
import json
import logging
import os
from abc import ABC

from colorama import init, Style, Fore
from fpdf import FPDF
from requests import get

# Initialization colorama for colorized output
init()

__all__ = ['OutputController']


class BaseController(ABC):
    """
    Abstract base class for all output controllers. Using such interface for all controllers.
    """

    def print_to(self, articles, **kwargs):
        """
        Procedure for output of news articles.

        :param articles: dict with title and list of news articles
        :param kwargs: optional params. Use to extend a count given params in base method
        :type articles: dict
        """

    def _print_article(self, article, **kwargs):
        """
        Method for output given articles in given PDF file.

        :param article: article to output
        :param kwargs: optional params. Use to extend a count given params in base method
        :type article: dict
        """

    def _print_title(self, title, **kwargs):
        """
        Method for output given title.

        :param title: title to output
        :param kwargs: optional params. Use to extend a count given params in base method
        :type title: str
        """


class SamplePrintController(BaseController):
    """
    Class controller for sample output in standard out.
    """

    def print_to(self, articles, **kwargs):
        """
        Procedure for sample output of news articles.

        :param articles: dict with title and list of news articles
        :param kwargs: optional params. Use to extend a count given params in base method
            colorize: bool - print the result of the utility in colorized mode
        :type articles: dict
        """
        logging.info("Start sample output")
        if (title := articles.get('title', None)) is not None:
            self._print_title(title, colorize=kwargs.get('colorize', False))

        for article in articles['articles']:
            self._print_article(article, colorize=kwargs.get('colorize', False))

    def _print_article(self, article, **kwargs):
        """
        Method for output given articles in standard out.

        :param article: articles to output
        :param kwargs: optional params. Use to extend a count given params in base method
            colorize: bool - print the result of the utility in colorized mode
        :type article: dict
        """

        if kwargs.get('colorize', False):
            output = "{}Title:{} %s\n" \
                     "{}Date: {}%s{}\n" \
                     "{}Link: {}%s{}\n" \
                     "\n" \
                     "%s\n" \
                     "\n" \
                     "{}Links:{}".format(Fore.BLUE, Style.RESET_ALL,
                                         Fore.BLUE, Fore.LIGHTYELLOW_EX, Style.RESET_ALL,
                                         Fore.BLUE, Fore.YELLOW, Style.RESET_ALL,
                                         Fore.BLUE, Style.RESET_ALL)
            format_link = "{}%s{}"
        else:
            output = "Title: %s\n" \
                     "Date: %s\n" \
                     "Link: %s\n" \
                     "\n" \
                     "%s\n" \
                     "\n" \
                     "Links:"
            format_link = "%s"

        print(output % (article['title'], article['pubDate'], article['link'], article['dec_description']))

        for link in article['dec_links']:
            params = (Fore.YELLOW, Style.RESET_ALL) if link.endswith('(link)') else (Fore.GREEN, Style.RESET_ALL)
            print((format_link % link).format(*params))
        print('################################################################################')

    def _print_title(self, title, **kwargs):
        """
        Method for output given articles in given PDF file.

        :param title: title to output
        :param kwargs: optional params. Use to extend a count given params in base method
            colorize: bool - print the result of the utility in colorized mode
        :type title: str
        """
        if kwargs.get('colorize', False):
            print(f"%sFeed: %s{title}%s\n" % (Fore.BLUE, Fore.LIGHTMAGENTA_EX, Style.RESET_ALL))
        else:
            print(f"Feed: {title}\n")


class JSONPrintController(BaseController):
    """
    Class controller for output JSON form of articles in standard out.
    """

    def print_to(self, articles, **kwargs):
        """
        Procedure for output articles in JSON format.

        :param articles: dict with title and list of news articles
        :param kwargs: optional params. Use to extend a count given params in base method
        :type articles: dict
        """
        logging.info("Converting all articles to JSON")
        data = json.dumps(articles)
        logging.info("Completed. Output JSON")
        print(data)


class PDFPrintController(BaseController):
    """
    Class controller for output given articles in PDF in file.
    """
    image_ext = 'jpg'
    cache_folder = "__cache__"
    extension = '.pdf'
    delimiter_before = "_" * 59
    delimiter_after = "%d".rjust(55, '_').ljust(59, '_')

    def print_to(self, articles, **kwargs):
        """
        Method for output given articles in given PDF file.

        :param articles: articles to output
        :param kwargs: optional params. Use to extend a count given params in base method.
            filename - name of output file
        :type articles: dict
        """
        print_to = kwargs.get('filename', None)
        if print_to is not None and not print_to.endswith(self.extension):
            print_to += self.extension

        writer = FPDF()
        writer.add_page()
        self._print_title(articles['title'], writer=writer)

        for i, article in enumerate(articles['articles']):
            self._print_article(article, writer=writer, ind=i)

        writer.output(print_to)

    def _print_title(self, title, **kwargs):
        """
        Method for output given articles in given PDF file.

        :param title: title to output
        :param kwargs: optional params. Use to extend a count given params in base method
            writer - FPDF object for output in PDF file
        :type title: str
        """
        writer = kwargs['writer']
        writer.set_font('Courier', 'B', 20)
        writer.multi_cell(0, 30, title, align='C')

    def _print_article(self, article, **kwargs):
        """
        Method for output one article in PDF.

        :param article: article to output
        :param kwargs: optional params. Use to extend a count given params in base method
            writer - FPDF object for output in PDF file
            ind - sequence number of article
        :type article: dict
        """
        writer = kwargs['writer']
        ind = kwargs['ind']

        article = self._clean_each_elem_article(article)

        writer.set_font("Courier", 'B', 15)
        writer.multi_cell(0, 10, self.delimiter_before)

        writer.set_font("Courier", "B", 13)
        writer.multi_cell(0, 7, f"Title: {article['title']}", align="L")

        writer.set_font("Courier", "BI", 11)
        writer.multi_cell(0, 10, f"Date: {article['pubDate']}", align='R')

        for img in article['media']:
            self._draw_image(writer, img)

        writer.set_font("Courier", size=12)
        writer.multi_cell(0, 5, article['description'], align='L')

        writer.set_font("Courier", "BI", size=9)
        writer.multi_cell(0, 10, f"Link: {article['link']}", align='L')

        writer.set_font("Courier", 'B', 15)
        writer.multi_cell(0, 10, self.delimiter_after % (ind + 1))

    def _clean_each_elem_article(self, elem):
        """
        Recursive method for cleaning errors with encoding 'latin-1' for output ready text in PDF file.
        Go throw all elements of given objects and remove error with encoding 'latin-1'.

        :param elem: current element for checking and removing errors with encoding
        :return: recursive call this method if givn object is collection, else string
        """
        if type(elem) == str:
            return elem.encode('latin-1', 'replace').decode('latin-1')
        elif type(elem) == dict:
            return {k: self._clean_each_elem_article(v) for k, v in elem.items()}
        elif type(elem) == list:
            return [self._clean_each_elem_article(el) for el in elem]

    def _draw_image(self, writer, image):
        """
        Method for draw image in file by given FPDF writer.

        :param writer: FPDF object for drawing in file
        :param image: dict with info about image
        :type writer: fpdf.FPDF
        :type image: dict
        """
        try:
            image_name = f"{image['src'].split('/')[-1]}.{self.image_ext}"
            image_path = self._download_to(image['src'], image_name)
            writer.image(image_path, type=self.image_ext, link=image['src'], x=(writer.w - 50) // 2)
        except (ValueError, TypeError, RuntimeError):
            writer.set_font("Courier", 'B', 10)
            writer.multi_cell(0, 3, f"NO IMAGE: {image['alt']}", align='C')

    def _download_to(self, link, filename):
        """
        Method for downloading image by link in given file. Return path to downloaded image.

        :param link: link to image
        :param filename: name of file, such will be rewriten.
        :type link: str
        :type filename: str
        :return: absolute path to downloaded image
        :rtype: str
        """
        if not os.path.exists(os.path.join(self.cache_folder)):
            os.mkdir(os.path.join(self.cache_folder))
        img_data = get(link).content
        ready_image_path = os.path.join(self.cache_folder, filename)
        with open(ready_image_path, 'wb') as handler:
            handler.write(img_data)

        return ready_image_path


class HTMLPrintController(BaseController):
    """
    Class controller for output given articles using HTML in file.
    """
    extension = '.html'

    def print_to(self, articles, **kwargs):
        """
        Method for output given articles in given file with HTML.

        :param articles: articles to output
        :param kwargs: optional params. Use to extend a count given params in base method.
            filename - name of output file
        :type articles: dict
        """
        print_to = kwargs.get('filename', None)
        if print_to is not None and not print_to.endswith(self.extension):
            print_to += self.extension

        html_text = f"<!DOCTYPE html>" \
                    f"<html>" \
                    f"<head>" \
                    f"<meta charset='utf-8'>" \
                    f"<title>RSS Feeds</title>" \
                    f"</head>" \
                    f"<body>" \
                    f"<h2 align=center>{articles['title']}</h2>" \
                    f"{''.join([self._print_article(art) for art in articles['articles']])}" \
                    f"</body>" \
                    f"</html>"

        with open(print_to, 'w') as file:
            file.write(html_text)

    def _print_article(self, article, **kwargs):
        """
        Method for output one article use HTML.

        :param article: article to output
        :param kwargs: optional params. Use to extend a count given params in base method
        :type article: dict
        :return: string with html version of given article
        :rtype: str
        """
        result = "<div style=\"background-color:lightblue; margin-bottom:20px;\">" \
                 "<h3 style=\"margin: 0;\">"
        result += '<a href="{}" style="text-decoration:None; color:Black; font-size:25px;">' \
                  '{} (Link to original)' \
                  '</a>' \
                  '</h3>'.format(article['link'], article['title'])
        for image in article['media']:
            attrs = " ".join([f"{k}=\"{v}\"" for k, v in image.items()])
            result += "<br>" \
                      "<img {}>".format(attrs)
        result += f'<p style="color: blue; font-size:20px;">' \
                  f'Published: {article["pubDate"]}' \
                  f'</p>'
        result += f'<p>' \
                  f'{article["description"]}' \
                  f'</p>' \
                  f'<br>' \
                  f'<p>' \
                  f'Links:' \
                  f'</p>'
        for i in range(len(article['dec_links'])):
            result += f'<a href="{article["links"][i]}" style="text-decoration:None;">' \
                      f'{article["dec_links"][i]}' \
                      f'</a>' \
                      f'<br>'
        result += "</div>"
        return result


class OutputController:
    """
    Main OutputController class such working with all controllers in this module.
    """

    @staticmethod
    def print(articles, to_pdf=None, to_html=None, to_json=False, colorize=False):
        """
        Method for the choice and run procedure of output given articles.
        The output method depends on a given parameters.
        HTML output - to_html = 'filename'
        PDF output - to_pdf = 'filename'
        JSON output - to_json = True
        Default start sample output.

        :param articles: articles for output
        :param to_pdf: filename for output in PDF
        :param to_html: filename for output using HTML
        :param to_json: Print given articles in JSON format
        :param colorize: Print result in colorized mode
        :type articles: dict
        :type to_pdf: str
        :type to_html: str
        :type to_json: bool
        :type colorize: bool
        """
        if to_html is not None:
            HTMLPrintController().print_to(articles, filename=to_html)
        if to_pdf is not None:
            PDFPrintController().print_to(articles, filename=to_pdf)

        if to_json:
            JSONPrintController().print_to(articles)
        else:
            SamplePrintController().print_to(articles, colorize=colorize)
