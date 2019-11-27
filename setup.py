from setuptools import setup, find_packages

with open('README.md', 'r') as file:
    long_description = file.read()


setup(
    name='news-feed',
    version='0.2',
    description='News aggregator',
    long_description=long_description,
    long_description_content_type='text/markdown',
    # package_dir={'': 'news_feed'},

    py_modules=['news_feed.rss_reader', 'news_feed.format_converter'],
    author='Vadim Titko',
    author_email='Vadbeg@tut.by',
    url='https://github.com/Vadbeg/news_feed_reader',

    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],

    package_data={'news_feed': ['news_feed/fonts/arial.ttf', 'news_feed/req.txt']},
    include_package_data=True,

    entry_points={
        'console_scripts': [
            'rss_reader = news_feed.rss_reader:main'
        ]
    },

    install_requires=['lxml>=4.3.0', 'requests',
                      'colorama', 'Pillow',
                      'PyPDF2', 'Django',
                      'xhtml2pdf', 'fpdf'],
    python_requires='>=3.6'
)
