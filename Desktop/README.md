# Desktop-Console-Utility
---

## Installation of application

You can install utility if you have python3.6 and higher.

Example of installation:
    
    $ git clone https://github.com/Elaskinok/PythonHomework.git --branch rss_reader
    $ cd PythonHomework/Desktop
    $ pip3 install .
   
After installation you may to call application everywhere, where ever you are.

## Running application

For running Rss Reader you should enter command:

    $ rss-reader [url] [option]

For getting help:
    
    $ rss-reader
    $ rss-reader -h
    $ rss-reader --help
(These are the same ways)
 
## Application features

Utility provides the following interface:

- positional arguments:

|argument|description|
|---|---|
|link | Link on RSS resource|

- optional arguments:

|argument|description|
|---|---|
|-h, --help     |       Display this help message and exit
|  -v, --version   |      Print version info
|  --json         |       Print result as JSON in stdout
|  -l LIMIT, --limit LIMIT|  Limit news topics if this parameter provided
|  --date DATE      |     Argument, which allows to get cashed news by date. Format: YYYYMMDD. For getting list of existing dates you can enter any value with this argument. For example: '$ rssreader --date .' 
|  -V, --verbose     |    Print all logs in stdout
| --colorize        |    Print news with colorize mode. It's works only with default output. Sorry, but you can not change colors :( Wait for update...
|  --to_fb2 PATH    |     Convert news to fb2 format. Path must contain exsisting directories Supports LIMIT
|  --to_pdf PATH   |      Convert news to pdf format. Convertation to PDF supports only latin resource. Path must contain exsisting directories Supports LIMIT|

### Be careful! Convartation to fb2 and pdf is slow, because these processes works with images! Advice you use --limit with these options.
