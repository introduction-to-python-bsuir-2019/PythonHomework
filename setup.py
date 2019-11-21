from setuptools import setup

setup(
    name='RSS parser',
    version = 'Second iteration',
    description = 'CLI utility to process RSS',
    author = 'Pavel Shymansky',
    py_module = ['rss.parser','arg.py'],
    install_requires = ['feedparser', 'bs4'], #!!!!!!!!!!!!!!!!!!!не забытЬ!!!!!!!!!!!!!
    python_requires='>=3.8',
    entry_points ='''
    [console_scripts]
    rss-parser=rss_parser: main
    '''
    )