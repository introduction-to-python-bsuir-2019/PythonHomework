from setuptools import setup, find_packages
from rssreader import cnf

setup(
    name=cnf.__package__,
    version=cnf.__version__,
    description="One-shot command-line RSS reader",
    long_description="All information in the documentation",
    author="Nikita Koznev",
    author_email="nikitakoznev@gmail.com",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "bs4", "feedparser", "nose", "pymongo", "coverage",
        "fpdf", "requests", "colored"],
    entry_points={
        "console_scripts":
            [f"{cnf.__package__} = rssreader.__main__:main"]
        }
)
