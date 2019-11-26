#Introduction to Python. Hometask

RSS reader is a command-line utility which receives RSS URL and prints results in human-readable format.

Utility provides the following interface:

usage: rss_reader.py [-h] [--version] [--json] [--verbose] [--limit LIMIT] [--date DATE]
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
  --date DATE    print news topics for a specific date    