import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rss_reader", 
    version="1.0",
    author="Antonyuk Evgeniy",
    author_email="antoyuk.evgeniy333@gmail.com",
    description="final task",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Evgeniy69/PythonHomework",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
