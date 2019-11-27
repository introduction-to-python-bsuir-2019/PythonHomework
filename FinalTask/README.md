Pure Python command-line RSS reader.

Utility provide the following interface:

usage: rss_reader.py [-h] [--version] [--json] [--verbose] [--limit LIMIT]
                     [--source SOURCE] [--date DATE]

  --source or --date argument required   

  --source argument should take RSS feed url
  --date argument should take a date in %Y%m%d format

optional arguments:
  -h, --help     show this help message and exit
  --version      Print version info
  --json         Print result as JSON in stdout
  --verbose      Outputs verbose status messages
  --limit LIMIT  Limit news topics if this parameter provided
