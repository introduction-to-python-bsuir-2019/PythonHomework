"""
This module provides tools for working with OS
"""
import os
import sys


def create_directory(path, name):
    """
    This function creates directory
    :param path: path to directory (str)
    :param name: new directory name (str)
    :return: path to directory (str)
    """
    if os.path.exists(path):
        path = os.path.join(path, name)
        if not os.path.exists(path):
            os.mkdir(path)
        return path


def get_project_directory_path():
    """
    This function returns path to project directory
    :return: str
    """
    return os.path.dirname(sys.argv[0])


def download_images(news_item, path_to_dir, item_index):
    """
    THis function downloads images from Internet
    :param news_item: NewsItem class instance
    :param path_to_dir: path to destination directory (str)
    :param item_index: news_item index in news object (int)
    :return: list of image paths (list)
    """
    img_path_list = []
    img_index = 0
    for img in news_item.content.images:
        img_path = img.download(path_to_dir, f'{str(item_index)}_{str(img_index)}.jpeg')
        img_path_list.append(img_path)
        img_index += 1
    return img_path_list
