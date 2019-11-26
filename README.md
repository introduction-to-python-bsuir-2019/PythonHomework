## It is a one-shot command-line RSS reader by Zviger.
### Installation
Clone this repository and run setup.py file with parameters "install --user"
or
Download docker [https://docs.docker.com/] and docker-compose [https://docs.docker.com/compose/install/]
after this run command:
```text
docker-compose up -d
```
and
```text
docker exec -it rss_reader bash (this command u will run every time, when u need to use reader)
```
Fine!

Now you can write in the docker console "rss_reader" with some parameters
### User interface
```text
usage: rss_reader [-h] [--version] [-l LIMIT] [--verbose] [--json] [--length LENGTH] [--date DATE] source

It is a python command-line rss reader

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
  --date DATE           Search past news by date in format yeardaymonth (19991311)

```

### Json structure
```json
[
  {
    "title": "Yahoo News - Latest News & Headlines",
    "link": "https://www.yahoo.com/news",
    "items":
      [
        {
          "title": "Sorry, Hillary: Democrats don&#39;t need a savior",
          "link": "https://news.yahoo.com/sorry-hillary-democrats-dont-need-a-savior-194253123.html",
          "author": "no author",
          "published_parsed": [2019, 11, 13, 19, 42, 53, 2, 317, 0],
          "description": "With the Iowa caucuses fast approaching, Hillary Clinton is just the latest in the colorful cast of characters who seem to have surveyed the sprawling Democratic field, sensed something lacking and decided that \u201csomething\u201d might be them.",
          "img_links":
            [
              "http://l.yimg.com/uu/api/res/1.2/xq3Ser6KXPfV6aeoxbq9Uw--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzMDs-/https://media-mbst-pub-ue1.s3.amazonaws.com/creatr-uploaded-images/2019-11/14586fd0-064d-11ea-b7df-7288f8d8c1a7"
            ]
        }
      ]
  }
]
```
### Cashing
The news is saved to the database when news output commands are executed. MongoDB is used as a database management system.
When the --date parameter is used, news is downloaded from the database by the entered date and the entered RSS link.

Features:
* The --limit parameter affects the amount of data loaded into the database.
* Date must be written in the yearmonthday (example - 19991113) format. 
