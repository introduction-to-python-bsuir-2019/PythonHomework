#Introduction to Python. Hometask

RSS reader is a command-line utility which receives RSS URL and prints results in human-readable format.

Utility provides the following interface:

usage: rss_reader.py [-h] [--version] [--json] [--verbose] [--limit LIMIT] [--date DATE] [--colorize] [--to-fb2] [--to-pdf]
                     source

Pure Python command-line RSS reader.

positional arguments:
  source         RSS URL

optional arguments:
  -h, --help     Show this help message and exit
  --version      Print version info
  --json         Print result as JSON in stdout
  --verbose      Outputs verbose status messages
  --limit LIMIT  Limit news topics if this parameter provided
  --date DATE    Print news topics for a specific date  
  --colorize     Print the result of the utility in colorized mode
  --to-fb2       In the activated state, the program creates a News.fb2 file in the working directory
  --to-pdf       In the activated state, the program creates a News.pdf file in the working directory
  