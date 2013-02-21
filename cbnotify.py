import argparse
from BeautifulSoup import BeautifulSoup    
import feedparser
import subprocess
import time

def main():
    parser = argparse.ArgumentParser(description='Send codebasehq notification events to notify.')
    parser.add_argument('url', nargs=1, help='codebasehq repo rss feed url')
    parser.add_argument('-s', '--seconds', default=60, help='seconds between rss polls')
    args = parser.parse_args()

    seen = []
    first = True
    while True:
        d = feedparser.parse(args.url[0])
        for i in d['entries']:
            id = u''.join(BeautifulSoup(i['id']).findAll(text=True))
            title = u''.join(BeautifulSoup(i['title']).getText())
            summary = BeautifulSoup(i['summary']).ul.li.p.contents[1].replace('&#x27;', "'").strip()
            if id not in seen:
                seen.append(id)
                if not first:
                    subprocess.call(['notify-send', u'{}'.format(title), u'{}'.format(summary)])
        first = False
        time.sleep(args.seconds)

if __name__ == '__main__':
    main()
