import os
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='rss_reader',
    version='1.1',
    description='A useful module',
    license="MIT",
    author='Varabei Kanstantsin',
    author_email='vorobeybird@gmail.com',
    url='https://github.com/introduction-to-python-bsuir-2019/PythonHomework/pull/48',
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=['feedparser>=6.0.0b1','argparse','requests','bs4','json2html','lxml','Pillow'],
                      
    entry_points = {
        'console_scripts': ['rss_reader=Rssreader.rss_reader:Main'],
    }
)
