import setuptools
import conf
from pathlib import Path

here = Path(__file__).resolve()


def get_install_requirements():
    with open(here.joinpath('requirements.txt'), 'r') as file:
        return [requirement.strip() for requirement in file]


with open(here.joinpath('README.md'), encoding='utf-8') as f:
    long_description = f.read()


setuptools.setup(
    name=conf.__package__,
    version=conf.__version__,
    license='MIT',
    author=conf.__author__,
    author_email=conf.__email__,
    description=long_description,
    long_description=conf.__description__,
    long_description_content_type='text/markdown',
    url=conf.__url__,
    packages=setuptools.find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=get_install_requirements(),
    python_requires='>=3.6',
    entry_points={
        'console_scripts':
            ['%s = __main__:main' % conf.__package__]
    }
)
