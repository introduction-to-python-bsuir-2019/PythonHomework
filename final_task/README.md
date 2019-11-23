##### JSON structure

```
{
  "news": {
    "feed": "Yahoo News - Latest News & Headlines",
    "publications": [
      {
        "title": "Stefanik embraces spotlight at impeachment hearings",
        "pub_date": "Fri, 15 Nov 2019 17:55:51 -0500",
        "link": "https://news.yahoo.com/stefanik-embraces-spotlight-at-impeachment-hearings-225551297.html",
        "description": "[image 2: Stefanik embraces spotlight at impeachment hearings] [2]\nThe second day of the impeachment inquiry\u2019s public hearings, on Friday, began the same way\nas the first: with an attempt by Rep. Elise Stefanik, a New York Republican, to interrupt proceedings\nwith a procedural objection.",
        "hrefs": [
          [
            "https://news.yahoo.com/stefanik-embraces-spotlight-at-impeachment-hearings-225551297.html",
            "link"
          ],
          [
            "http://l.yimg.com/uu/api/res/1.2/NRuDo56c6EiwjZH4WOqEZg--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzMDs-/https://media-mbst-pub-ue1.s3.amazonaws.com/creatr-uploaded-images/2019-11/7a1d0760-07d6-11ea-bef7-f17150574bb2",
            "image",
            "Stefanik embraces spotlight at impeachment hearings"
          ]
        ]
      }
    ]
  }
}
```

##### Cache description

News received from feed is cached through database is being created locally.

The database consists of the only file named "cache.db". It has the following structure:

     |  id  | feed | title | pub_date | pub_parsed | link | description | hrefs 
-----|------|------|-------|----------|------------|------|-------------|--------
post |  ..  | ...  |  ...  |   ...    |    ...     | ...  |     ...     |   ...    

All fields except "id" have text type. ID field plays a role of post primary key.

Hrefs field is composed of all post links including image links and image descriptions.
Usual references section and one for image links are separated by --|-- sequence. 
Items in one section are separated by -+- sequence. And -|- is for dividing link, it's type and image description.
