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
    "feed_title": "Yahoo News - Latest News & Headlines",
    "feed_link": "https://www.yahoo.com/news",
    "items":
    [
      {
        "item_title": "Top House Armed Services Republican: Trump&#39;s Ukraine call was &#39;inappropriate&#39; but not impeachable",
        "item_link": "https://news.yahoo.com/trump-impeachment-mac-thornberry-abc-this-week-165743982.html",
        "item_author": null, "item_description": "Rep. Mac Thornberry, R-Texas, said President Trump's call with Ukraine'spresident was \"inappropriate\" — but it did not warrant his impeachment.",
        "item_date": "Sun, 10 Nov 2019 11:57:43-0500", "item_img_links":
        [
          "http://l1.yimg.com/uu/api/res/1.2/nZ9ESccFgs8cyvX3b2LOUA--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzMDs-/https://media-mbst-pub-ue1.s3.amazonaws.com/creatr-uploaded-images/2019-11/922d39a0-03db-11ea-bf1e-9fbc638c65a1"
        ]
       }
    ]
  }
]
```

