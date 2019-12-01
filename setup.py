from setuptools import setup


setup(
    name="rssreader",
    version=1.3,
    description="Utility to read rss",
    long_description="CLI utility for rss reading",
    author="Vladislav Bakhmat",
    author_email="uservice589@gmail.com",
    packages=["rssreader"],
    install_requires=[
        "argparse==1.4.0",
        "bs4==0.0.1",
        "urllib3==1.25.7",
        "logger==1.4",
        "feedparser==5.2.1",
	"fpdf==1.7.2"
	"lxml==4.4.1"
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts':
            ['rss-reader = %s.rssreader:main' % "rssreader"]
        }
)