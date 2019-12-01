import setuptools

setuptools.setup(
    name="rss-reader-euseand",
    version="0.414",
    author="Yevgeny Semak",
    author_email="euseand@gmail.com",
    url="https://github.com/euseand/PythonHomework/tree/FinalTask/FinalTask",
    description=("Basic rss-reader working in command prompt."),
    keywords="rss-reader",
    package_data={'fonts': ['rss_reader/fonts/ttf/*']},
    include_package_data=True,
    install_requires=['feedparser', 'bs4', 'fpdf', 'requests'],
    packages=setuptools.find_packages(),
    python_requires='>=3.8',
    entry_points={
        'console_scripts': ['rss-reader=rss_reader.rss_reader:main'],
    }

)