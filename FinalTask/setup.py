import setuptools

setuptools.setup(
                name='rss_reader',
                version='2.0',
                description='Pure Python CLI RSS reader',
                author='Aliaksei Krop',
                author_email='qqaezz@gmail.com',
                packages=setuptools.find_packages(include=['rss_reader, RSSHandle']),
                python_requires='>=3',
                scripts = ['rss_reader']
)
