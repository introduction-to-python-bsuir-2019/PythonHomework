# PythonHomework
[Introduction to Python] Homework Repository
# How to use
* pip install -r requirements.txt
* python rss-reader "https://news.yahoo.com/rss/" --limit 2 --json
# Parameters
* --help (Show this help message and exit)
* source (RSS URL)
* --limit LIMIT (Limit news topics if this parameter provided)
* --json (Prints result as JSON in stdout)
* --verbose (Outputs verbose status messages)
* --version (Print version info)
* --date ()
# JSON structure
news = {"Title": "title", "Date":"date", "Alt image":"alt", "Discription":"discription", "Links":{"News":"link", "Image":"src"} }