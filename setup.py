from setuptools import setup

setup(
    name='rss-reader',
    version='1.0',
    packages=['rss-reader'],
    url='',
    license='',
    author='zavxoz',
    author_email='artem.klimec8@gmail.com',
    description='simple command-line rss reader',
    entry_points={
        'console_scripts': ['rss_reader = rss_reader.__main__:main']
    }
)
