# Introduction to Python. Hometask

RSS reader is a command-line utility which receives [RSS](wikipedia.org/wiki/RSS) URL and prints results in human-readable format.


Utility provides the following interface:
```shell
usage: rss_reader.py [-h] [--version] [--json] [--verbose] [--limit LIMIT]
                     [--date DATE] [--to-html TO_HTML] [--to-fb2 TO_FB2]
                     [--colorize]
                     source

Pure Python command-line RSS reader.

positional arguments:
  source         RSS URL

optional arguments:
  -h, --help         show this help message and exit
  --version          Prints version info
  --json             Prints result as JSON in stdout
  --verbose          Outputs verbose status messages
  --limit LIMIT      Limits news topics if this parameter provided
  --date DATE        Shows news of specific date
  --to-html TO_HTML  Converts news into html format and save to a specified
                     path
  --to-fb2 TO_FB2    Converts news into fb2 format and save to a specified
                     path
  --colorize         Colorizes the cmd output
```

With the argument `--json` the program converts the news into [JSON](https://en.wikipedia.org/wiki/JSON) format.

With the argument `--limit` the program prints given number of news.

With the argument `--verbose` the program prints all logs in stdout.

With the argument `--version` the program prints in stdout it's current version and complete it's work.

With the argument `--date` the program prints or saves news of source from specific date stored if there are any.

With the argument `--to-html` the program saves news from source to the given path as a html file.

With the argument `--to-fb2` the program saves news from source to the given path as a fb2 file.

With the argument `--colorize` the program colorizes output in cmd.

# Caching

This program stores data in `"home directory"/rss_reader_cache`. In this directory images in folder `images` are stored and a `cache.json` file is located. It stores all data independent of `--date` attribute.