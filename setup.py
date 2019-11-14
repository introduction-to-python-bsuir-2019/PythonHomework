import setuptools
import os
import app

with open('requirements.txt') as fp:
    install_requires = fp.read()

setuptools.setup(
    name='rss_reader',
    version=app.__version__,
    author='Budzich Maxim',
    author_email='131119999@gmail.com',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
    url='https://github.com/Zviger/PythonHomework/tree/final_proj',
    packages=setuptools.find_packages(),
    python_requires='>=3.8',
    install_requires=install_requires,
    entry_points={
        'console_scripts': ['rss_reader=app.core:main'],
    }
)
