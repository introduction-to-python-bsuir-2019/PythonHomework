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
  {"title": "Yahoo News - Latest News & Headlines", 
    "link": "https://www.yahoo.com/news",
    "items":
      [
        {"title": "CouldPresident Trump be impeached and removed from office \u2014 but still reelected?",
         "link": "https://news.yahoo.com/could-president-trump-be-impeached-and-removed-from-office-but-still-reelected-184643831.html",
          "author": "no author",
          "published": "Tue, 12 Nov 2019 13:46:43 -0500",
          "description": "What happens when a presidentialimpeachment inquiry runs into a presidential election year? The United States in uncharted territory.",
          "img_links": 
            [
              "http://l2.yimg.com/uu/api/res/1.2/7LKu1VqFsBWR.ZGGf.U.zQ--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzMDs-/https://s.yimg.com/os/creatr-images/2019-11/fae1bf00-0581-11ea-93ff-f43ed8c16284"
            ]
         }
      ]
  }
]
```

