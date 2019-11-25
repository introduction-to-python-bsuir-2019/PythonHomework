"""Module contains objects related to printing data"""
import logging
from typing import Dict, Any

from rss_reader_ft.conversion.json_converter import JsonConverter
from rss_reader_ft.conversion.html_converter import HtmlConverter


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
    def to_json_format(rss_feed_dict: Dict[str, Any]) -> None:
        """Output data to the console in JSON format"""
        logging.info('Print RSS feed in JSON format')

        json_data = JsonConverter(rss_feed_dict).convert_to_format()
        print(json_data)

    @staticmethod
    def to_html_format(rss_feed_dict: Dict[str, Any]) -> None:
        """Output data to the console in HTML format"""
        logging.info('Print RSS feed in HTML format')

        html_data = HtmlConverter(rss_feed_dict).convert_to_format()

        with open('News_feed.html', 'w') as fw:
            fw.write(html_data)
