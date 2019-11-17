from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='RSSReader_Kiryl',
    version='0.2',
    url='https://github.com/KirylDv/PythonHomework/tree/FinalTask',
    packages=find_packages(),
    python_requires='>=3.6.8',
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # `pip` to create the appropriate form of executable for the target
    # platform.
    #
    # For example, the following would provide a command called `sample` which
    # executes the function `main` from this package when invoked:
    entry_points={  # Optional
        'console_scripts': ['rss-reader=rss_reader.py:main'],
    },
)