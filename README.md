## It is a one-shot command-line RSS reader by Zviger.
### Installation
Clone this repository and run
```text
pip install . --user
```
Also, you must have installed and running MongoDB.
Run
```text
service mongod status
```
to make sure that Mongodb is running.
### User interface
```text
usage: rss-reader [-h] [--version] [-l LIMIT] [--verbose] [--json] [--length LENGTH] [--date DATE] [--to_html PATH] [--to_fb2 PATH] [--colorize] source

positional arguments:
  source                RSS URL

optional arguments:
  -h, --help            show this help message and exit
  --version             Print version info
  -l LIMIT, --limit LIMIT
                        Limit news topics if this parameter provided
  --verbose             Print result as JSON in stdout
  --json                Outputs verbose status messages
  --length LENGTH       Sets the length of each line of news output
  --date DATE           Search past news by date in format yeardaymonth (19991311)
  --to_html PATH        Save news by path in html format
  --to_fb2 PATH         Save news by path in fb2 format
  --colorize            Make console text display colorful
```

### Json structure
```json
[
  {
    "title": "Yahoo News - Latest News & Headlines",
    "link": "https://www.yahoo.com/news",
    "items":
      [
        {
          "title": "Sorry, Hillary: Democrats don&#39;t need a savior",
          "link": "https://news.yahoo.com/sorry-hillary-democrats-dont-need-a-savior-194253123.html",
          "author": "no author",
          "published_parsed": [2019, 11, 13, 19, 42, 53, 2, 317, 0],
          "description": "With the Iowa caucuses fast approaching, Hillary Clinton is just the latest in the colorful cast of characters who seem to have surveyed the sprawling Democratic field, sensed something lacking and decided that \u201csomething\u201d might be them.",
          "img_links":
            [
              "http://l.yimg.com/uu/api/res/1.2/xq3Ser6KXPfV6aeoxbq9Uw--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzMDs-/https://media-mbst-pub-ue1.s3.amazonaws.com/creatr-uploaded-images/2019-11/14586fd0-064d-11ea-b7df-7288f8d8c1a7"
            ]
        }
      ]
  }
]
```
### Cashing
The news is saved to the database when news output commands are executed. MongoDB is used as a database management system.
When the --date parameter is used, news is downloaded from the database by the entered date and the entered RSS link.

Features:
* The --limit parameter affects the amount of data loaded into the database.
* Date must be written in the yearmonthday (example - 19991113) format.

### Saving in files
Using the "--to_html" and "--to_fb2" parameters, you can save files at a given path.
The path should be written in the style of UNIX systems (example: ./some/folder).
File names are formed using the "feed[index].[format]" template (example: feed13.html).
File indices go sequentially and a new file fills this sequence or is set to the end.
What does this mean: if, for example, there are files "feed1.html" and "feed3.html",
a new file will be created with the name "feed2.html".