# RSS reader

RSS reader is a command-line utility that receives [RSS](wikipedia.org/wiki/RSS) URL and prints results in a human-readable format.

## Install
 For install come to the root of repository and type:
``` shell
pip3 install .
```

or  
``` shell
pip3 install -r requirements.txt && python3 setup.py install
```

## Using

Utility provide the following interface:

```shell 
rss_reader [-h] [--version] [--json] [--verbose] [--limit LIMIT] 
```

* positional arguments:

    - ```source```  RSS URL

* optional arguments:
   - ```-h, --help```     show this help message and exit
   - ```--version```      Print version info
   - ```--json```         Print result as JSON in stdout
   - ```--verbose```      Outputs verbose status messages
   - ```--limit LIMIT```  Limit news topics if this parameter provided
   - ```--date DATE```    Returns news for requested date and source if this parameter provided. Date format is YYYYmmdd

Notes:

* JSON schema described in *json_feed.json*.
* By default log messages writes to *home/.rss/rss_reader.log*, 
with ```--verbose``` argument messages prints to stdout too.
* Can run the application by ```python3 rss_reader```  
or 
``` python3 rss_reader/main.py``` from the root of the repository.

## Testing


To test come to root directory of the repository and type 
```shell
 python3 tests 
```

## Caching


From version 3.0 all RSS feeds stored in local SQLite database
while reading. You can find a database in */home/.rss/feeds.db*.

The cashed news can be by read optional argument ```--date```. The news from the specified day and sourse will be printed out. If the news are not found returns an error.



