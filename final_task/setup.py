import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="rss-reader",
    version="1.4",
    author="Anton Pashkevich",
    author_email="mario.lazer@mail.ru",
    description="Pure Python command-line RSS reader",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    url="https://github.com/prague15031939/PythonHomework",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["rss_reader"],
    package_dir={"rss_reader": 'rss_reader'},
    include_package_data=True,
    python_requires='>=3.8',
    install_requires=['feedparser', 'bs4', 'fpdf'],
    entry_points={
        'console_scripts':
            [f"rss-reader = rss_reader.rss_reader:main"]
        }
)
