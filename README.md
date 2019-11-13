# PythonHomework
[Introduction to Python] Homework Repository for EPAM courses

# How to use
1.  `pip3 install -r requirements.txt`
2.  `python3.8 rss_reader.py "https://www.androidpolice.com/feed/" --limit 10 --json`

# Parameters
-  **--help** (help text)
-  **--json** (print rss feed in json format)
-  **--verbose** (print verbose log messages)
-  **--limit** (limit printed entries)

## JSON structure
`{"feed": "rss_title", "entries": [{"title": "title", "date": "date", "link": "link", "summary": "summary"}, ...]}`

# TODO
-   [x] [Iteration 1] One-shot command-line RSS reader.
-   [ ] [Iteration 2] Distribution
-   [ ] [Iteration 3] News caching
-   [ ] [Iteration 4] Format converter
-   [ ] * [Iteration 5] Output colorization
-   [ ] * [Iteration 6] Web-server
