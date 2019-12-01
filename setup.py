from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='rss-reader',
    version='0.4.0',
    description='A simple Python3.8 rss reader',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/introduction-to-python-bsuir-2019/PythonHomework',
    author='ge2nadiy',
    author_email='ge2nadiy.k@gmail.com',
    keywords='simple rss reader',
    packages=find_packages(),
    package_data={
        'rss_app': [
            'fonts/ttf/DejaVuSansCondensed.ttf'
        ]
    },
    python_requires='>=3.8',
    install_requires=['bs4', 'feedparser', 'requests', 'python-dateutil', 'httplib2', 'fpdf', 'colorama'],
    entry_points={
        'console_scripts': [
            'rss-reader=rss_app.main:main',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/introduction-to-python-bsuir-2019/PythonHomework/issues',
        'Source': 'https://github.com/introduction-to-python-bsuir-2019/PythonHomework',
    },
)
