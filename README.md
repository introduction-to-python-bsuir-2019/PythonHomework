# Introduction to Python. Hometask

RSS reader is a command-line utility which receives [RSS](wikipedia.org/wiki/RSS) URL and prints results in human-readable format.


Utility provides the following interface:
```shell
usage: rss_reader.py [-h] [--version] [--json] [--verbose] [--limit LIMIT]
                     source

Pure Python command-line RSS reader.

positional arguments:
  source         RSS URL

optional arguments:
  -h, --help     show this help message and exit
  --version      Print version info
  --json         Print result as JSON in stdout
  --verbose      Outputs verbose status messages
  --limit LIMIT  Limit news topics if this parameter provided

```

With the argument `--json` the program converts the news into [JSON](https://en.wikipedia.org/wiki/JSON) format.

With the argument `--limit` the program prints given number of news.

With the argument `--verbose` the program prints all logs in stdout.(Still in progress)

Withe the argument `--version` the program prints in stdout it's current version and complete it's work.