from setuptools import setup

from rss_reader_ft.app import rss_reader_config

setup(
    name=rss_reader_config.__package__,
    version=rss_reader_config.__version__,
    description="One-shot command-line RSS reader",
    long_description="RSS reader should be a command-line utility which receives RSS URL \
                      and prints results in human-readable format.",
    author="Vlad Bubeniuk",
    author_email="zaybyst@mail.ru",
    packages=[rss_reader_config.__package__],
    python_requires='>=3.8',
    url="https://github.com/ZayJob/PythonHomework/tree/finalTask",
    entry_points={
        'console_scripts':
            ['rss-reader = %s.rss_reader:main' % rss_reader_config.__package__]
    }
)
