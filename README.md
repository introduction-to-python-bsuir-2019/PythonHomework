#RSS reader

RSS reader is a command-line utility which receives RSS URL and prints results in human-readable format.


## Specification
Utility provides the following interface:
  + positional arguments:
    + source - RSS URL
  + optional arguments:
    + -h, --help - Show help message and exit.
    + --version  - Print version info.
    + --json     - Print result as JSON in stdout.
    + --verbose  - Outputs verbose status messages.
    + --limit    - Limit news topics if this parameter is provided.
    + --date     - Return cached news from the specified day. Format is %Y%M%D.

##Install RSS reader

  + ...

## Distribution
Utility is wrapped into package named rss_reader_ft. Additionally this package exports CLI utility named rss-reader.

## Caching
The RSS news are stored in a local storage while reading.