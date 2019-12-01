# Pure Python RSS Reader [PythonHomework]

Python version: v3.8

Current version: v0.2

Code checking: Code correspond to pep8
#### Usage:
```shell
usage: __main__.py [-h] [--version] [--json] [--verbose] [--limit LIMIT] [--date DATE] [--to-pdf] [--to-html] source

Pure Python command-line RSS reader.

positional arguments:
  source         RSS URL

optional arguments:
  -h, --help     show this help message and exit
  --version      Print version info
  --json         Print result as JSON in stdout
  --verbose      Outputs verbose status messages
  --limit LIMIT  Limit news topics if this parameter provided
  --date DATE    Show cached news by input date
  --to-pdf       Convert news to pdf format
  --to-html      Convert news to html format
  ```
  JSON scheme is described in `json_schema.json`.
  
  News caching in json file `cached_news.json` in root application directory.
