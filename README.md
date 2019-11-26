# Rss reader hometask for EpamTrainee
Python RSS-reader.

Url for cloning:
`https://github.com/Nenu1985/PythonHomework.git`

Version 4
```shell
usage: rss_reader [-h] [--verbose] [--limit LIMIT] [--json] [-v]
                  [--width WIDTH] [--date DATE] [--to_pdf TO_PDF]
                  [--to_html TO_HTML]
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
./make_tests.sh
```
- to pass test with coverage
(nose and coverage packages must be installed)

## Version 2: Distribution
Utility wrapes into distribution package with setuptools.
This package exports CLI utility named rss-reader.

To generate distribution package (setuptool and wheel must be installed).
Launch:

``` python3 setup.py sdist bdist_wheel```

In the ./dist repo you'll find a .tar and .whl files.

Wheel package for the second iteration task 
(maybe is discarded but it works) on the Google Drive:
```https://drive.google.com/file/d/1RbMYxvpEXTx77Dk61xPkwSChD_jTf0jf/view?usp=sharin```

Actual packages you may find in the './dist' repo if you don't want to generate it manually.

Installing: 

```python3 -m pip install ./dist/rss_reader-4.0-py3-none-any.whl```

OR
```
python3 -m pip install -r requirements.txt
pip install ./dist/rss-reader-4.0.tar.gz
```
## Version 3: News cashing
News cashing implemented by using Sqlite3 DB. DB consists of 4 related tables: feed, news_item, links, imgs.
The implementation is in the rss_reader/utils/sqlite.py file. It contains RssDB class. Builtin sqlite3 lib is
used.
Base RssParser class imports RssDB class and uses for storing and loading data. RssParser's method print_news() 
is decorated with call_save_news_after_method() (rss_parser/utils/decorators) that calls appropriate function 
for storing news data (_store_news()).

## Version 4: Converters
Utility implements news converting to pdf and html formats. See according files: rss_reader/utils/pdf.py and 
rss_reader/utils/html_writer.py files.
Pdf converter uses pyFPDF package. To correct print cyrillic symbols djvu fonts are imported. Html2Pdf method
doesn't use because of unsupported utf-8 encoding. That's why I had to parse htmls and generate pdf object 
manually.
Html converter uses lxml.html library to parse and generate html content. 



## Docker deployment
docker run -it python /bin/bash
git clone https://github.com/Nenu1985/PythonHomework.git 
cd PythonHomework
pip install -r requirements.txt
pip install .
rss-reader --help




