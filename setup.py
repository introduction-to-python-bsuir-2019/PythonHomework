import setuptools
from rss_reader.rss_reader import VERSION

setuptools.setup(name='adzemreader',
                version=VERSION[1:],
                author='Aliaksei Dzemasiuk',
                author_email='mr.glazik@gmail.com',
                description='RSS-feed reader',
                long_description='Pure Python command line RSS-feed reader ',
                packages=setuptools.find_packages(),
                classifiers=["Programming Language :: Python :: 3",
                            "Operating System :: OS Independent"],
                python_requires='>=3.5',
                entry_points={'console_scripts': ['rssreader=rss_reader.rss_reader:main']},
                install_requires=['bs4',
                                 'feedparser',
                                 'jsonpickle'])       

