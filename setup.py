import os

import setuptools

import app
from app.support_files.config import APP_NAME

with open("requirements.txt") as fp:
    install_requires = fp.read()

setuptools.setup(
    name=APP_NAME,
    version=app.__version__,
    author="Budzich Maxim",
    author_email="131119999@gmail.com",
    long_description=open(os.path.join(os.path.dirname(__file__), "README.md")).read(),
    url="https://github.com/Zviger/PythonHomework/tree/final_proj",
    packages=setuptools.find_packages(),
    python_requires=">=3.8",
    install_requires=install_requires,
    include_package_data=True,
    entry_points={
        "console_scripts": [f"{APP_NAME}=app.core:main"],
    }
)
