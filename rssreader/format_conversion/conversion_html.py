"""Html conversion module"""

import logging


class HtmlConversion():
    """A class that converts to HTML"""
    def __init__(self, list_news_dict: list) -> None:
        self.list_news_dict = list_news_dict

    def conversion_to_html(self) -> list:
        """Method that converts a dictionary to html"""
        result_news = []
        current_news = []
        template = '<!DOCTYPE HTML><html><head>\
            <meta http-equiv="Content-Type" content="text/html;charset=utf-8">\
            <title>News feed</title>\
            </head><body><table width="600" align="center">'
        result_news.append(template)

        for news in self.list_news_dict:
            feed_html = f'<caption><h1>{news["Feed"]}</h1></caption>'
            current_news.append(feed_html)
            current_news.append('<tr><td>')
            current_news.append(
                f'\n<h3><p align="center">{news["Title"]}</p></h3>')
            current_news.append(
                f'<p align="center">\
                <a href={news["Link"]}\
                style="color:#800080">News Link</a></p>')
            current_news.append(
                f'<p style="color:#008000">Date: {news["Date"]}</p>')

            for link in news["Links"]:
                current_news.append(
                    f'<p><img src=\'{link}\' width="600" height="400"></p>')

            current_news.append(f'<p>{news["Description"]}\n</p>')
            current_news.append('</td></tr>')
            result_news.append("".join(current_news))

            current_news.clear()
        result_news.append('</table></body></html>')

        logging.info("News converted to html")

        return "".join(result_news)

    def save_html_news(self, news) -> None:
        """Method that saves html file"""
        with open("parsing_news.html", "w") as wf:
            wf.write(news)
        logging.info("File html saved successfully")
