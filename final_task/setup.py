import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='rss_reader',
    version='3.0',
    author='Polina Pashkovskaya',
    author_email='polly.pashkovskaya@gmail.com',
    url='https://github.com/pashkovskaya/PythonHomework/tree/final_task/final_task',
    packages=setuptools.find_packages(),
    python_requires='>=3.8',
    install_requires=['jinja2', 'requests', 'bs4', 'feedparser', 'lxml'],
    entry_points={
        'console_scripts': ['rss-reader=rss_reader.rss_reader:main'],
    }
)
