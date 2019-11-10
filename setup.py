from setuptools import setup

DESCRIPTON = 'RSS reader is a command-line utility, \
which receives RSS URL and prints results in human-readable format.'

setup(name='rss-reader',
	version='1.0',
	description=DESCRIPTON,
	url='#',
	author='KozachenkoKirill',
	author_email='mr.elaskin@mail.ru',
	license='EPAM-Introduction-to-Python',
	packages=['RSS-Reader'],
	zip_safe=False
)
