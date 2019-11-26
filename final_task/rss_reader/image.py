"""
This module provides tools for working with images
"""
import os
import requests


class Image:
    """
    This class represents information about image like link and alternative text
    """

    def __init__(self, link, alt):
        self.link = link
        self.alt = alt

    def to_json(self):
        """
        This method converts Image object to JSON
        :return: dict
        """
        return {'link': self.link, 'alt': self.alt}

    @staticmethod
    def from_json(json_obj):
        """
        This method gets Image object from JSON
        :param json_obj: dict
        :return: Image class instance
        """
        if json_obj:
            return Image(json_obj.get('link', ''), json_obj.get('alt', ''))

    def download(self, dest, name):
        """
        This methods downloads image from Internet to 'dest' folder by name 'name'
        :param dest: destination folder (str)
        :param name: result file name (str)
        :return: path to result file (str)
        """
        path = os.path.join(dest, name)
        resource = requests.get(self.link)
        with open(path, 'wb') as img:
            img.write(resource.content)
        return path
