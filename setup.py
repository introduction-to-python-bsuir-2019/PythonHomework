import setuptools

setuptools.setup(
    name="rss-reader-kis",
    version="1.82",
    author="Anton Kiselevich",
    author_email="kiselevichanton@gmail.com",
    description="Simple command line rss-reader.",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=[
        'feedparser',
        'bs4'
    ],
    entry_points={
        'console_scripts': ['rss-reader=reader.main:main'],
    }
)
