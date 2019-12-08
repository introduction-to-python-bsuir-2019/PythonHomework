# RSS reader

Python RSS reader - command-line utility.

## [Usage]:
  * positional\required arguments:
    * source .. RSS URL
  * optional arguments:
    * -h, --help .. Show help message and exit.
    * --version  .. Print version info.
    * --json     .. Print result as JSON in stdout.
    * --verbose  .. Outputs verbose status messages.
    * --limit    .. Limit news topics if this parameter is provided.
    * --date     .. Return cached news from the specified day. Format is YYYYMMDD.
    * --to-html  .. Convert news into html format and save a file to the specified path.
    * --to-pdf   .. Convert news into pdf format and save a file to the specified path.
    * --colorize .. Output in colorized mode
 
 ## [Cache]
   Cached Rss feeds are stored in `~/.rss-reader` folder in `cache.db` file. Cache use sqllite3 for storing Rss feeds.
   When you run utility cache module always storing or updating [if news already exists] parsing news from Rss feed.

## [Converter]
   News can be converted into `HTML` and `PDF` formats. If the file already exists at the specified path, it will be overwritten.

 
 ## [JSON structure]
<pre>
{
  "title": "Yahoo News - Latest News & Headlines",
  "url": "https://news.yahoo.com/rss/",
  "image": "http://l.yimg.com/rz/d/yahoo_news_en-US_s_f_p_168x21_news.png",
  "entries": [
    {
      "entry": {
        "link": "https://news.yahoo.com/1-protesters-burn-tyres-southern-113205795.html",
        "body": {
          "title": "UPDATE 3-Iraq protesters burn shrine entrance in holy city, PM quitting 'not enough'",
          "date": "Sat, 30 Nov 2019 - [11:32:05]",
          "links": [
            {
              "rel": "alternate",
              "type": "text/html",
              "href": "https://news.yahoo.com/1-protesters-burn-tyres-southern-113205795.html"
            }
          ],
          "media": [],
          "description": "Iraqi protesters set fire to the entrance of a shrine in the southern holy city of Najaf on Saturday and security forces fired tear gas to disperse them, police and a demonstrator at the scene said, risking more bloodshed after a rare day of calm.  The demonstrator sent a video to Reuters of a doorway to the Hakim shrine blazing as protesters cheered and filmed it on their mobile phones.  The incident took place during one of the bloodiest weeks of Iraq\u2019s anti-government unrest, which erupted last month."
        }
      }
    }
  ]
}

</pre>
