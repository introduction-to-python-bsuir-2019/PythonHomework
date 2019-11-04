from setuptools import setup, find_packages

with open('README.md', 'r') as file:
    long_description = file.read()


setup(
    name='news-feed',
    version='0.2',
    description='News aggregator',
    long_description=long_description,
    long_description_content_type='text/markdown',

    py_modules=['news_feed.rss_reader'],
    author='Vadim Titko',
    author_email='Vadbeg@tut.by',
    url='https://github.com/Vadbeg/news_feed_reader',

    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],

    entry_points={
        'console_scripts': [
            'rss_reader = news_feed.rss_reader:main'
        ]
    },

    install_requires=['lxml>=4.3.0', 'dateutil', 'requests', 'pandas'],
    python_requires='>=3.6'
)

