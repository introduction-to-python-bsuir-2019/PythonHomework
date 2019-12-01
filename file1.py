#!/usr/bin/env python

from bs4 import BeautifulSoup
import requests
import urllib
import urllib.request
import argparse
import sys
import json
import logging

parser=argparse.ArgumentParser()
parser.add_argument('url',type=str)
parser.add_argument('--version',action='store_true')
parser.add_argument('--limit', type=int)
parser.add_argument('--json', action='store_true')
agrs=parser.parse_args()

logging.basicConfig( filename='rss_read/rss_read.log',level=logging.INFO,format=u'[%(asctime)s]  %(message)s')

class Feed():
    """ """
    
    def __init__(self, url):
        self.url=url
        self.list_news=[]
        self.class_news=[]
        
    def setupconnection(self):
       self.webUrl  = urllib.request.urlopen(self.url)
       if self.webUrl.getcode()!=200:
           print("Cannot get a proper connection to the web-site")
           logging.error('Cannot get a proper conncetion to the web-site')
           

      
    
    def createfields(self):
        self.handler=self.webUrl.read()
        self.soup=BeautifulSoup(self.handler,"xml")
        if agrs.limit==None:
           self.list_news = self.soup.find_all('item')
        else:
            self.list_news = self.soup.find_all('item',limit=agrs.limit)
      
        for item in self.list_news:
            
           
            title=item.find('title')
            date=item.find('pubDate')
            des=item.find('description')
            link=item.find('link')
            des=BeautifulSoup(des.text,'xml')
            img=des.find('img')['src']
            description=des.find('a')
            
            self.class_news.append(News(title.text,date.text,link.text,img,description.text))
            

        
    def printout(self):
        for i in self.class_news:
            i.printnews()  
    def tojson(self):
        try:
            print("ss")
            jsonfile=open('news_json.json','w+')
            json_list: list=[]
            for i in self.class_news:
               data=i.converttojson()
               json_list.append(data)
            json.dump(json_list,jsonfile) 
        except IOError:
            print("Error: Can't create the json file")
            sys.exit()
            

class News():
    """"""
    def __init__(self,title, date, link,img,des):
        self.title="Title: "+title
        self.date="Publicatiob date: "+date
        self.des="Description : "+des
        self.img="Image link: "+img
        self.link="Link: "+link
    def printnews(self):
        print(self.title)
        print(self.date)
        print(self.des)
        print(self.link)
        print(self.img)
    def converttojson(self):
        to_dict= self.__dict__
        return to_dict

def vers():
    print('Current version is 1')
    sys.exit()
def main(url):
  logging.info('Started executing')
  if agrs.version==True:
      vers()
  
  work=Feed(url)
  work.setupconnection()
  work.createfields()
  if agrs.json==True:
      

      work.tojson()
  work.printout()
 

main(agrs.url)



