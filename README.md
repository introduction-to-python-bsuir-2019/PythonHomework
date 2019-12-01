# Welcome
This project was created for the EPAM Python Courses 2019.

## Installing

First, this app runs on Python version >=3.8.

### Download:

`git clone https://github.com/TeRRoRlsT/PythonHomework.git`

### Setup:
Go to repository **PythonHomework** and execute the command:

`python3.8 -m pip install .` 

or

`pip install .` 

## Running
To view the help for running project go to **PythonHomework/rssreader** folder and execute the command:

`python3.8 rss_reader.py --help`

### SQLite3
This application uses SQLite3 database to cache all downloaded news articles.
If you use '--date YYYYMMDD' the application will load news articles from the DB with the date after the given date.

## Tests
For run unittest go to **PythonHomework** folder and execute the command:

`python3.8 -m unittest tests`

 ## Authors
* Sergey Pivovar - BSUIR 2019