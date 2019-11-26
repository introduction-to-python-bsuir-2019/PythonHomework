"""Utils to export CLI rss_reader module
using: 'python3 setup.py sdist bdist_wheel'
"""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

def get_install_requires():
    with open('requirements.txt') as f:
        return [req.strip() for req in f]

setuptools.setup(
    name="rss-reader",  # Replace with your own username
    version=str(4.0),
    author="Andrey Nenuzhny",
    author_email="nenuzhny85@gmail.com",
    description="Rss reader Epam task",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Nenu1985/PythonHomework",

    packages=setuptools.find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),

    install_requires=get_install_requires(),

    extras_require={  # Optional
        'tests': ['nose', 'coverage'],
    },

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
    ],

    zip_safe=False,
    python_requires='>=3.7',
)
