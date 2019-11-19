from setuptools import setup, find_packages
import reader

setup(
	name='reader',
	version=reader.__version__,
	packages=find_packages(),
	entry_points={
		'console_scripts':
			['rss_reader = reader.rss:main']
	},
	install_requires=[
		"logging",
		"argparse",
		"beautifulsoup4",
		"lxml",
	],
)
