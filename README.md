# RSS-reader
RSS reader is a command-line utility which receives RSS URL and prints results in human-readable format.
## Installation
Upgrade the package manager pip up to the latest version.  
```bash
python -m pip install --upgrade pip
``` 
Use the pip to install rss-reader.
```bash
python -m pip install --extra https://test.pypi.org/simple/ rss-reader-kis==1.88
``` 
## Usage
### Print first 2 news
```bash
rss-reader "https://news.yahoo.com/rss/" --limit 2 
```
### Load from cache by date
```bash
rss-reader "https://news.yahoo.com/rss/" --date 20191201 
```
### Convert to html format
```bash
rss-reader "https://news.yahoo.com/rss/" --to-html "D:" 
```
### Convert to fb2 format
```bash
rss-reader "https://news.yahoo.com/rss/" --to-fb2 "D:" 
```
### Print in json format
```bash
rss-reader "https://news.yahoo.com/rss/" --json 
```
## Json structure
```
{
 "news": [
  {
   "feed_name": "Yahoo News - Latest News & Headlines",
   "title": "MSNBC confuses ex-Trump navy secretary for infamous white supremacist",
   "date": "Sun, 01 Dec 2019 13:14:35 -0500",
   "link": "https://news.yahoo.com/msnbc-confuses-ex-trump-navy-secretary-for-infamous-white-supremacist-181435331.html",
   "image_title": "MSNBC confuses ex-Trump navy secretary for infamous white supremacist",
   "image_description": "MSNBC mistook two notable men with the same name, Richard Spencer., a now-former navy secretary and Richard Spencer, a white supremacist.",
   "image_link": "http://l2.yimg.com/uu/api/res/1.2/hed3UxVsjGElE_4eA2zkCQ--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzMDs-/https://media-mbst-pub-ue1.s3.amazonaws.com/creatr-uploaded-images/2019-12/7703b4a0-1467-11ea-b376-8a5026520f44"
  }
 ]
}
```
## Promotion
Star are welcome.