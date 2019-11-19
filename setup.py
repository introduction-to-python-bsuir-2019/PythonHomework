from setuptools import setup, find_packages

setup(
	name='reader',
	version='1.13',
	packages=find_packages(),
	entry_points={
		'console_scripts':
			['rss_reader = reader.rss:main']
		}
)
