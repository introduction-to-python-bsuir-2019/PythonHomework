# RSS-reader
RSS reader is a command-line utility which receives RSS URL and prints results in human-readable format.
## Installation
Use the package manager pip to install rss_reader.
```bash
pip install -i https://test.pypi.org/simple/ rss-reader-kis==1.1
pip install feedparser
pip install bs4
``` 
## Usage
```python
from reader import rss_reader

"""
Construct a new RSSReader object.

:param source: The name of your rss feed
:param limit: Limit of news that you want to see
"""
reader = rss_reader.RSSReader('https://news.yahoo.com/rss/', 2)
reader.parse_source()

```
## Promotion
Star are welcome.