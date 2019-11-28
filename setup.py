from setuptools import setup, find_packages
import reader

setup(
    name='reader',
    packages=find_packages(),
    install_requires=["argparse", "beautifulsoup4", "lxml"],
    entry_points={
        'console_scripts':
            ["rss-reader = reader.rss:main"]
    }
)
