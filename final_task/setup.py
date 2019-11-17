import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="rss-reader",
    version="1.2",
    author="Anton Pashkevich",
    author_email="mario.lazer@mail.ru",
    description="Pure Python command-line RSS reader",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/prague15031939/PythonHomework",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)