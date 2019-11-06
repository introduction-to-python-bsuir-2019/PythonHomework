# RSS reader

RSS reader is a command-line utility which receives RSS URL and prints results in human-readable format.


## Specification
Utility provides the following interface:
  * positional\required arguments:
    * source .. RSS URL
  * optional arguments:
    * -h, --help .. Show help message and exit.
    * --version  .. Print version info.
    * --json     .. Print result as JSON in stdout.
    * --verbose  .. Outputs verbose status messages.
    * --limit    .. Limit news topics if this parameter is provided.
    * --date     .. Return cached news from the specified day. Format is YYYYMMDD.

There are several notes:
  * in case of using `--json` argument utility converts the news into JSON format. JSON schema is described in feed_json_schema.json. 
  * the `--limit` argument affects JSON generation to.
  * with the argument `--verbose` program prints all logs in stdout.
  * with the argument `--version` program prints in stdout it's current version and complete it's work. The version supposed to change with every iteration.

## Distribution
Utility is wrapped into package named _rssreader_. Additionally this package exports CLI utility named _rss-reader_.

## Caching
The RSS news are stored in a local storage while reading. Local storage is internally based on sqlite3.
The database file is stored in the home directory under the name _rssreader.db_.

Just to be clear, the `--limit` argument doesn't affect the number of news to be stored locally.
A whole set of news is cached every time. Sure, if any news already exists in the cache, it won't be added.
