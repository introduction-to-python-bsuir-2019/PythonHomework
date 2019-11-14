## It is a one-shot command-line RSS reader by Zviger.
### Installation
```text
Clone this repository and run setup.py file with parameters "install --user"
```
### User interface
```text
usage: frbz.py [-h] [--version] [-l LIMIT] [--verbose] [--json] [--length LENGTH] source

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

