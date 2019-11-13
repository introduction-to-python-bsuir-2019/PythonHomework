# RSS reader

RSS reader is a command-line utility which receives RSS URL and prints results in human-readable format.

## Specification

usage: rss_reader.py [-h] [--version] [--json] [--verbose] [--limit LIMIT]
                     source

Pure Python command-line RSS reader.

positional arguments:
  source         RSS URL

optional arguments:
  -h, --help     show this help message and exit
  --version      Print version info
  --json         Print result as JSON in stdout
  --verbose      Outputs verbose status messages
  --limit LIMIT  Limit news topics if this parameter provided

## JSON structure

{
    "news": {
        "feed": "Yahoo News - Latest News & Headlines",
        "items": [
            {
                "title": "Ukrainian energy company tied to Hunter Biden supported American think tank, paid for trips",
                "link": "https://news.yahoo.com/ukrainian-energy-company-tied-to-hunter-biden-supported-american-think-tank-paid-for-trips-015132322.html",
                "date": "Tue, 12 Nov 2019 20:51:32 -0500",
                "description": {
                    "text": "Burisma gave more than $450,000 to the Atlantic Council, a prominent Washington think tank.",
                    "images": [
                        "http://l1.yimg.com/uu/api/res/1.2/2Q92DOIaZFmDeg0l9DbhAg--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzMDs-/https://media-mbst-pub-ue1.s3.amazonaws.com/creatr-images/2019-11/42dec8d0-05a9-11ea-adcf-9417cbbb4d35"
                    ],
                    "links": [
                        "https://news.yahoo.com/ukrainian-energy-company-tied-to-hunter-biden-supported-american-think-tank-paid-for-trips-015132322.html"
                    ]
                }
            }
        ]
    }
}
