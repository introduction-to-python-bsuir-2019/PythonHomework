import setuptools
from rss_reader import version

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rss-reader", 
    version=version.__version__,
    author="Elia Onishchouk",
    author_email="elias0n@mail.ru",
    description="A simple command-line RSS reader",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/el0ny/PythonHomework",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={  

        'console_scripts': [

            'rss_reader = rss_reader.rss_reader:main',

        ],

    },
    install_requires=['feedparser', 'bs4'],
    python_requires='>=3.6',
)
