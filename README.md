# RSS reader

RSS reader is a command-line utility which receives [RSS](wikipedia.org/wiki/RSS) URL and prints results in human-readable format.

## Declaration

Utility provide the following interface:
```shell 
rss_reader.py [-h] [--version] [--json] [--verbose] [--limit LIMIT] 
```

    * positional arguments:
        source  RSS URL

    * optional arguments:
        -h, --help     show this help message and exit
        --version      Print version info
        --json         Print result as JSON in stdout
        --verbose      Outputs verbose status messages
        --limit LIMIT  Limit news topics if this parameter provided
Notes:

    * JSON schema described in json_feed.json.
    * By default status messages writes to rss_reader.log, 
      with --verbose argument messages prints to stdout too.