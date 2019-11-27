# PythonHomework
[Introduction to Python] Homework Repository

# How to use
* pip install -r requirements.txt
* python rss-reader.py "https://news.yahoo.com/rss/" --limit 2 --json
* --date prints cached news that were parsed previously from the given URL
* For --to-pdf argument: specify the path to the folder 
where 'news.pdf/cached_news.pdf' file will be saved.
The file will be overwritten after restarting the program.
Make sure to copy that file if you need it
* Btw i use fonts for .pdf files, hope they will be installed correctly
by 'pip install .'
* P.S. Ля, ребята, 4 курс птуира, уже распред идет во всю, работа нужна кааапец


# Parameters
* --help (show this help message and exit)
* --limit LIMIT (limit news topics if this parameter provided)
* --json (prints result as JSON in stdout)
* --verbose (outputs verbose status messages)
* --version (print version info)
* --date (It should take a date in YYYYmmdd format. For example:
 --date 20191020The new from the specified day will be printed out.
  If the news are not found error will be returned.)
* --to-pdf TO_PDF (It should take the path of the directory where new PDF file will be saved)

# JSON structure
feed = {
  'Title': 'feed title',
  'Published': 'date',
  'Summary': 'news description',
  'Link': 'original link to news',
  'Url': 'url of rss feed'
  'Image': 'original link to the image'
}

# Progress
-   [x] [Iteration 1] One-shot command-line RSS reader.
-   [x] [Iteration 2] Distribution
-   [x] [Iteration 3] News caching
-   [ ] [Iteration 4] Format converter
-   [ ] * [Iteration 5] Output colorization
-   [ ] * [Iteration 6] Web-server