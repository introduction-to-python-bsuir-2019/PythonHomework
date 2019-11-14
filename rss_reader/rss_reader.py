import argparse
import feedparser
import html
from bs4 import BeautifulSoup
import json
#from tqdm import tqdm
from rss_reader import version
#import version

class News_Feed:
    def __init__(self, feed_title, items):
        self.feed_title=feed_title
        self.items=items
        
    def print_to_json(self):
        with open("news.json", "w") as write_file:
                json.dump({"Feed":self.feed_title, "Items":[item.return_item() for item in self.items]}, write_file)
        print('news.json created successfully')

    def print_to_console(self):
        print ('Feed: {0}'.format(self.feed_title))    
        for item in self.items:
            item.print_to_console()
        
    def print_feed(self, json):
        if(json):
            self.print_to_json()
        else:
            self.print_to_console()

class Item:
    def __init__(self, title, date, link, description, links):
        self.title=title
        self.date=date
        self.link=link
        self.description=description
        self.links=links
        
    def print_to_console(self):
        print ('\nTitle: {0}'.format(self.title))    
        print ('Date: {0}'.format(self.date))
        print ('Link: {0} \n'.format(self.link))
        
        print(self.description)
        print()
        if self.links['href_links']:
            print ('\nLinks:')
            for link in self.links['href_links']:
                print (link)
                
        if self.links['images_links']:
            print ('\nImages:')
            for link in self.links['images_links']:
                print (link)
            
        if self.links['video_links']:
            print ('\nVideos:')
            for link in self.links['video_links']:
                print (link)
        print ('\n//////////////////////////////////////////////////////////////////////////')
        
    def return_item(self):
        return {"title": self.title,"description": self.description,"link": self.link,"pubDate": self.date,"source": self.links}
def set_argparse():
    parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader.')
    parser.add_argument('source', type=str, help='RSS URL')

    parser.add_argument('--version', action='version', version='%(prog)s v'+version.__version__, help='Print version info')
    parser.add_argument('--json', action='store_true', help='Print result as JSON in stdout')
    parser.add_argument('--verbose', action='store_true', help='Outputs verbose status messages')
    parser.add_argument('--limit', type=int, default=-1, help='Limit news topics if this parameter provided')
    return parser.parse_args()

def find_images(args, soup):
    
    image_iterator=1
    images_links=[]
    for img in soup.findAll('img') :       
        
        if 'alt' in img.attrs and img['alt']!='':
            replaced_data=' [image {0} | {1}] '.format(image_iterator,img['alt'])                                   
        else:
            replaced_data=' [image {0}]'.format(image_iterator)
        src=img['src']
        images_links.append('[{0}]: {1}'.format(image_iterator, src))
        soup.find('img').replace_with(replaced_data)
        image_iterator+=1
    return images_links

def find_href(args,soup):
    href_iterator=1
    href_links=[]
    for href in soup.findAll('a') :       
        
        if 'href' in href.attrs:
            link=href['href']
            if href.text!='':
                replaced_data=' [link {0} | {1}] '.format(href_iterator,href.text)                                   
            else:
                replaced_data=' [link {0}] '.format(href_iterator)
            href_links.append('[{0}]: {1}'.format(href_iterator, link))
            soup.find('a').replace_with(replaced_data)
            href_iterator+=1 
    return href_links
def find_videos(args,soup):
    video_iterator=1
    video_links=[]
    for video in soup.findAll('iframe'):
        if 'src' in video.attrs:
            link=video['src']
            replaced_data=' [video {0}] '.format(video_iterator)            
            video_links.append('[{0}]: {1}'.format(video_iterator, link))            
            soup.find('iframe').replace_with(final)
            video_iterator+=1
            
def main() -> None:
    args=set_argparse();
    NewsFeed = feedparser.parse(args.source)
    if args.limit==-1 :
        args.limit=len(NewsFeed.entries)

    news=[]
    
    for i in range(args.limit) :
        
        entry = NewsFeed.entries[i]
        soup = html.unescape(BeautifulSoup(entry['summary'], "html.parser"))
 
        images_links=find_images(args, soup)
        href_links=find_href(args, soup)
        video_links=find_videos(args, soup)
          
        links={'images_links':images_links,'href_links':href_links,'video_links':video_links}
        
        news.append(Item(html.unescape(entry['title']),entry['published'],entry['link'],soup.text,links))
        
    newsFeed=News_Feed(NewsFeed.feed.title, news)
    newsFeed.print_feed(args.json);
if __name__ == '__main__':
    
    main()
