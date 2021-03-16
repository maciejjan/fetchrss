import argparse
import csv
import datetime
import dateutil.parser
from dateutil.tz import tzlocal
import feedparser
import lxml.html
import os
import os.path
import sys


def get_lmdate(filename):
	'''Get the last modified date of a file.
	   Returns None if the file doesn't exist.'''
	lmdate = None
	if os.path.isfile(filename):
		lmdate = datetime.datetime.fromtimestamp(\
		    os.stat(filename).st_mtime, tz=tzlocal())
	return lmdate


def htmltotext(string):
	return ''.join(lxml.html.fromstring(string).itertext())


def write_feed_as_csv(url, fp, lmdate=None):
	writer = csv.DictWriter(fp, ('id', 'title', 'link', 'date', 'text'))
	if lmdate is None:
		writer.writeheader()
	feed = feedparser.parse(url)
	for e in feed.entries:
		dd = dateutil.parser.parse(e['published'])
		if lmdate is not None and dd <= lmdate:
			continue
		text = None
		if 'content' in e and e['content']:
			if e['content'][0]['type'] == 'text/html':
				text = htmltotext(e['content'][0]['value'])
			else:
				text = e['content'][0]['value']
		writer.writerow({
		    'id': e['id'], 'title': e['title'], 'link': e['link'],
			'date': e['published'], 'text': text})


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Fetch an RSS feed and write articles to a CSV file.')
    parser.add_argument('url', metavar='URL', help='The URL of the feed.')
    parser.add_argument('-o', '--output-file', metavar='PATH')
    return parser.parse_args()


if __name__ == '__main__':
	args = parse_arguments()

	if args.output_file is not None:
		lmdate = get_lmdate(args.output_file)
		with open(args.output_file, 'a+') as fp:
			write_feed_as_csv(args.url, fp, lmdate=lmdate)
	else:
		write_feed_as_csv(args.url, sys.stdout)

