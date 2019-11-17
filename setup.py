import setuptools
import conf

setuptools.setup(
    name=conf.__package__,
    version=conf.__version__,
    author=conf.__author__,
    author_email=conf.__email__,
    description=conf.__description__,
    url=conf.__url__,
    packages=[conf.__package__],
    python_requires='>=3.8',
    entry_points={
        'console_scripts':
            ['rss-reader = cmd:main']
    }
)
