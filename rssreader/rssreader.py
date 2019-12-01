import argparse
import logging
import urllib3
from bs4 import BeautifulSoup
import urllib.request
import sys
import json
from fpdf import FPDF
import os


def argsparsing():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="RSS URL", type=str)
    parser.add_argument("--version", action='version', version='%(prog)s ' + 'v 2.0', help="Print version info", )
    parser.add_argument("--json", help="Print result as JSON in stdout", action="store_true")
    parser.add_argument("--verbose", help="Outputs verbose status messages", action="store_true")
    parser.add_argument("--limit", type=int, help="Limit news topics if this parameter provided")
    parser.add_argument("--date", type=int, help="Read cashed news by date in next format YYMMDD")
    parser.add_argument('--html', type=str, help="Convert news to html and save in .html file.Path in format smth\\")
    parser.add_argument('--pdf', type=str, help="Convert news to pdf and save in .pdf file.Path in format smth\\")
    return parser.parse_args()


def making_log(operation, message, file='loglist.log'):
    """func can do 2 ops, if 1 to write if 0 to read"""
    if bool(operation):
        logging.basicConfig(filename=file, format='%(name)s - %(levelname)s - %(message)s-%(asctime)s',
                            level=logging.INFO)
        logging.info(message)
    else:
        print(open(file, 'r').read())


def spliting_items(lst, index1, tag):
    try:
        line_list = ''
        split_list = []
        split_list = str(tag+str(lst)).split(" ")
        for index in range(len(split_list)):
            if len(str(line_list)) < 120:
                line_list = line_list + " %s" % str(split_list[index])
            else:
                index1.cell(250, 10, line_list, ln=1, align="C")
                line_list = ''
        index1.cell(250, 10, line_list, ln=1, align="pos")
    except:
        making_log(1, "Cant't save feed with index=%d to index")
        print("Can't save news as index ;(")


