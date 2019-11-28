import feedparser
import json
from bs4 import BeautifulSoup
from arg import args
from loggerfile import log
from cache import sql_connection, sql_table, sql_fetch
from version import version_info


def parse():
    '''Returns URL ADDRESS'''
    parse_arg = args()
    return feedparser.parse(parse_arg.source)


def get_source(parsed):
    '''Gets link, title and subtitle from the executing URL'''
    feed = parsed['feed']
    return ({
        'link': feed['link'],
        'title': feed['title'],
        'subtitle': feed['subtitle']
    })


def get_articles(parsed):
    '''Gets information from the article and returns this'''
    articles = []
    entries = parsed['entries']
    try:
        for entry in entries:
            img = BeautifulSoup(entry.summary, features="html.parser")
            article_img = img.find('img')['src']
            text = BeautifulSoup(entry.summary, features='html.parser').text
            articles.append({
                'ID': entry['id'],
                'Link': entry['link'],
                'Title': entry['title'].replace('&#39;', "'"),
                'Description': text,
                'Published': entry['published'],
                'article IMG': article_img,
            })
    finally:
        for entry in entries:
            text = BeautifulSoup(entry.summary, features='html.parser').text
            articles.append({
                'ID': entry['id'],
                'Link': entry['link'],
                'Title': entry['title'].replace('&#39;', "'"),
                'Description': text,
                'Published': entry['published'],
            })
        return articles


def print_articles(parsed, args_ord, logs_art):
    '''Function to output information'''
    articles = get_articles(parsed)
    feed = get_source(parsed)
    if args_ord.limit == 0:
        print('Error, argument should be more than zero')
    else:
        print('----------' + feed['title'] + '----------\n')
        print('URL ADDRESS: ' + feed['link'] + '\n')
        print(feed['subtitle'])
        for article in articles[0:args_ord.limit]:
            print("\nTitle: ", article['Title'])
            print("Date: ", article['Published'])
            print("Link: ", article['Link'])
            print("\nDescription: ", article['Description'])
            try:
                print("\nImage: ", article['article IMG'])
            except:
                print('\nNo images given')
            print('\n')
        if args_ord.verbose:
            logs_art.info('Program started with source: ' + feed['link'])
            logs_art.info('Limit is {}'.format(args_ord.limit))
            logs_art.info('News in ordinary format parsed successfully ')


def print_articles_json(parsed, args_json, logs_json):
    '''Function to output information in JSON format'''
    feed = get_source(parsed)
    if args_json.limit == 0:
        print('Error, argument should be more than zero')
    else:
        print('----------' + feed['title'] + '----------')
        print('URL ADDRESS: ' + feed['link'] + '')
        print(feed['subtitle'])
        print(json.dumps(get_articles(parse())[0:args_json.limit], indent=3, ensure_ascii=False, ))
    if args_json.verbose:
        logs_json.info('Program started with source: ' + feed['link'])
        logs_json.info('Limit is {}'.format(args_json.limit))
        logs_json.info('News in json format parsed successfully ')


def getting_info(parsed):
    articles = get_articles(parsed)
    for article in articles[0:]:
        entities = (article['Title'], article['Published'],
                    article['Link'], article['Description'])
    return entities


def cache_main(info):
    con = sql_connection()
    sql_table(con, info)
    sql_fetch(con)


def main():
    console_args = args()
    logs = log()
    if console_args.json:
        print_articles_json(parse(), console_args, logs)
    else:
        print_articles(parse(), console_args, logs)
    if console_args.version:
        version_info(parse())
    if console_args.date:
        cache_main(getting_info(parse()))


if __name__ == "__main__":
    main()
