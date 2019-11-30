# RSS reader

RSS reader is a command-line utility which receives RSS URL and prints results in human-readable format.

## Specification
<pre>
usage: rss_reader.py [-h] [--version] [--json] [--verbose] [--limit LIMIT]
                     source

Pure Python command-line RSS reader.

positional arguments:
  source         RSS URL

ooptional arguments:
  -h, --help         show this help message and exit
  --version          Print version info
  --json             Print result as JSON in stdout
  --verbose          Outputs verbose status messages
  --limit LIMIT      Limit news topics if this parameter provided
  --date DATE        Take a date in %Y%m%d format. The news from the specified
                     day will be printed out.
  --to-html TO_HTML  Convert news into html and print in stdout. Argument
                     receives the path where new file will be saved.
  --to-fb2 TO_FB2    Convert news into fb2 and print in stdout. Argument
                     receives the path where new file will be saved.

</pre>

## News caching
The RSS news are stored in a local storage while reading. Local storage is implemented using shelve. The cached news are dicts with the news itself and its row (html) description which are stored by key. The key consists of date and RSS URL. The cashed news can be read with optional argument --date. Utility creates binary db file 'cache.db' in current directory. If you change current directory, db file from previoгs will not be copied to the current directory.

## JSON structure
<pre>
{
    "news": {
        "feed": "TUT.BY: Новости ТУТ - Главные новости",
        "items": [
            {
                "title": "Охрана, неприкосновенность, пенсия. Канопацкая предлагает закон о гарантиях для экс-президента Беларуси",
                "link": "https://news.tut.by/economics/662957.html?utm_campaign=news-feed&utm_medium=rss&utm_source=rss-news",
                "date": "Wed, 27 Nov 2019 15:41:00 +0300",
                "description": {
                    "text": "Депутат Анна Канопацкая разработала законопроект «О гарантиях президенту Республики Беларусь, прекратившему исполнение своих полномочий, и членам его семьи» и в ближайшее время внесет его на рассмотрение в Палату представителей.",
                    "images": [
                        {
                            "src": "https://img.tyt.by/thumbnails/n/politika/04/4/c5109116a72e8f8029fecf5ca544c9d4.jpg",
                            "alt": "Фото: sb.by"
                        }
                    ],
                    "links": null
                }
            }
        ]
    }
}
</pre>
