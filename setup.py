import setuptools
import os

with open("requirements.txt") as fp:
    install_requires = fp.read()

setuptools.setup(
    name='rss_reader',
    author='echizhevskaya',
    long_description=open(os.path.join(os.path.dirname(__file__), "README.md")).read(),
    url='https://github.com/KateChizhevskaya/PythonHomework',
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=install_requires,
    entry_points={
        'console_scripts': ['rss-reader=app.rssConverter.main:main'],
    }
)