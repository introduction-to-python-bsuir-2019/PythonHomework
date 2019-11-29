# PythonHomework
[Introduction to Python] Homework Repository for EPAM courses

# How to use
1.  install git `apt-get install git`
2.  `pip3 install .`
3.  `rss-reader "https://www.androidpolice.com/feed/" --limit 3 --json --verbose --date`

# Parameters
-  **--help** (help text)
-  **--json** (print rss feed in json format)
-  **--verbose** (print verbose log messages)
-  **--limit** (limit printed entries)
-  **--date** (print cached entries if exist)
-  **--colorize** (colorize output)
-  **--to-html** (convert rss feed to html document)
-  **--to-pdf** (convert rss feed to pdf document)

## JSON structure
`{"feed": "rss_title", "entries": [{"title": "title", "date": "date", "link": "link", "summary": "summary"}, ...]}`

## Storage
Used [Pickle](https://docs.python.org/3/library/pickle.html) for storage

Entries cached in `cache/date/domain.rss`
-  cache - name of cache folder, default "cache"
-  date - script execution date
-  domain - domain of rss feed

Example: `cache/20191117/www.androidpolice.com.rss`

## Convertation

Examples:
-  `--to-html folder_name` will create "out.html" and "images" folder in folder_name, 
-  `--to-pdf folder_name` will create "out.pdf" in folder_name

# TODO
-   [x] [Iteration 1] One-shot command-line RSS reader.
-   [x] [Iteration 2] Distribution
-   [x] [Iteration 3] News caching
-   [x] [Iteration 4] Format converter
-   [x] * [Iteration 5] Output colorization
-   [ ] * [Iteration 6] Web-server
