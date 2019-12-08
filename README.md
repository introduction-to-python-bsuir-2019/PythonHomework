# PythonHomework
[Introduction to Python] Homework Repository

# How to use
* pip install .
* rss-reader rss-reader.py "https://news.yahoo.com/rss/" --limit 2 --json
--to-pdf C:\Users\User_name\Desktop
* --date prints cached news that were parsed previously from the given URL
Creates folder cache and saves news in JSON files format
file name = date (like 20191125.json)
* For --to-pdf argument: specify the path to the folder 
where 'news.pdf/cached_news.pdf' file will be saved.
The file will be overwritten after restarting the program.
Make sure to copy that file if you need it. Same thing with --to-html argument.
Also --to-html uses pictures from websites, so they wont be displayed without
internet connection
* Btw i use fonts for .pdf files to avoid encoding issues,
hope they will be installed correctly by 'pip install .'


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
* --to-html TO_HTML (It should take the path of the directory where new HTML file will be saved)

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
-   [x] [Iteration 4] Format converter
-   [x] * [Iteration 5] Output colorization
-   [ ] * [Iteration 6] Web-server