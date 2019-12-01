# euseand's RSS-reader
My RSS-reader is a command line utility which parses RSS URL and prints news in human-readable format.
## installation
You can use pip to install my package from test pypi index:
```bash
pip install --extra-index-url https://test.pypi.org/simple/ rss-reader-euseand==0.413
```
Or simply clone the repo and use pip install:
```bash
git clone --branch FinalTask https://github.com/euseand/PythonHomework.git
pip install .
``` 
## usage
Print 10(default limit) news from default (yahoo) online feed:
```bash
rss-reader ""
```
Print 10 news from online feed and store it in HTML-page (with additional verbosity):
```bash
rss-reader "https://news.yahoo.com/rss/" --limit 10 --verbose --to-html
```
Print 10 news from online feed and store it in PDF-file (with additional verbosity):
```bash
rss-reader "https://news.yahoo.com/rss/" --limit 10 --verbose --to-pdf
```
Print 10 news from cached feed and store it in HTML-page:
```bash
rss-reader "https://news.yahoo.com/rss/" --limit 10 --date 20191129
```
## feed examples (tested):
```bash
https://news.google.com/news/rss
https://news.yahoo.com/rss/
```
## JSON structure:
```
{"news": [
    {
     "feed": "Yahoo News - Latest News & Headlines",
     "url": "https://news.yahoo.com/rss/",
     "news_objects": [
      {
       "title": "Saudi Arabia takes over G20 presidency from Japan",
       "date": "Sun, 01 Dec 2019 05:33:38 -0500",
       "url": "https://news.yahoo.com/saudi-arabia-takes-over-g20-presidency-japan-103338011.html",
       "description": "Saudi Arabia became the first Arab nation Sunday to take over the G20 presidency as it seeks to bounce back onto the world stage following global uproar ov
    er its human rights record.  The oil-rich kingdom has promoted a liberalisation drive, including granting greater rights to women, but faced strong criticism over a crackdown
     on dissent and the murder last year of journalist Jamal Khashoggi.  The G20 presidency, which Saudi Arabia takes over from Japan, will see it host world leaders for a global
     summit in its capital next November 21-22.",
       "links": [
        {
         "id": 0,
         "url": "https://news.yahoo.com/saudi-arabia-takes-over-g20-presidency-japan-103338011.html",
         "type": "link"
        },
        {
         "id": 1,
         "url": "http://l2.yimg.com/uu/api/res/1.2/QZTf5K9T_TdjPVgXGViQTA--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzMDs-/http://media.zenfs.com/en_us/News/afp.com/7db623080129f4f56ad714f
    f06872a44e144fb03.jpg",
         "type": "image",
         "alt": "Saudi Arabia takes over G20 presidency from Japan"
        }
       ]
      }
     ]
    }
 ]
}
```