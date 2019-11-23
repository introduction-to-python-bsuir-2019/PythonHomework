# Desktop-Console-Utility
---

Utility provides the following interface:

- positional arguments:

|argument|description|
|---|---|
|link | Link on RSS resource|

- optional arguments:

|argument|description|
|---|---|
|-h, --help     |       show this help message and exit
|  -v, --version   |      Print version info
|  --json         |       Print result as JSON in stdout
|  -l LIMIT, --limit LIMIT|  Limit news topics if this parameter provided
|  --date DATE      |     Argument, which allows to get !cashed! news by date. Format: YYYYMMDD
|  -V, --verbose     |    Print all logs in stdout
|  --to_fb2 PATH    |     Convert news to fb2 format. Path must contain exsisting directories Supports LIMIT
|  --to_pdf PATH   |      Convert news to pdf format. Convertation to PDF supports only latin resource. Path must contain exsisting directories Supports LIMIT|
