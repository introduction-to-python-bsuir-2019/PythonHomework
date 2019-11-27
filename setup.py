from setuptools import setup, find_packages

from rss_reader_ft import config

setup(
    name=config.__package__,
    version=config.__version__,
    description="One-shot command-line RSS reader",
    long_description="RSS reader should be a command-line utility which receives RSS URL \
                      and prints results in human-readable format.",
    author="Vlad Bubeniuk",
    author_email="zaybyst@mail.ru",
    packages=find_packages(),
    python_requires='>=3.8',
    url="https://github.com/ZayJob/PythonHomework/tree/finalTask",
    install_requires=["bs4", "feedparser", "pymongo"],
    entry_points={
        'console_scripts':
            ['rss-reader = rss_reader_ft.__main__:main']
    }
)
