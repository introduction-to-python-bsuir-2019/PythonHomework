import argparse
import logging
import urllib3
from bs4 import BeautifulSoup
import feedparser
import urllib.request
import sys
import json
import datetime


def argsparsing():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="RSS URL", type=str)
    parser.add_argument("--version", action='version', version='%(prog)s ' + 'v 1.2', help="Print version info", )
    parser.add_argument("--json", help="Print result as JSON in stdout", action="store_true")
    parser.add_argument("--verbose", help="Outputs verbose status messages", action="store_true")
    parser.add_argument("--limit", type=int, help="Limit news topics if this parameter provided")
    parser.add_argument("--date",type=int,help="Read cashed news by date in next format YYMMDD")
    return parser.parse_args()

def making_log(operation, message, file='loglist.log'):
    """func can do 2 ops, if 1 to write if 0 to read"""
    if bool(operation):
        logging.basicConfig(filename=file, format='%(name)s - %(levelname)s - %(message)s-%(asctime)s',
                            level=logging.INFO)
        logging.info(message)
    else:
        print(open(file, 'r').read())


class NewsRss:
    """Class with all parts of rss news and methods to work with its."""


    def __init__(self):
        self.arguments=argsparsing()
        self.title=[]
        self.pubDate=[]
        self.link=[]
        self.desc=[]
        self.links=[]
        self.datalist=[]

    def feed_find(self):
        soup = BeautifulSoup(urllib.request.urlopen(self.arguments.source), "xml")
        making_log(1, "Opened URL for news reading, URL: %s" % self.arguments.source)
        list = soup.find_all("item")
        datafeed={}
        making_log(1, "Find all <item> tags in feed.")
        making_log(1, "Limit is: (%s)        " % (str(self.arguments.limit)))
        for cout, feed in enumerate(list):
            if cout != self.arguments.limit:
                making_log(1, "Opened feed on %s link." % feed.link.text)
                strmedia = str(feed.find_all("media:content"))
                ded = feed.description.text
                self.links=[] 
                for i in range(strmedia.count('url="')):
                    self.links.append(strmedia[strmedia.find('url="'): (strmedia.find('"', (strmedia.find('url="')+5))+1)])
                self.link.append(feed.link.text)
                self.title.append(feed.title.text)
                self.pubDate.append(feed.pubDate.text)
                self.desc.append(ded[(ded.find('a>') + 1):ded.find('<p><br')])
            else:
                making_log(1, "Iteration closed with code 0(all_goods)")
                break


    def print_news(self):
        arg=self.arguments.json
        for index in range(len(self.title)):
            if arg:
                print(json.dumps({"item":{"link":self.link[index],"body":{"title":self.title[index],"date": self.pubDate[index],"images": self.links,"feed":self.desc[index]}}},indent=4))
                print("\n\n\n")
            else:    
                print("Title: " + self.title[index],
                        "\nDate: " + self.pubDate[index],
                        "\nLink: " + self.link[index])
                print("Feed: " + self.desc[index])
                if self.links != []:
                    print("Images: \n" + str(self.links))
                print("\n\n\n")    
    

    def date_convert(self):
        if len(str(self.arguments.date))>8 or len(str(self.arguments.date))<8 :
            print("Error in date input")
            return False
        
        return True


    def filewrite(self):
        for index in range(len(self.title)):
                fp=open("feeddata.txt","a")
                fp.write(str(self.pubDate[index]))
                fp.write(" \n")
                fp.write(str(self.title[index]))
                fp.write(" \n")
                fp.write(str(self.link[index]))
                fp.write(" \n")
                fp.write(str(self.desc[index]))
                fp.write(" \n")
                fp.write(str(self.links))
                fp.write(' \n')
                fp.close()


    def fileread(self):     
        fp=open("feeddata.txt","r")
        flag=True
        for line in fp:
            #monttdict={'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
            day=line[(line.find(", ")+2):line.find(" ",line.find(", ")+2)]
            month1=line[line.find(" ",line.find(", ")+2):line.find(" ",line.find(", ")+5)]
            month1=month1[1:]
            year=line[(line.rfind(month1)+4):(line.rfind(month1)+8)]
            if month1=='Nov': month1='11'
            elif month1=='Jan': month1='01'
            cachedate=year+month1+day
            if str(cachedate)==str(self.arguments.date):
                flag=False
                self.pubDate.append(line)
                self.title.append(fp.readline())
                self.link.append(fp.readline())
                self.desc.append(fp.readline())
                self.links.append(fp.readline())
        if flag: print("No news on this date :(")
        fp.close()

      


def main():
    news=NewsRss()
    if news.arguments.date:
        if news.date_convert():
            news.fileread()
            news.print_news()
            if news.arguments.verbose:
                making_log(0,'')
    else:
        news.feed_find()
        news.print_news()
        news.filewrite()
        if news.arguments.verbose:
            making_log(0,'')


if __name__=='__main__':
    main()



