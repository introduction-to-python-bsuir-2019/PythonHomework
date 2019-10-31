from setuptools import setup
from rssreader import conf

setup(
    name=conf.__package__,
    version=conf.__version__,
    description="CLI utility to process RSS",
    long_description="Simple command-line utility which works with news in RSS format",
    author="Andrei Puzanau",
    author_email="puzanov.a.a@gmail.com",
    packages=[conf.__package__],
    install_requires=[
        "feedparser==5.2.1",
        "bs4==0.0.1",
        "typing"
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts':
            ['rss-reader = %s.cmd:main' % conf.__package__]
        }
)
