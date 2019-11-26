"""
This module provides tools for working with OS
"""
import os
from pathlib import Path
from inspect import currentframe, getframeinfo


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
    return os.path.dirname(__file__)  #Path(getframeinfo(currentframe()).filename).resolve().parent
