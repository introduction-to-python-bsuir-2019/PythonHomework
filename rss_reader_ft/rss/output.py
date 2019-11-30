"""Module contains objects related to printing data"""
import logging
from typing import Dict, Any

from colored import fore, style, back

from rss_reader_ft.conversion.json_converter import JsonConverter
from rss_reader_ft.conversion.html_converter import HtmlConverter
from rss_reader_ft.conversion.pdf_converter import PdfConverter


class Output:
    """PrintData class"""
    @staticmethod
    def to_rss_format(rss_feed_dict: Dict[str, Any]) -> None:
        """Output to the console"""
        logging.info('Print RSS feed')

        print(f'Feed: {rss_feed_dict["Feed"]}')
        for entry in rss_feed_dict["News"]:
            print(f'\nTitle: {entry["Title"]}')
            print(f'Date: {entry["Date"]}')
            print(f'Link: {entry["Link"]}\n')
            print(f'{entry["Description"]}\n')
            print(f'Links:\n[1] {entry["Links"]["Source_link"]} (link)')

            for count, img_link in enumerate(entry["Links"]["Img_links"]):
                print(f'[{count + 2}] {img_link} (image)')  # 2 this a shift

    @staticmethod
    def to_rss_format_colored(rss_feed_dict: Dict[str, Any]) -> None:
        """Output to the console with color"""
        logging.info('Print RSS feed')
        print(fore.GREEN + style.BOLD + f'Feed: {rss_feed_dict["Feed"]}' + style.RESET)
        for entry in rss_feed_dict["News"]:
            print(fore.LIGHT_BLUE + style.BOLD + '\nTitle: ' + style.RESET + style.BOLD + f'{entry["Title"]}' + style.RESET)
            print(fore.LIGHT_RED + style.BOLD + 'Date: ' + style.RESET + style.BOLD + f'{entry["Date"]}' + style.RESET)
            print(fore.LIGHT_BLUE + style.BOLD + 'Link: ' + style.RESET + style.BOLD + f'{entry["Link"]}\n' + style.RESET)
            print(style.BOLD + f'{entry["Description"]}\n' + style.RESET)
            print(fore.LIGHT_BLUE + f'Links:\n[1] {entry["Links"]["Source_link"]} (link)')

            for count, img_link in enumerate(entry["Links"]["Img_links"]):
                print(f'[{count + 2}] {img_link} (image)' + style.RESET)  # 2 this a shift

    @staticmethod
    def to_json_format(rss_feed_dict: Dict[str, Any]) -> None:
        """Output data to the console in JSON format"""
        json_data = JsonConverter(rss_feed_dict).convert_to_format()

        logging.info('Print RSS feed in JSON format')

        print(json_data)

    @staticmethod
    def to_html_format(rss_feed_dict: Dict[str, Any]) -> None:
        """Output data to HTML file"""
        html_data = HtmlConverter(rss_feed_dict).convert_to_format()

        logging.info('Print RSS feed in HTML file')

        with open('News_feed.html', 'w') as fw:
            fw.write(html_data)

    @staticmethod
    def to_pdf_format(rss_feed_dict: Dict[str, Any]) -> None:
        """Output data to PDF file"""

        logging.info('Print RSS feed in PDF file')

        PdfConverter(rss_feed_dict).convert_to_format()
