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

There are several notes:
  * in case of using `--json` argument utility converts the news into JSON format. JSON schema is described in feed_json_schema.json. 
  * the `--limit` argument affects JSON generation to.
  * with the argument `--verbose` program prints all logs in stdout.
  * with the argument `--version` program prints in stdout it's current version and complete it's work. The version supposed to change with every iteration.
