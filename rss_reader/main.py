import argparse
import urllib.request as req
from xml.dom import minidom

parser = argparse.ArgumentParser()
parser.add_argument('--url', help='url of news source in RSS format')
args = parser.parse_args()

with req.urlopen(args.url) as f:
  content = f.read().decode("UTF-8")
  contentBytes = f.read()

rss = minidom.parseString(content)
urlTitle = rss.getElementsByTagName("channel")[0]

print("Resource:", urlTitle.getElementsByTagName("title")[0].firstChild.data)
print("Link:", urlTitle.getElementsByTagName("link")[0].firstChild.data)
print("About:", urlTitle.getElementsByTagName("description")[0].firstChild.data)
print("\n\n")

items = rss.getElementsByTagName("item")

for item in items:
  print("Title:", item.getElementsByTagName("title")[0].firstChild.data)
  print("RSS Link:", item.getElementsByTagName("link")[0].firstChild.data)
  print("Browser link:", item.getElementsByTagName("guid")[0].firstChild.data)
  print("Description:", item.getElementsByTagName("description")[0].firstChild.data)
  print("\n")