#RSS reader

RSS reader is a command-line utility which receives RSS URL and prints results in human-readable format.


## Specification
Utility provides the following interface:
  + positional arguments:
    + source - RSS URL
  + optional arguments:
    + -h, --help - Show help message and exit.
    + --version  - Print version info.
    + --json     - Print result as JSON in stdout.
    + --verbose  - Outputs verbose status messages.
    + --limit    - Limit news topics if this parameter is provided.
    + --date     - Return cached news from the specified day. Format is %Y%M%D.

##Install RSS reader

1. Clone or Download [repository](https://github.com/ZayJob/PythonHomework)
2. Go to folder /PythonHomework
3. **git branch**
4. There is no branch besides **master**? Then follow this tutorial.
    + **git branch -a**.
    + **git branch --track finalTask remotes/origin/finalTask**.
    + **git checkout finalTask**.
    + **git branch**.
    + **git checkout cfbdb81**.
5. I recommend creating a virtual environment. **python3.8 -m venv env**, **. env/bin/activate**.
6. Let's collect our package **python3.8 setup.py sdist**.
7. Let's install our package **pip3.8 install dist/rss-reader-2.0.tar.gz**

## Distribution
Utility is wrapped into package named rss_reader_ft. Additionally this package exports CLI utility named rss-reader.

## Caching
The RSS news are stored in a local storage while reading.
