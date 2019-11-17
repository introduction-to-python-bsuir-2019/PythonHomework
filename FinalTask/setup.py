import setuptools

setuptools.setup(
    name="euseand's rss-parser",
    version="0.1",
    author="Yevgeny Semak",
    author_email="euseand@gmail.com",
    url="https://github.com/euseand/PythonHomework/tree/FinalTask/FinalTask",
    description=("Basic rss-reader working in command prompt."),
    keywords="rss-reader",
    install_requires=['feedparser', 'bs4', 'rss_parser'],
    packages=setuptools.find_packages(),
    python_requires='>=3.8',
    entry_points={
        'console_scripts': ['rss-reader=rss_reader.rss_reader:main'],
    }

)