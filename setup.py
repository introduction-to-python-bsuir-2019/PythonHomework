from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='rss-reader',
    version='2.0',
    description='Pure Python command-line RSS reader',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/yanaShcherbich/PythonHomework',
    author='Yana Shcherbich',
    author_email='vilikdf@gmail.com',
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=['feedparser', 'bs4'],
    entry_points={
        'console_scripts': ['rss-reader=rss.rss_reader:main'],
    }
)
