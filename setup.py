from setuptools import setup, find_packages
setup(
    name="RSS-READER.py",
    version="0.1",
    packages=find_packages(include=["feedparser","feedparser.*"]),
    scripts=["finalTaskPart1.py"],
    install_requires=['feedparser']
)
