
import feedparser

if __name__ == '__main__':
    feed = feedparser.parse("rss.xml")
    print feed
    print "Hello World"
