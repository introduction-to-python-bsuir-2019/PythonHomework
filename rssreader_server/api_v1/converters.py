"""
Module for output the result of the utility and printing in different formats.
Recommend use only class OutputController with parameters:
    * to_json: bool - output in JSON or not
    * to_pdf: str - string filename for output
    * to_html: str - string filename for output
Default start sample output.

"""
import json
import os
from abc import ABC

from fpdf import FPDF
from requests import get

__all__ = ['SamplePrintResponseConverter', 'JSONPrintResponseConverter',
           'PDFPrintResponseConverter', 'HTMLPrintResponseConverter']


class BaseResponseConverter(ABC):
    cache_folder = '__cache__'

    def print(self, articles, filename, **kwargs):
        """
        Procedure for output of news articles.

        :param articles: dict with title and list of news articles
        :param filename: name of the file output
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


class SamplePrintResponseConverter(BaseResponseConverter):
    """
    Class controller for sample output in standard out.
    """
    delimiter = "#" * 80

    def print(self, articles, filename, **kwargs):
        """
        Method for output of given articles if given filename.

        :param articles: articles for output in file
        :param filename: name of file to output
        :return: path to file with result
        :rtype: str
        """
        if (title := articles.get('title', None)) is not None:
            response_result = f"Feed: {title}\n"

        for article in articles['articles']:
            response_result += self._print_article(article)

        with open(os.path.join(self.cache_folder, filename), 'w') as file:
            file.write(response_result)

        return filename

    def _print_article(self, article, **kwargs):
        """
        Method for output articles in PDF format.

        :param article: current dict with article info for output
        :type dict
        """
        response_result = f"Title: {article['title']}\n" \
                          f"Date: {article['pubDate']}\n" \
                          f"Link: {article['link']}\n" \
                          f"\n" \
                          f"{article['dec_description']}\n" \
                          f"\n" \
                          f"Links:"

        for link in article['dec_links']:
            response_result += f"\n{link}"
        response_result += f"\n{self.delimiter}"

        return response_result


class JSONPrintResponseConverter(BaseResponseConverter):
    """
    Class controller for output JSON form of articles in standard out.
    """

    def print(self, articles, filename, **kwargs):
        """
        Method for output of given articles if given filename.

        :param articles: articles for output in file
        :param filename: name of file to output
        :return: path to file with result
        :rtype: str
        """
        with open(os.path.join(self.cache_folder, filename), 'w') as file:
            file.write(json.dumps(articles))

        return filename


class PDFPrintResponseConverter(BaseResponseConverter):
    """
    Class controller for output given articles in PDF in file.
    """
    image_ext = 'jpg'
    cache_folder = "__cache__"
    extension = '.pdf'
    delimiter_before = "_" * 59
    delimiter_after = "%d".rjust(55, '_').ljust(59, '_')

    def print(self, articles, filename, **kwargs):
        """
        Method for output of given articles if given filename.

        :param articles: articles for output in file
        :param filename: name of file to output
        :return: path to file with result
        :rtype: str
        """
        writer = FPDF()
        writer.add_page()
        self._print_title(articles['title'], writer=writer)

        for i, article in enumerate(articles['articles']):
            self._print_article(article, writer=writer, ind=i)

        writer.output(os.path.join(self.cache_folder, filename))

        # os.removedirs(self.cache_folder)

        return filename

    def _print_title(self, title, **kwargs):
        """
        Method for output title of RSS Feeds.

        :param title: title of RSS Feed
        :rtype: dict
        """
        writer = kwargs['writer']
        writer.set_font('Courier', 'B', 20)
        writer.multi_cell(0, 30, title, align='C')

    def _print_article(self, article, **kwargs):
        """
        Method for output articles in PDF format.

        :param article: current dict with article info for output
        :type dict
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


class HTMLPrintResponseConverter(BaseResponseConverter):
    """
    Class controller for output given articles using HTML in file.
    """
    extension = '.html'

    def print(self, articles, filename, **kwargs):
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

        with open(os.path.join(self.cache_folder, filename), 'w') as file:
            file.write(html_text)

        return filename

    def _print_article(self, article, **kwargs):
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
