from os import path
from setuptools import setup, find_packages

HERE = path.abspath(path.dirname(__file__))
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name='rss-reader',
    version='0.3.0',
    description='A simple Python3.8 rss reader',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='https://github.com/introduction-to-python-bsuir-2019/PythonHomework',
    author='DiSonDS',
    author_email='dison.ds@gmail.com',
    keywords='simple rss reader',
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=['feedparser>=6.0.0b1', 'requests', 'bs4', 'colorama', 'jinja2', 'pdfkit'],
    entry_points={
        'console_scripts': [
            'rss-reader=rss_reader.__main__:main',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/introduction-to-python-bsuir-2019/PythonHomework/issues',
        'Source': 'https://github.com/introduction-to-python-bsuir-2019/PythonHomework',
    },
)
