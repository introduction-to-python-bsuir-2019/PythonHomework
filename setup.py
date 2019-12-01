from setuptools import setup, find_packages

with open('README.md') as file:
    LONG_DESCRIPTION = file.read()

setup(
    name='rss-reader',
    version=__import__('rssreader').__version__,
    description="RSS News Reader for EPAM Python Courses",
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author="Pivovar Sergey",
    author_email="pivovar-ser-leon@inbox.ru",
    url="https://github.com/TeRRoRlsT/PythonHomework.git",

    packages=find_packages(),

    python_requires='>=3.8',
    install_requires=['feedparser', 'requests', 'fpdf', 'peewee', 'colorama'],

    entry_points={
        'console_scripts': [
            'rss-reader=rssreader.rss_reader:main',
        ]
    },
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
)
