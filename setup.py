from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='rss-reader',
    version='3.0',
    description='Pure Python command-line RSS reader',
    long_description=long_description,
    url='https://github.com/yanaShcherbich/PythonHomework',
    author='Yana Shcherbich',
    author_email='vilikdf@gmail.com',
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=['feedparser', 'bs4', 'dateparser'],
    entry_points={
        'console_scripts': ['rss-reader=rss.rss_reader:run'],
    }
)
