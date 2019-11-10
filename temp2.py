import argparse
import feedparser

def fib(url):
    NewsFeed = feedparser.parse(url)

    for entry in NewsFeed.entries[0:1]:
        
        print(entry.title)
        print("******")
        print(entry.summary)
        print("------News Link--------")
        print(entry.link)

def Main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help = "Provide usl please", type = str)
    parser.add_argument("-o","--output", help = "output result to a file",action="store_true")
    parser.add_argument("--version", help = "show initial version",action="store_true")
    parser.add_argument("--json", help = "convert output to json",action="store_true")
    parser.add_argument("--verbose", help = "Outputs verbose status messages",action="store_true")
    parser.add_argument("--limit","-LIMIT", help = "Limit news topics if this parameter provided",action="store_true")

    args = parser.parse_args()

    return fib(args.url)
    

    

if __name__ == '__main__':
		Main()