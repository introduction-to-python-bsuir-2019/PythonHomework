# Rss reader hometask for EpamTrainee
Python RSS-reader.

Version 1
```shell
usage: rss.py [-h] [--verbose] [--limit LIMIT] [--json] [-v] [--width WIDTH]
              url

Rss reader. Just enter rss url from your favorite site and app will print
latest news.

positional arguments:
  url            url of rss

optional arguments:
  -h, --help     show this help message and exit
  --verbose      Outputs verbose status messages
  --limit LIMIT  Limit news topics if this parameter provided
  --json         Print result as JSON in stdout
  -v, --version  Print version info
  --width WIDTH  Define a screen width to display news

```

## Code description
* Code uses `argparse` module.
* Codebase covered with unit tests with at 90% coverage.
* Any mistakes are printed in human-readable error explanation.
Exception tracebacks in stdout are prohibited.
* Docstrings are mandatory for all methods, classes, functions and modules.
* Code corresponds to `pep8` (used `pycodestyle` utility for self-check).
* Feedparser module is used for rss parsing;
* There are several bots for parsing news: default bor for unimplemented RSS urls and
    custom bots (yahoo, tut) with detailed approach to parsing.

## Code self-checking
Use ./pycodestyle.sh to check the code corresponding to `pep8`
(pycodestyle package must be installed)

## Testing
Use 
```
nosetests --with-coverage --cover-erase --cover-package=utils --cover-html
nosetests --with-coverage --cover-erase --cover-package=bots --cover-html
nosetests --with-coverage --cover-erase --cover-package=rss --cover-html
```
- to pass test with coverage
(nose and coverage packages must be installed)



