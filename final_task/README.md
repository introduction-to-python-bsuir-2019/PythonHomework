<h4><b>[Iteration 2] One-shot command-line RSS reader.</b></h4>

<h5>Utility interface</h5>

<pre>
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
</pre>

<h5>JSON structure</h5>
<pre>
{
  "news": {
    "feed": "Yahoo News - Latest News & Headlines",
    "items": [
      {
        "title": "Look out below: Which Democratic candidate will drop out next?",
        "date": "Tue, 05 Nov 2019 11:18:43 -0500",
        "source": "https://news.yahoo.com/look-out-below-which-democratic-candidate-will-drop-out-next-161843916.html",
        "content": {
          "text": "At first there were 26. Now there are \u201conly\u201d 17. Who will be the next Democratic presidential candidate to drop out?",
          "images": [
            {
              "link": "http://l1.yimg.com/uu/api/res/1.2/G95rCcy3tWXT.0Mf3yCsrA--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzMDs-/https://media-mbst-pub-ue1.s3.amazonaws.com/creatr-uploaded-images/2019-11/d2b0ba80-ffe2-11e9-b6ff-0e39e79953b2",
              "alt": "Look out below: Which Democratic candidate will drop out next?"
            }
          ],
          "links": [
            "https://news.yahoo.com/look-out-below-which-democratic-candidate-will-drop-out-next-161843916.html"
          ]
        }
      }
    ]
  }
}
</pre>

<li>This package exports CLI utility rss-reader</li> 