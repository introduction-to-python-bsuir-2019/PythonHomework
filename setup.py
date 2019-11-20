from setuptools import setup

from rssreader import conf

setup(
    name=conf.__package__,
    version=conf.__version__,
    description="CLI utility to process RSS",
    long_description="Simple command-line utility which works with news in RSS format",
    license='MIT',
    author="Andrei Puzanau",
    author_email="puzanov.a.a@gmail.com",
    packages=[conf.__package__],
    package_dir={conf.__package__: 'rssreader'},
    package_data={conf.__package__: ['data/*.*']},
    python_requires='>=3.8',
    install_requires=['feedparser', 'bs4', 'termcolor'],
    entry_points={
        'console_scripts':
            ['rss-reader = %s.cmd:main' % conf.__package__]
        }
)
