#Introduction to Python. Hometask

RSS reader is a command-line utility which receives RSS URL and prints results in human-readable format.

Utility provides the following interface:

usage: rss_reader.py [-h] [--version] [--json] [--verbose] [--limit LIMIT] [--date DATE] [--colorize] [--to-fb2] [--to-pdf]
                     source

Pure Python command-line RSS reader.

positional arguments:
  source         RSS URL

optional arguments:
  -h, --help     Show this help message and exit
  --version      Print version info
  --json         Print result as JSON in stdout
  --verbose      Outputs verbose status messages
  --limit LIMIT  Limit news topics if this parameter provided
  --date DATE    Print news topics for a specific date  
  --colorize     Print the result of the utility in colorized mode
  --to-fb2       In the activated state, the program creates a News.fb2 file in the working directory
  --to-pdf       In the activated state, the program creates a News.pdf file in the working directory
  
Json schema:
{
    "definitions": {},
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "http://example.com/root.json",
    "type": "object",
    "title": "The Root Schema",
    "required": [
      "feed",
      "link",
      "title",
      "date",
      "description",
      "image_url"
    ],
    "properties": {
      "feed": {
        "$id": "#/properties/feed",
        "type": "string",
        "title": "The feed Schema",
        "default": "",
        "examples": [
          "Yahoo News - Latest News & Headlines"
        ],
        "pattern": "^(.*)$"
      },
      "link": {
        "$id": "#/properties/link",
        "type": "string",
        "title": "The link Schema",
        "default": "",
        "examples": [
          "https://news.yahoo.com/trump-impeachment-mac-thornberry-abc-this-week-165743982.html"
        ],
        "pattern": "^(.*)$"
      },
      "title": {
        "$id": "#/properties/title",
        "type": "string",
        "title": "The title Schema",
        "default": "",
        "examples": [
          "Top House Armed Services Republican: Trump's Ukraine call was 'inappropriate' but not impeachable"
        ],
        "pattern": "^(.*)$"
      },
      "date": {
        "$id": "#/properties/date",
        "type": "string",
        "title": "The date Schema",
        "default": "",
        "examples": [
          "Sun, 10 Nov 2019 11:57:43 -0500"
        ],
        "pattern": "^(.*)$"
      },
      "description": {
        "$id": "#/properties/description",
        "type": "string",
        "title": "The description Schema",
        "default": "",
        "examples": [
          "Rep. Mac Thornberry, R-Texas, said President Trumps call with Ukraines president was inappropriate — but it did not warrant his impeachment."
        ],
        "pattern": "^(.*)$"
      },
      "image_url": {
        "$id": "#/properties/image_url",
        "type": "array",
        "title": "The image_url Schema",
        "items": {
          "$id": "#/properties/image_url/items",
          "type": "string",
          "title": "The items Schema",
          "default": "",
          "examples": [
            "http://l1.yimg.com/uu/api/res/1.2/pprhLmQfU6bmFDTaOGZZ6w--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzMDs-/https://media.zenfs.com/en/the_national_interest_705/d2d976b857f599d16444382365feefc1"
          ],
          "pattern": "^(.*)$"
        }
      }
    }
  }

