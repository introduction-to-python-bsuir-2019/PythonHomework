import feedparser
import json
import html
from bs4 import BeautifulSoup
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from arg import args
from loggerfile import log
from cache import sql_connection, sql_fetch
from version import version_info


def parse():
    '''Returns URL ADDRESS'''
    parse_arg = args()
    return feedparser.parse(parse_arg.source)


def get_source(parsed):
    '''Gets link, title and subtitle from the executing URL'''
    feed = parsed['feed']
    try:
        return ({
            'link': feed['link'],
            'title': feed['title'],
            'subtitle': feed['subtitle']
        })
    except:
        print('')


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
                'Title': html.unescape(entry['title']),
                'Description': text,
                'Published': entry['published'],
                'article IMG': article_img,
            })
        return articles
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
        try:
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
        except:
            print('')
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


def sql_table(con, parsed, sql_args, sql_logs):
    '''Initialise database if it's not created yet and
     entering information into it'''
    articles = get_articles(parsed)
    cursorObj = con.cursor()
    try:
        cursorObj.execute("CREATE TABLE IF NOT EXISTS news(title, published, link, description)")
    finally:
        if sql_args.source:
            for article in articles[0:]:
                entities = (article['Title'], article['Published'],
                            article['Link'], article['Description'], )
                cursorObj.execute('INSERT OR IGNORE INTO news(title,'
                                    'published, link, description) VALUES(?, ?, ?, ?)', entities)
            if sql_args.verbose:
                sql_logs.info('Caching news')
                sql_logs.info('News cached successfully')
    con.commit()


def cache_main(info):
    '''Function to call others connected with cache'''
    con = sql_connection()
    sql_fetch(con)


def to_pdf(articles, agrs_conv):
    '''Function that should convert into pdf
     But it's very poor and I done '''
    pdf = canvas.Canvas('Test.pdf')
    pdf.setTitle('Converter to PDF')
    pdfmetrics.registerFont(
        TTFont('abc', 'SakBunderan.ttf')
    )
    pdf.setFont('abc', 12)
    for article in articles[0:agrs_conv.limit]:
        pdf.drawCentredString(300, 770, article['Title'])
        textobject = pdf.beginText(40, 680)
        textobject.setFont("Helvetica-Oblique", 14)
        for line in article['Description']:
            textobject.textOut(line)
    pdf.save()


def start():
    '''Function which calls when --to_pdf argument entered'''
    to_pdf(get_articles(parse()),args())


def main():
    '''Heart of the project'''
    console_args = args()
    logs = log()
    con = sql_connection()
    if console_args.json:
        print_articles_json(parse(), console_args, logs)
        sql_table(con, parse(), console_args, logs)
    else:
        print_articles(parse(), console_args, logs)
        sql_table(con, parse(), console_args, logs)
    if console_args.version:
        version_info(parse())
    if console_args.date:
        cache_main(parse())
    if console_args.to_pdf:
        start()


if __name__ == "__main__":
    main()
