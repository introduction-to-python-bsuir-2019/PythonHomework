from setuptools import setup, find_packages
import App

setup(
    name="RSS Reader",
    version=App.__version__,
    description="Utility to process RSS",
    author="Borodin Ilya",
    author_email="ilya.borodin8@gmail.com",
    url="https://github.com/ilyaborodin/PythonHomework/tree/Final_Task",
    packages=find_packages(),
    install_requires=['feedparser==5.2.1', 'weasyprint', 'termcolor'],
    python_requires='>=3.8',
    entry_points={
        "console_scripts": ["rss-reader=App.rss_reader:main"],
    }

)
