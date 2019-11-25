import json
import logging
import abc

import requests

__all__ = ['OutputController']


class BaseController(abc.ABC):
    def print_to(self, articles, **kwargs):
        """
        Method of processing articles and title. Without work with files
        """

    def _print_article(self, title):
        pass

    def _print_title(self, article):
        pass


class SamplePrintController(BaseController):
    def print_to(self, articles, **kwargs):
        """
        Procedure for sample output of news articles.

        :param articles: dict with title and list of news articles
        :type articles: dict
        """
        logging.info("Start sample output")
        if (title := articles.get('title', None)) is not None:
            self._print_title(title)

        for article in articles['articles']:
            self._print_article(article)

    def _print_article(self, article):
        print(f"Title: {article['title']}\n"
              f"Date: {article['pubDate']}\n"
              f"Link: {article['link']}\n\n"
              f"{article['dec_description']}\n\n"
              f"Links:")
        for link in article['dec_links']:
            print(link)
        print('################################################################################')

    def _print_title(self, title):
        print(f"Feed: {title}\n")


class JSONPrintController(BaseController):
    def print_to(self, articles, **kwargs):
        """
        Procedure for output articles in JSON format.

        :param articles: dict with title and list of news articles
        :type articles: dict
        """
        logging.info("Converting all articles to JSON")
        data = json.dumps(articles)
        logging.info("Completed. Output JSON")
        print(data)


class PDFPrintController(BaseController):
    pass


class HTMLPrintController(BaseController):
    extension = '.html'

    def print_to(self, articles, **kwargs):
        print_to = kwargs.get('filename', None)
        if print_to is not None and not print_to.endswith(self.extension):
            print_to += self.extension

        html_text = f"<!DOCTYPE html><html><head><meta charset='utf-8'><title>RSS Feeds</title></head>" \
                    f"<body><h2 align=center>{articles['title']}</h2>" \
                    f"{''.join([self._print_article(art) for art in articles['articles']])}</body></html>"

        with open(print_to, 'w') as file:
            file.write(html_text)

    def _print_article(self, article):
        result = "<div style=\"background-color:lightblue; margin-bottom:20px;\"><h3 style=\"margin: 0;\">"
        result += '<a href="{}" style="text-decoration:None; color:Black; font-size:25px;">{}(Link to original</a>' \
                  '</h3>'.format(article['link'], article['title'])
        for image in article['media']:
            attrs = " ".join([f"{k}=\"{v}\"" for k, v in image.items()])
            result += "<br><img {}>".format(attrs)
        result += f'<p style="color: blue; font-size:20px;">Published: {article["pubDate"]}</p>'
        result += f'<p>{article["description"]}</p><br><p>Links:</p>'
        for i in range(len(article['dec_links'])):
            result += f'{i + 1}) <a href="{article["links"][i]}" style=\"text-decoration:None; font-size:15px\">' \
                      f'{article["dec_links"][i]}</a><br>'
        result += "</div>"
        return result

    @staticmethod
    def _download_to(link, filename):
        img_data = requests.get(link).content
        with open(filename, 'wb') as handler:
            handler.write(img_data)
        return filename


class OutputController:
    @staticmethod
    def print(articles, to_pdf=None, to_html=None, to_json=False):
        if to_html is not None:
            HTMLPrintController().print_to(articles, filename=to_html)
        if to_pdf is not None:
            PDFPrintController().print_to(articles, filename=to_pdf)

        if to_json:
            JSONPrintController().print_to(articles)
        else:
            SamplePrintController().print_to(articles)
