import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='rss_reader',
    version='1.0',
    author='Andrei Antnoiuk',
    author_email='andriei.antoniuk@gmail.com',
    packages=setuptools.find_packages(),
    python_requires='>=3.7',
    entry_points = {
        'console_scripts': ['rss-reader=rss_reader.rss_reader:main'],
    }
)