import setuptools

with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
    name='rss_reader',
    version='1.3',
    author='Boris Dashko',
    author_email='borya.dashko@gmail.com',
    url='https://github.com/BoryaD/PythonHomework/tree/FinalTask',
    packages=setuptools.find_packages(),
    python_requires='>=3.8',
    install_requires=required,
    entry_points={
        'console_scripts': [
            'rss-reader = rss_reader.rss_reader:main',
        ],
    },
)