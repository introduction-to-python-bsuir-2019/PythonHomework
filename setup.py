from setuptools import setup
from rss_reader import __version__ as version


with open('requirements.txt') as f:
    requirements = f.read()


setup(
    name='rss-reader',
    version=version,
    packages=['rss_reader'],
    url='',
    license='',
    author='Zavxoz',
    author_email='artem.klimec8@gmail.com',
    description='simple command-line rss reader',
    install_requires=requirements,
    include_package_data=True,
    entry_points={
        'console_scripts': ['rss-reader = rss_reader.cli:main']
    }
)
