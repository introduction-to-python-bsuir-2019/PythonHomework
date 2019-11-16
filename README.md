# PythonHomework
[Introduction to Python] Homework Repository

# How to use
* pip install -r requirements.txt
* python rss-reader.py "https://news.yahoo.com/rss/" --limit 2 --json

# Parameters
* --help (show this help message and exit)
* --limit LIMIT (limit news topics if this parameter provided)
* --json (prints result as JSON in stdout)
* --verbose (outputs verbose status messages)
* --version (print version info)

# JSON structure
feed = {
  'Title': 'feed title',
  'Published': 'date',
  'Summary': 'news description',
  'Link': 'original link to news',
}
