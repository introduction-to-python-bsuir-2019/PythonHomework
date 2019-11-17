from setuptools import setup

setup(
    name='rss-reader',
    version='1.2',
    packages=['rss_reader'],
    url='',
    license='',
    author='Zavxoz',
    author_email='artem.klimec8@gmail.com',
    description='simple command-line rss reader',
    entry_points={
        'console_scripts': ['rss-reader = rss_reader.cli:main']
    }
)
