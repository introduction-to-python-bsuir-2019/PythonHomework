from setuptools import setup, find_packages

DESCRIPTON = 'RSS reader is a command-line utility, \
which receives RSS URL and prints results in human-readable format.'

setup(
    name='webrssreader',
    version='1.0',
    description=DESCRIPTON,
    url='#',
    author='KozachenkoKirill',
    author_email='mr.elaskin@mail.ru',
    license='EPAM-Introduction-to-Python-2019',
    python_requires='>=3.6',
    install_requires=['feedparser', 'bs4', 'lxml', 'fpdf', 'sqlparse', 'django'],
    zip_safe=False
)
