#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os import path
from setuptools import find_packages, setup

from core.__version__ import __version__

setup(
    name="rss_reader",
    version=__version__,
    description="Pure Python command-line RSS reader.",
    url="https://github.com/aviacore/PythonHomework",
    author="Sergey Kornilov",
    author_email="info@ksn.by",
    packages=find_packages(),
    requires=["argparse", "bs4", "requests", "termcolor"],
    scripts=["rss_reader.py"],
)
