import setuptools

setuptools.setup(
    name="Pure Python command line rss-reader",
    version=2.0,
    author="Gulida Marta",
    author_email="gulidamarta@gmail.com",
    description="RSS-reader, which can help you to read news "
                "from the source you will give it.",
    install_requires=['feedparser', 'bs4', 'lxml', 'Reader'],
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    entry_points={
        'console_scripts': ['reader=rss_reader:main'],
    }
)
