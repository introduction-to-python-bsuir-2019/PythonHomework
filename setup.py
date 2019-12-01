from setuptools import setup

setup(
    name='RSS reader',
    version = 'Second iteration',
    description = 'CLI utility to process RSS',
    author = 'Pavel Shymansky',
    py_module = ['rss_reader.py', 'arg.py', 'loggerfile.py', 'version.py', 'cache.py', 'date_converter.py', 'SakBunderan.ttf'],
    install_requires = ['feedparser', 'bs4'],
    python_requires='>=3.7',
    entry_points ='''
    [console_scripts]
    rss-reader=rss_reader:main
    '''
    )