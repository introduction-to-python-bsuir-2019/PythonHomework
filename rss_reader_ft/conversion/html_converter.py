"""Module contains objects related to HTML"""
import logging
from typing import Dict, Any

from rss_reader_ft.conversion.format_converter import FormatConverter


class HtmlConverter(FormatConverter):
    """
    HtmlConverter class
    inherited from FormatConverter abstract class.
    """
    def __init__(self, rss_feed_dict: Dict[str, Any]):
        """Init HtmlConverter class"""
        self.convert_data: Dict[str, Any] = rss_feed_dict

    def convert_to_format(self) -> str:
        """Сonversion method to HTML format"""
        logging.info('Convert data to HTML and return it')

        html: str = """
            <!DOCTYPE HTML>
            <html>
             <head>
              <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
              <title>News feed</title>
             </head>
             <body>
              <table width="600" align="center">
        """

        html += f'<caption><h1>{self.convert_data["Feed"]} <a href={self.convert_data["Url"]}>Ссылка</a></h1></caption>'

        for entry in self.convert_data["News"]:
            html += '<tr><td>'
            html += f'\n<h3><p align="center">{entry["Title"]}</p></h3>'
            html += f'<p align="center"><a href={entry["Link"]}>Ссылка на статью</a></p>'
            for count, img_link in enumerate(entry["Links"]["Img_links"]):
                html += f'<p><img src=\'{img_link}\' width="600" height="400"></p>'
            html += f'<p>Date: {entry["Date"]}</p>'
            html += f'<p>{entry["Description"]}\n</p>'
            html += '</td></tr>'

        html += '</table></body></html>'
        return html
