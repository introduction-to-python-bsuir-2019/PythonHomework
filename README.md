# Pure Python RSS Reader [PythonHomework]

Python version: v3.8

Current version: v0.2

Code checking: Code correspond to pep8
#### Usage:
```shell
usage: __main__.py [-h] [--version] [--json] [--verbose] [--limit LIMIT] source

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
  ```
  JSON scheme is described in `json_schema.json`
