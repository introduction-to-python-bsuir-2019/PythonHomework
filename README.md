#One-shot command-line RSS reader
###Interface
usage: rss_reader.py  [-h] [--version] [--json] [--verbose] [--limit LIMIT]
                     url

Pure Python command-line RSS reader.

positional arguments:
  url         RSS URL

optional arguments:
  -h, --help     show this help message and exit
  --version      Print version info
  --json         Print result as JSON in stdout
  --verbose      Outputs verbose status messages
  --limit LIMIT  Limit news topics if this parameter provided