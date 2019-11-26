import setuptools

setuptools.setup(
    name="rss-reader-euseand",
    version="0.24",
    author="Yevgeny Semak",
    author_email="euseand@gmail.com",
    url="https://github.com/euseand/PythonHomework/tree/FinalTask/FinalTask",
    description=("Basic rss-reader working in command prompt."),
    keywords="rss-reader",
    install_requires=['feedparser', 'bs4'],
    packages=setuptools.find_packages(),
    python_requires='>=3.8',
    entry_points={
        'console_scripts': ['rss-reader=rss_reader.rss_reader:main'],
    }

)