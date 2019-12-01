from setuptools import setup, find_packages
from os import path
here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.txt'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = "rss_read",
    version = "0.0.1",
    author = "Kseniya Chystova",
    author_email = "lublubulbu@gmail.com",
    description = ("A simple reader for rss format"),
    long_description=long_description,
    keywords = ("rss", "parsing"),
    packages=find_packages()
   
)