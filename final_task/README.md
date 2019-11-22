<h4><b>[Iteration 3] One-shot command-line RSS reader.</b></h4>

<h5>Utility interface</h5>

<pre>
usage: rss_reader.py [-h] [--version] [--json] [--verbose] [--limit LIMIT] [--date DATE] source

Pure Python command-line RSS rss_reader.

positional arguments:
  source         RSS URL

optional arguments:
  -h, --help     show this help message and exit
  --version      Print version info
  --json         Print result as JSON in stdout
  --verbose      Output verbose status messages
  --limit LIMIT  Limit news topics if this parameter provided
  --date DATE    Get news by date (date format: "yyyymmdd")
</pre>

<h5>JSON structure</h5>
<pre>
{
  "news": {
    "feed": "Yahoo News - Latest News & Headlines",
    "items": [
      {
        "title": "PHOTOS: Deadly shooting at California football party",
        "date": [
          2019,
          11,
          18,
          13,
          9,
          9,
          0,
          322,
          0
        ],
        "source": "https://news.yahoo.com/photos-deadly-shooting-at-california-football-party-130909246.html",
        "content": {
          "text": "Four people were killed and six more wounded when \u201cunknown suspects\u201d sneaked into a backyard filled with people at a party in central California and fired into the crowd, police said.",
          "images": [
            {
              "link": "http://l.yimg.com/uu/api/res/1.2/zk3Vm4IumKHd15y_m9XXFQ--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzMDs-/https://media-mbst-pub-ue1.s3.amazonaws.com/creatr-uploaded-images/2019-11/53b14e90-0a03-11ea-9a77-714a8e20d9a5",
              "alt": "PHOTOS: Deadly shooting at California football party"
            }
          ],
          "links": [
            "https://news.yahoo.com/photos-deadly-shooting-at-california-football-party-130909246.html"
          ]
        }
      }
    ]
  },
  "source": "https://news.yahoo.com/rss/"
}
</pre>

<li>This package exports CLI utility rss-reader</li> 