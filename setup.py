import setuptools

with open("README.md") as readme_stream:
    description = readme_stream.read()

setuptools.setup(
    name="rss-reader",
    version=2.0,
    author="Gulida Marta",
    author_email="gulidamarta@gmail.com",
    description="RSS-reader, which can help you to read news "
                "from the source you will give it.",
    install_requires=['feedparser', 'bs4', 'lxml', 'requests'],
    packages=setuptools.find_packages(),
    include_package_data=True,
    python_requires='>=3.6',
    entry_points={
        'console_scripts': ['rss-reader=rss_reader.rss_reader:main'],
    }
)
