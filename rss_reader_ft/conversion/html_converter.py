"""Module contains objects related to JSON"""
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
        logging.info('Convert data to JSON and return it')

        html: str = """
            <!DOCTYPE HTML>
            <html>
             <head>
              <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
              <title>News feed</title>
             </head>
             <body>
              <table>
        """

        html += f'<caption>{self.convert_data["Feed"]} {self.convert_data["Url"]}</caption>'


        for entry in self.convert_data["News"]:
            html += '<tr><td>'
            html += f'\n<p>Title: {entry["Title"]}</p>'
            html += f'<p>Date: {entry["Date"]}</p>'
            html += f'<p>Link: {entry["Link"]}\n</p>'
            for count, img_link in enumerate(entry["Links"]["Img_links"]):
                html += f'<p><img src=\'{img_link}\' width="189" height="255"></p>'  # 2 this a shift
            html += f'<p>{entry["Description"]}\n</p>'
            html += f'<p>Links:\n[1] {entry["Links"]["Source_link"]} (link)</p>'
            html += '</td></tr>'

        html += '</table></body></html>'

        return html
