# euesand's RSS-reader
My RSS-reader is a command line utility which parses RSS URL and prints news in human-readable format.
## installation
You can use pip to install my package from test pypi index:
```bash
pip install --extra-index-package https://test.pypi.org/simple/ rss-reader-euseand==0.4
```
Or simply clone the repo and use pip install:
```bash
git clone --branch FinalTask https://github.com/euseand/PythonHomework.git
pip install .
``` 
## usage
Print 10(default limit) news from default (yahoo) online feed:
```bash
rss-reader ""
```
Print 10 news from online feed and store it in HTML-page with additional verbosity:
```bash
rss-reader "https://news.yahoo.com/rss/" --limit 10 --verbose --to-html
```
Print 10 news from cached feed and store it in HTML-page:
```bash
rss-reader "https://news.yahoo.com/rss/" --limit 10 --date 20191129
```
## feed examples (tested):
```bash
https://news.google.com/news/rss
https://news.yahoo.com/rss/
```