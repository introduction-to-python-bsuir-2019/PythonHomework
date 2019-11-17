from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='rss-reader',
    version='0.2.0',
    description='A simple Python3.8 rss reader',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/introduction-to-python-bsuir-2019/PythonHomework',
    author='Dydyshko Andrey',
    author_email='dydyshko1999@gmail.com',
    keywords='simple rss reader',
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=['feedparser>=6.0.0b1', 'requests', 'bs4'],
    entry_points={
        'console_scripts': [
            'rss-reader=app.__main__:main',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/introduction-to-python-bsuir-2019/PythonHomework/issues',
        'Source': 'https://github.com/introduction-to-python-bsuir-2019/PythonHomework',
    },
)