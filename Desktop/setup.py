from setuptools import setup, find_packages

DESCRIPTON = 'RSS reader is a command-line utility, \
which receives RSS URL and prints results in human-readable format.'

setup(
    name='rssreader',
    version='4.0',
    description=DESCRIPTON,
    url='#',
    author='KozachenkoKirill',
    author_email='mr.elaskin@mail.ru',
    license='EPAM-Introduction-to-Python-2019',
    packages=find_packages(),
    package_dir={'rssreader': 'rssreader'},
    include_package_data=True,
    package_data={'': ['FreeSans.ttf', 'rss_reader.log', 'news.db',]},
    python_requires='>=3.6',
    install_requires=['feedparser', 'bs4', 'lxml', 'fpdf', 'sqlparse', 'termcolor', 'image'],
    entry_points={'console_scripts' : ['rss-reader = rssreader.main:main']},
    zip_safe=False
)
