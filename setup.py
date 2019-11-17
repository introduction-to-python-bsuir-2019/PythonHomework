import setuptools

setuptools.setup(
    name="top-pure-rss-reader",
    version="0.2",
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
    python_requires='>=3.8'
)