# RSS reader
RSS reader is a command-line utility which receives RSS URL and prints results in human-readable format.

## Interface
Utility should provide the following interface:
+ Usage:
   + rss_reader.py 'source' '-h' '--version' '--json' '--verbose' '--limit LIMIT'
+ Positional arguments:
   + source - RSS URL
+ Optional arguments:
   + -h, --help     - Show this help message and exit
   + --version      - Print version info
   + --json         - Print result as JSON in stdout
   + --verbose      - Outputs verbose status messages
   + --limit LIMIT  - Limit news topics if this parameter provided
   + --date DATE    - Display news for the specified day, reading them from the cache. DATE format: YYYYmmDD
   + --to-html PATH - Convert news to HTML format. Specify the path to the file in PATH
   + --to-pdf PATH  - Convert news to PDF format. Specify the path to the file in PATH
   + --colorize     - Print text result in colorized mode

Argument description:
+ In case of using --json argument your utility should convert the news into JSON format. You should come up with the JSON structure on you own and describe it in the README.md file for your repository or in a separate documentation file.
+ The --limit argument should also affect JSON generation.
+ With the argument --verbose your program should print all logs in stdout.
+ Withe the argument --version your program should print in stdout it's current version and complete it's work. The version supposed to change with every iteration.

## Distribution
Utility wrapped into distribution package 'rss_reader' with setuptools. This package export CLI utility named rss-reader.

## Caching
The RSS news are stored in a local storage while reading. Local storage is based on TinyDB. Cached information is stored in a file 'cache_db.json'. All news read from the RSS feed are written to the repository. To read news from the cache implement '--date' argument

## Format converter
News can be converted into HTML and PDF formats. To convert news to a file implement '--to-html' or '--to-pdf' argument and specify the path to the local file.

## Unit tests
The program code can be checked by running the command 'nosetests' from the root of the repository. The package 'nose' is required.
