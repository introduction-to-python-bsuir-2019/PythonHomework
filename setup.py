from setuptools import setup, find_packages

with open('README.md') as file:
    LONG_DESCRIPTION = file.read()

PACKAGE = 'rss-reader'

setup(
    name=PACKAGE,
    version=__import__(PACKAGE).__version__,
    description="RSS News Reader for EPAM Python Courses",
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author="Pivovar Sergey",
    author_email="pivovar-ser-leon@inbox.ru",
    url="https://github.com/TeRRoRlsT/PythonHomework.git",

    packages=find_packages(),

    python_requires='>=3.8',
    install_requires=['argparse', 'logging', 'feedparser', 'htmlparser', 'json'],

    classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
)
