import setuptools

setuptools.setup(
                name='rss_reader',
                version='2.0',
                description='Pure Python CLI RSS reader',
                author='Aliaksei Krop',
                author_email='qqaezz@gmail.com',
                include_package_data=True,
                python_requires='>=3',
                install_requires=['feedparser==5.2.1', 'beautifulsoup4==4.8.0',
                                  'python-dateutil==2.8.0', 'lxml==4.4.1'],
                packages=setuptools.find_packages(exclude=["tests"]),
                py_modules=['rss_reader_module.module.RSSHandle', 'rss_reader_module.rss_reader'],
                entry_points={
                    'console_scripts': [
                        'rss-reader=rss_reader_module.rss_reader:main',
                        'rss_reader=rss_reader_module.rss_reader:main'
                    ]
                },
                package_data={
                    '': ['*.txt', '*.in', '*.md']
                }
)
