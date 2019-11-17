import os
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='rss_reader',
    version='1.0',
    description='A useful module',
    license="MIT",
    author='Varabei Kanstantsin',
    author_email='vorobeybird@gmail.com',
    url='https://github.com/introduction-to-python-bsuir-2019/PythonHomework/pull/48',
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    entry_points = {
        'console_scripts': ['rss-reader=PythonHomework.rss_reader:Main'],
    }
)
