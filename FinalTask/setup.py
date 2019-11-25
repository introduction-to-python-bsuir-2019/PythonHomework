import setuptools

setuptools.setup(
                name='rss_reader',
                version='2.0',
                description='Pure Python CLI RSS reader',
                author='Aliaksei Krop',
                author_email='qqaezz@gmail.com',
                include_package_data=True,
                python_requires='>=3',
                packages=setuptools.find_packages(exclude=["tests"]),
                py_modules=['rss_reader.RSSHandle'],
                entry_points={
                    'console_scripts': [
                        'rss-reader=rss_reader.rss_reader:main',
                        'rss_reader=rss_reader.rss_reader:main'
                    ]
                },
                package_data={
                    '': ['*.txt', '*.in', '*.md']
                }
)
