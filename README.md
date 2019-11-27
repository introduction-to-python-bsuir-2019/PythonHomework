# Rss news reader

This is a project for news reading using Python. There you can 
find command line utility. And Django web application.

## Getting Started

To download project:
```
git clone https://github.com/Vadbeg/PythonHomework.git 
```


### Installing
To install all libraries you need to use this package, print in package tree: 

```
pip install .
```

### CLU Usage

After installation you can use script for getting news from rss url 

```
>> rss_reader --help

usage: rss_reader [-h] [--version] [--json] [--verbose] [--caching]
                  [--colorful] [--limit LIMIT] [--date DATE] [--to-pdf TO_PDF]
                  [--to-html TO_HTML] [--to-fb2 TO_FB2]
                  source

Pure Python command-line RSS reader

positional arguments:
  source             RSS URL

optional arguments:
  -h, --help         show this help message and exit
  --version          Print version info
  --json             Print result as json in stdout
  --verbose          Output verbose status messages
  --caching          Cache news if chosen
  --colorful         Colorize output
  --limit LIMIT      Limit news topics if this parameter provided
  --date DATE        Reads cashed news by date. And output them
  --to-pdf TO_PDF    Read rss by url and write it into pdf. Print file name as
                     input
  --to-html TO_HTML  Read rss by url and write it into html. Print file name
                     as input
  --to-fb2 TO_FB2    Read rss by url and write it into fb2. Print file name as
                     input
```

Example of usage:

```
>> rss_reader "https://news.yahoo.com/rss/" --limit 2

News feed is ready
Feed: Yahoo News - Latest News & Headlines
____________________________________________________________________________________________________
____________________________________________________________________________________________________

        Title: Fox News&#39; Wallace calls out GOP senator for pushing debunked conspiracy theory
        Date: Sun, 24 Nov 2019 13:20:36 -0500
        Link: https://news.yahoo.com/fox-news-wallace-calls-out-gop-senator-for-pushing-debunked-conspiracy-182036006.html

        Image link: http://l.yimg.com/uu/api/res/1.2/8ChsXkGBxAcADn5S4Ig8dA--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzMDs-/https://media-mbst-pub-ue1.s3.amazonaws.com/creatr-uploaded-images/2019-11/3cfbe6f0-0ee6-11ea-bdfd-e3033f7dee57
        Image description: Fox News' Wallace calls out GOP senator for pushing debunked conspiracy theory
        Description: Fox News host Chris Wallace pushed back against GOP Senator John Kennedy, who repeated a debunked conspiracy theory promoted by President Trump. 
____________________________________________________________________________________________________

        Title: Guards charged over Epstein&#39;s suicide get trial date
        Date: Mon, 25 Nov 2019 13:54:40 -0500
        Link: https://news.yahoo.com/guards-charged-over-epsteins-suicide-185440082.html

        Image link: http://l2.yimg.com/uu/api/res/1.2/RWUv7dCaeUojowUdU.sMqA--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzMDs-/https://media.zenfs.com/en-US/reuters.com/055598e0d7f37ed77d700669fa2d2560
        Image description: Guards charged over Epstein's suicide get trial date
        Description: Two correctional officers accused of covering up their failure to check on financier Jeffrey Epstein before he hanged himself will face an April 20 trial date.  U.S. District Judge Analisa Torres scheduled the trial for Tova Noel and Michael Thomas at a hearing in Manhattan federal court on Monday.  Epstein's suicide on Aug. 10, at age 66, came a little over a month after the well-connected money manager was arrested and charged with trafficking dozens of underage girls as young as 14 from at least 2002 to 2005.
____________________________________________________________________________________________________
```
## Web application usage
To start web application input next commands:

```
>> cd newsfeed
>> python manage.py runserver
```

## Tests:
To run unittests go to news_feed directory and print in console:

```
>> python rss_reader_unittest.py
```


## Built With

* [Django](https://docs.djangoproject.com/en/2.2/) - The web framework used


## Authors

* **Vadim Titko** aka *Vadbeg* - [GitHub](https://github.com/Vadbeg/PythonHomework/commits?author=Vadbeg)
 
