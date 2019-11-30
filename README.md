# One-shot command-line RSS reader
### Interface
usage: rss_reader.py  [-h] [--version] [--json] [--verbose] [--limit LIMIT]
                      [--to-html] [--to-fb2] [--date] url

Pure Python command-line RSS reader.

positional arguments:
  url         RSS URL

optional arguments:
  -h, --help     show this help message and exit
  --version      Print version info
  --json         Print result as JSON in stdout
  --verbose      Outputs verbose status messages
  --limit LIMIT  Limit news topics if this parameter provided
  --to-html      Creating html file with news at specified path
  --to-fb2       Creating fb2 file with news at specified path
  --date         Returning news that you read at that date at format YearMonthDate (20191020 for example)
  
 example of json format:
{
  "news" : [
    {
    "title" : ,
    "summary" : ,
    "link" : ,
    "images" :,
    "links" : []
    }
  ]
}

###Installation
1) git clone < repositiry >  
2) cd PythonHomework
3) pip install . 
4) run reader
