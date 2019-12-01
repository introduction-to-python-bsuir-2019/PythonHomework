# RSS reader
RSS (originally RDF Site Summary; later, two competing approaches emerged, which used the backronyms Rich Site Summary and Really Simple Syndication respectively) is a type of web feed which allows users and applications to access updates to websites in a standardized, computer-readable format. These feeds can, for example, allow a user to keep track of many different websites in a single news aggregator.
RSS reader is a command-line utility which receives RSS URL and prints results.


## Specification
Utility provides the following interface:
  * positional\required arguments:
    * source .. RSS URL
  * optional arguments:
    * -h, --help -- Show help message and exit.
    * --version  -- Print version info.
    * --json     -- Print result as JSON in stdout.
    * --verbose  -- Outputs verbose status messages.
    * --limit    -- Limit news topics if this parameter is provided.
    * --date     -- Return cached news from the specified day. Format is YYYYMMDD.
    * --to_pdf   -- Convert news into pdf format and save a file to the specified path.


Notes
  * in case of using `--json` argument utility converts the news into JSON format.
  * the `--limit` also affects JSON format.


## Caching
News is stored in local storage are named 'mydatabase.db'
News that was already saved is not taken into account while caching. `--date` prints news in entered format (YYYYMMDD).

## Format converter
It's also provided function which converts news in PDF but it's very poor:(