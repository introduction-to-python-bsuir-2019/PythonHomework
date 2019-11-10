import setuptools

setuptools.setup(
    name='rss_reader_echizhevskaya',
    version='1.0.0',
    author='echizhevskaya',
    url='https://github.com/KateChizhevskaya/PythonHomework',
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    entry_points={
        'console_scripts': ['rss-reader=rssConverter.main:main'],
    }
)