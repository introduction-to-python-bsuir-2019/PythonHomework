import os

from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='rss-reader',
    version='0.4.0',
    description='A simple Python3.8 rss reader',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/introduction-to-python-bsuir-2019/PythonHomework',
    author='Dydyshko Andrey',
    author_email='dydyshko1999@gmail.com',
    keywords='simple rss reader',
    # packages=find_packages(),
    packages=['app', 'fonts', 'app.fonts'],
    # fonts for PDF
    package_data={
        'app': [
            'app/fonts/NotoSans-Black.ttf',
            'app/fonts/Black.cw127.pkl',
            'app/fonts/NotoSans-Black.pkl',
            'app/fonts/NotoSans-Thin.ttf',
            'app/fonts/NotoSans-Thin.pkl',
            'app/fonts/NotoSans-Thin.cw127.pkl',
        ],
        'fonts': [
            'NotoSans-Black.ttf',
            'Black.cw127.pkl',
            'NotoSans-Black.pkl',
            'NotoSans-Thin.ttf',
            'NotoSans-Thin.pkl',
            'NotoSans-Thin.cw127.pkl',
        ]
    },
    # data_files=[('app', ['fonts/NotoSans-Black.ttf', ])],
    include_package_data=True,
    python_requires='>=3.8',
    install_requires=['feedparser>=6.0.0b1', 'requests', 'bs4', 'python-dateutil', 'fpdf', 'setuptools-git'],
    entry_points={
        'console_scripts': [
            'rss-reader=app.__main__:main',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/introduction-to-python-bsuir-2019/PythonHomework/issues',
        'Source': 'https://github.com/introduction-to-python-bsuir-2019/PythonHomework',
    },
)