# RSS reader
RSS reader is a command-line utility that retrieves the RSS URL and prints the results in a human-readable format.

## Distribution
The program is located in module rssreader. When unpacking, it is installed in the system. After installation, to start using the program, write rss-reader to the terminal.

## Specification
The program works with command line arguments. Their description:

**usage:** rss-reader \[-h] \[--version] \[--json] \[--verbose] \[--limit *LIMIT*] source

+ Positionalarguments:
    + source => RSS URL

+ Optional arguments:
    + -h, --help => Show help message and exit. Сan be used as a single argument.
    + --version => Print version info. Сan be used as a single argument.
    + --json => Print result as JSON in stdout.
    + --verbose => Outputs verbose status messages. Use with other arguments.
    + --limit LIMIT => Limit news topics if this parameter is provided LIMIT.
    + --date DATE => Return cached news from the publication day. Format is YYYYMMDD". **Argument source has the meaning**.
    + --to-html => Convert news to html. Return file parsing_news.hmtl
    + --to-pdf => Convert news to pdf. Return parsing_news.pdf
    + --colorize => Print the result of the utility in colorized mode.

+ Additional description:
    + --limit => can be used with --json, --date, --to-pdf, --to-html.
    + --json => the description of the circuit is in the file **parsing_json_schema.json**
    + --date => can be used with --json, --limit, --to-pdf, --to-html.
    + --verbose => can be used with all agruments.
    + --colorize => use argument without --json. Because json will not be color.

For example you can use a super combination:
```bash
    source --limit LIMIT --json --date Date --to-pdf --to-html
```
## Get files from container

```bash
docker cp my_app:/code/parsing_news.pdf parsing_news.pdf
docker cp my_app:/code/parsing_news.html parsing_news.html
```

## Database check

Go to your browser at. Only after starting the application at least 1 time
```bash
http://0.0.0.0:8081/db/news/news_received
```

## Testing

Test find in the most important folder.

Write before tests
```bash
    pip install .
```
To test the package enter the command:
```bash
    nosetests --with-coverage --cover-erase --cover-package=rssreader
```
You can test internal packages as well: 
```bash
    --cover-package=rssreader.parser
```
