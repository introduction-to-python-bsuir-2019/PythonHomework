# PythonHomework
[Introduction to Python] Homework Repository
# How to use
* pip install -r requirements.txt
* python main.py "https://news.yahoo.com/rss/" --limit 2 --json
# Parameters
* --help (Show this help message and exit)
* source (RSS URL)
* --limit LIMIT (Limit news topics if this parameter provided)
* --json (Prints result as JSON in stdout)
* --verbose (Outputs verbose status messages)
* --version (Print version info)
# JSON structure
news = {"Title": "title", "Date":"date", "Link":"link", "Discription":"discription"}