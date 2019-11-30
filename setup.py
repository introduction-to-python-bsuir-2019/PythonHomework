import setuptools

setuptools.setup(
    name="rss-reader",
    version="0.4",
    author="Archeex",
    author_email="qsanich@gmail.com",
    description="Pure Python command-line RSS reader",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': ['rss_reader = rss_reader.__main__:main']
    },
    install_requires=[
        'feedparser==5.2.1',
        'requests==2.22.0',
        'tldextract==2.2.2'
    ],
    python_requires='>=3.8'
)