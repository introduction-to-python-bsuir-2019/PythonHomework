# Small hometasks for EpamTrainee
ALmost every task function covered with docstring

# Launching:
pip install -r requiremets.txt
python 2.py
python 3.py
python 4.py

Version 6
```shell
usage: __main__.py [-h] [--verbose] [--limit LIMIT] [--json] [-v]
                   [--width WIDTH] [--date DATE] [--to_pdf TO_PDF]
                   [--to_html TO_HTML] [--colorize]
                   url

Rss reader. Just enter rss url from your favorite site and app will print
latest news.

positional arguments:
  url                url of rss

optional arguments:
  -h, --help         show this help message and exit
  --verbose          Outputs verbose status messages
  --limit LIMIT      Limit news topics if this parameter provided
  --json             Print result as JSON in stdout
  -v, --version      Print version info
  --width WIDTH      Define a screen width to display news
  --date DATE        Date of stored news you want to see. Format: %Y%m%d
  --to_pdf TO_PDF    Convert and store news you are looking for to pdf
  --to_html TO_HTML  Convert and store news you are looking for to html
  --colorize         Colorize text

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
Tests are available at `https://github.com/Nenu1985/PythonHomework`
Launching:
```
Starting static code analys 
2.py PASSED
3.py PASSED
4.py PASSED
```
## Iteration 5
Defined class Colors with stored attributes for text color.
Without console arg --colorize class initialises with no colors,
but with --colorize class initialises with colors. News classe
use Colors's attributes to print their text

## Iteration 6
Web app is a simple flask app that do the only think - launch 
rss_reader's modules. That's why there is no rest api and 'big' DB.

To run server you may create a docker image:
`docker build . -t flask:v1`

And run it in a docker container:
`docker run -p 5000:5000 flask:v1`

App will be accessible on the 0.0.0.0:5000 socket.
BTW those commands will install rss_reader utility.

## Installing
Use the script `./install_util.sh`.
- it will install all dependencies and launch the server in a 
docker container.
- to use rss_reader utility enter:
`python -m rss_reader`

If you don't have docker server will not be launched. But you can do it 
manually by entering (in the root folder 'PythonHomework'):
`python -m server`

