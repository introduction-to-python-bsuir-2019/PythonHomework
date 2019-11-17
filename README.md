# RSS reader
RSS reader is a command-line utility which receives RSS URL and prints results in human-readable format.

## Interface
Utility should provide the following interface:
+ Usage:
   + rss_reader.py 'source' '-h' '--version' '--json' '--verbose' '--limit LIMIT'
+ Positional arguments:
   + source - RSS URL
+ Optional arguments:
   + -h, --help    - Show this help message and exit
   + --version     - Print version info
   + --json        - Print result as JSON in stdout
   + --verbose     - Outputs verbose status messages
   + --limit LIMIT - Limit news topics if this parameter provided

Argument description:
+ In case of using --json argument your utility should convert the news into JSON format. You should come up with the JSON structure on you own and describe it in the README.md file for your repository or in a separate documentation file.
+ The --limit argument should also affect JSON generation.
+ With the argument --verbose your program should print all logs in stdout.
+ Withe the argument --version your program should print in stdout it's current version and complete it's work. The version supposed to change with every iteration.

## Distribution
Utility wrapped into distribution package 'rss_reader' with setuptools. This package export CLI utility named rss-reader.
