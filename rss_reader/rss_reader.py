import argparse
import feedparser
import html
from bs4 import BeautifulSoup
import json
#from tqdm import tqdm

import version

class News_Feed:
    def __init__(self, feed_title, items):
        self.feed_title=feed_title
        self.items=items

    def print_feed(self):
        with open("data_file.json", "w") as write_file:
            json.dump({"Feed":self.feed_title, "Items":[item.return_item() for item in self.items]}, write_file)

class Item:
    def __init__(self, title, date, link, description, links):
        self.title=title
        self.date=date
        self.link=link
        self.description=description
        self.links=links
        
    def return_item(self):
        return {"title": self.title,"description": self.description,"link": self.link,"pubDate": self.date,"source": self.links}

def main() -> None:
    parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader.')
    parser.add_argument('source', type=str, help='RSS URL')

    parser.add_argument('--version', action='version', version='%(prog)s v'+version.__version__, help='Print version info')
    parser.add_argument('--json', action='store_true', help='Print result as JSON in stdout')
    parser.add_argument('--verbose', action='store_true', help='Outputs verbose status messages')
    parser.add_argument('--limit', type=int, default=-1, help='Limit news topics if this parameter provided')
    args = parser.parse_args()
    NewsFeed = feedparser.parse(args.source)
    if args.limit==-1 :
        args.limit=len(NewsFeed.entries)

    news=[]
    
    for i in range(args.limit) :
        
        entry = NewsFeed.entries[i]
        soup = html.unescape(BeautifulSoup(entry['summary'], "html.parser"))

        print ('Title: {0}'.format(html.unescape(entry['title'])))    
        print ('Date: {0}'.format(entry['published']))
        print ('Link: {0}'.format(entry['link']))
        print ()
        
        j=1
        images_links=[]
        for img in soup.findAll('img') :       
            
            if 'alt' in img.attrs:
                alt=img['alt']
                if alt!='':
                    final=' [image {0} | {1}] '.format(j,alt)
                else:
                    final=' [image {0}]'.format(j)    
                            
            else:
                final=' [image {0}]'.format(j)
            src=img['src']
            images_links.append('[{0}]: {1}'.format(j, src))
            j+=1
            
            soup.find('img').replace_with(final)
        j=1
        href_links=[]
        for href in soup.findAll('a'):
            if 'href' in href.attrs:
                link=href['href']
                if href.text!='':
                    final=' [link {0} | {1}] '.format(j,href.text)
                else:
                    final=' [link {0}] '.format(j)  
                soup.find('a').replace_with(final)
                href_links.append('[{0}]: {1}'.format(j, link))
                j+=1
        j=1
        video_links=[]
        for video in soup.findAll('iframe'):
            if 'src' in video.attrs:
                link=video['src']
                final=' [video {0}] '.format(j)
                soup.find('iframe').replace_with(final)
                video_links.append('[{0}]: {1}'.format(j, link))
                j+=1    
        links={'images_links':images_links,'href_links':href_links,'video_links':video_links}
        
        news.append(Item(html.unescape(entry['title']),entry['published'],entry['link'],soup.text,links))
        print(soup.text)
        print ()
        print ()
        if href_links:
            print ('Links:')
            for link in href_links:
                print (link)
        if images_links:
            print ()
            print ('Images:')
            for link in images_links:
                print (link)
            
        if video_links:
            print ()
            print ('Videos:')
            for link in video_links:
                print (link)
        print ()
        print ()
        print ()
    newsFeed=News_Feed("URL", news)
    newsFeed.print_feed();
if __name__ == '__main__':
    
    main()