class NewsRss:
    """Class with all parts of rss news and methods to work with its."""
    def __init__(self):
        self.arguments = argsparsing()
        self.title = []
        self.pubDate = []
        self.link = []
        self.desc = []
        self.links = []
        self.datalist = []

    def feed_find(self):
        try:
            urllib.request.urlopen(self.arguments.source)
        except:
            print("Error.URL is incorrect")
            exit(1)
        soup = BeautifulSoup(urllib.request.urlopen(self.arguments.source), "xml")
        making_log(1, "Opened URL for news reading, URL: %s" % self.arguments.source)
        try:
            list = soup.find_all("item")
        except:
            print("Error. Can't find <item> tag in URL. Try to use another URL for RSS parsing. ")
            exit(1)
        making_log(1, "Find all <item> tags in feed.")
        making_log(1, "Limit is: (%s)        " % (str(self.arguments.limit)))
        for cout, feed in enumerate(list):
            if cout != self.arguments.limit:
                making_log(1, "Opened feed on %s link." % feed.link.text)
                strmedia = str(feed.find_all("media:content"))
                tempstring = feed.description.text
                llink = []
                for i in range(strmedia.count('url="')):
                    llink.append(strmedia[(strmedia.find('url="')+5): (strmedia.find('"', (strmedia.find('url="')+5)))])
                self.links.append(str(llink))
                self.link.append(feed.link.text)
                tempstring = str(feed.description.text).replace("&#39;", "'").replace("&quot;", "'")
                tempstring.replace("&#92;", "\\")
                self.title.append(str(feed.title.text).replace("&#39;", "'").replace("&quot;", "'"))
                self.pubDate.append(feed.pubDate.text)
                self.desc.append(tempstring[(tempstring.find('a>') + 1):tempstring.find('<p><br')])
            else:
                making_log(1, "Iteration closed with code 0(all_goods)")
                break

    def convert_to_html(self):
        making_log(1, "Convertation to html opened.")
        try:
            for index in range(len(self.title)):
                image = str(self.links[index])
                image = image[2:-2]
                string = str(self.title[index])[:-2].replace("?", " ")
                string = string.replace(":", " ")
                filename = "%s%s.html" % (str(self.arguments.html), string)
                htmltext = """
    <html>
        <head>
                <title> %s </title>
        </head>
        <body>
                <h1> Title: %s </h1>
                <h4> Date: %s </h4>
                <h4> Link: %s </h4>
                <h4> Feed: %s </h4>
                <p><img src=%s width="400" height="400"></p>
        </body>
    </html>  
                """ % (str(self.title[index]), str(self.title[index]), str(self.pubDate[index]), str(self.link[index]), str(self.desc[index]), image)
                with open(filename, "w") as fp:
                    fp.write(htmltext)
        except:
            making_log(1, "Error. Some news not converted to html.")
        else: making_log(1, "All news converted to html.(all_goods)")

    def convert_to_pdf(self):
        for index in range(len(self.title)):
            try:
                string = str(self.title[index])[:-2].replace("?", " ")
                string = string.replace(":", " ")
                filename = "%s%s.pdf"%(str(self.arguments.pdf), string)
                http = urllib3.PoolManager()
                index1 = index
                index1 = FPDF(orientation="L")
                index1.add_page()
                index1.set_font("Arial", size=12)
                spliting_items(self.title[index], index1, "Title: ")
                spliting_items(self.pubDate[index], index1, "Date: ")
                spliting_items(self.link[index], index1, "Link: ")
                spliting_items(self.desc[index], index1, "Feed: ")
                image = str(self.links[index])
                image = image[2:-2]
                r = http.request('GET', image)            
                fileimage = "%s%s.jpg"%(str(self.arguments.pdf), string)
                fp = open(fileimage, "w+b")
                fp.write(r.data)
                try:
                    index1.image(fileimage, w=50)
                except: making_log(1, "Feed with index %s has a bad img format." % index)
                index1.output(filename)
            except: making_log(1, "Feed with index %s can't convert to pdf." % index)

    def print_news(self):
        making_log(1, "Print news in stdout opened.")
        try:
            for index in range(len(self.title)):
                if self.arguments.json:
                    print(json.dumps({"item": {"link":self.link[index], "body": {"title": self.title[index], "date": self.pubDate[index], "images": self.links[index], "feed": self.desc[index]}}}, indent=4))
                    print("\n\n\n")
                else:    
                    print("Title: " + self.title[index],
                            "\nDate: " + self.pubDate[index],
                            "\nLink: " + self.link[index])
                    print("Feed: " + self.desc[index])
                    if self.links != []:
                        print("Images: \n" + self.links[index])
                    print("\n\n\n")
        except:
            print("Error. Can't print news. Smth go bad ;(")
            making_log(1, "Error. Can't print news. Smth go bad ;(")
        else: making_log(1, "All news were printed.(all_goods)")    
    
    def date_check(self):
        if len(str(self.arguments.date)) > 8 or len(str(self.arguments.date)) < 8 :
            print("Error in date input")
            return False
        return True

    def filewrite(self):
        making_log(1, "Writing news in file opened. News saved in datafeed.txt")
        for index in range(len(self.title)):
                with open("data\datafeed.txt", "a") as fp:
                    try:
                        fp.write(str(self.pubDate[index]))
                        fp.write("\n")
                        fp.write(str(self.title[index]))
                        fp.write("\n")
                        fp.write(str(self.link[index]))
                        fp.write("\n")
                        fp.write(str(self.desc[index]))
                        fp.write("\n")
                        fp.write(str(self.links[index]))
                        fp.write("\n")
                    except:
                        making_log(1, "Error. Can't write feed with index=%s on file." % index)
                    else: making_log(1, "Feed wited in file.(all_goods)")

    def fileread(self):     
        with open("data\datafeed.txt", "r") as fp:
            flag = True
            check = 0
            for line in fp:
                day = line[(line.find(", ")+2): line.find(" ", line.find(", ")+2)]
                month1 = line[line.find(" ", line.find(", ")+2): line.find(" ", line.find(", ")+5)]
                month1 = month1[1:]
                year = line[(line.rfind(month1)+4): (line.rfind(month1)+8)]
                if month1 == 'Nov': month1 = '11'
                elif month1 == 'Jan': month1 = '01'
                elif month1 == 'Feb': month1 = '02'
                elif month1 == 'Mar': month1 = '03'
                elif month1 == 'Apr': month1 = '04'
                elif month1 == 'May': month1 = '05'
                elif month1 == 'Jun': month1 = '06'
                elif month1 == 'Jul': month1 = '07'
                elif month1 == 'Aug': month1 = '08'
                elif month1 == 'Sep': month1 = '09'
                elif month1 == 'Oct': month1 = '10'
                elif month1 == 'Dec': month1 = '12'
                cachedate = year + month1+day
                if str(cachedate) == str(self.arguments.date):
                    linefortitlecheck = line
                    self.pubDate.append(linefortitlecheck)
                    checkline = fp.readline()
                    control = False
                    for cout in range(len(self.title)):
                        if checkline == self.title[cout]:
                            control = True
                            self.pubDate.remove(linefortitlecheck)
                            break
                    if not control:
                        flag = False
                        self.title.append(checkline)
                        self.link.append(fp.readline())
                        self.desc.append(fp.readline())
                        self.links.append(fp.readline())
                check = check+5
            if flag: print("No news on this date (")

    def create_dir(self):
        if self.arguments.pdf:
            if not os.path.exists(self.arguments.pdf):
                os.mkdir(self.arguments.pdf)
        if self.arguments.html:
            if not os.path.exists(self.arguments.html):
                os.mkdir(self.arguments.html)
        if not os.path.exists("data"):
            os.mkdir("data")


def main():
    if not os.path.exists("data"):
        os.mkdir("data")
    news = NewsRss()
    if news.arguments.date:
        if news.date_check():
            news.fileread()
            news.print_news()
            if news.arguments.html:
                news.convert_to_html()
            if news.arguments.pdf:
                news.create_dir()
                news.convert_to_pdf()
            if news.arguments.verbose:
                making_log(0, '')
    else:
        news.feed_find()
        news.print_news()
        news.filewrite()
        if news.arguments.pdf:
            news.create_dir()
            news.convert_to_pdf()
        if news.arguments.html:
            news.create_dir()
            news.convert_to_html()
        if news.arguments.verbose:
            making_log(0, '')


if __name__ == '__main__':
    main()
