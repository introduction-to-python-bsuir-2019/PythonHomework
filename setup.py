import setuptools
from rss_reader import version

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name = "rss-reader", 
    version = version.version,
    author = "Alex Birillo",
    author_email = "tempbeerlover@gmail.com",
    description = "A simple command-line RSS reader",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "",
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={  

        'console_scripts': [

            'rss_reader = rss_reader.rss_reader:main',

        ],

    },
    install_requires=['feedparser', 'argparse'],
    python_requires='>=3.7',
)
