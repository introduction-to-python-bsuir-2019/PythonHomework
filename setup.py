"""Utils to export CLI rss_reader module
using: 'python3 setup.py sdist bdist_wheel'
"""
import setuptools
from rss_reader.rss import PROG_VERSION

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rss-reader",  # Replace with your own username
    version=str(PROG_VERSION),
    author="Andrey Nenuzhny",
    author_email="nenuzhny85@gmail.com",
    description="Rss reader Epam task",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Nenu1985/PythonHomework",

    packages=setuptools.find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),

    install_requires=['attrs',
                      'bs4',
                      'dateutil',
                      'feedparser',
                      'fpdf',
                      'lxml',
                      'python-dateutil',
                      'terminaltables',
                      ],

    extras_require={  # Optional
        'tests': ['nose', 'coverage'],
    },

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
    ],

    zip_safe=False,
    python_requires='>=3.7',
)
