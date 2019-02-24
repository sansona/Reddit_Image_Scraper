#!/usr/bin/python3
import praw
import requests
from bs4 import BeautifulSoup

import os
import sys

# ------------------------------------------------------------------------------


def WriteIm(im_url, fname):
    '''
    writes image from URL of direct image i.e imgur.com/foo.jpg

    Does not work for
    generic image pages or albums i.e imgur.com/foobar or
    imgur.com/a/foobar
    '''

    response = requests.get(im_url)

    if response.status_code == 200:
        try:
            with open(fname, 'wb') as f:
                for chunk in response.iter_content(4096):
                    f.write(chunk)
        except FileNotFoundError:
            '''
            if submission post has some oddity that makes it incompatible
            with file naming conventions, rename to some crypto hash
            '''
            with open(sys.argv[1]+'/'+str(os.urandom(5)), 'wb') as f:

                for chunk in response.iter_content(4096):
                    f.write(chunk)
# ------------------------------------------------------------------------------


def WriteAlbum(album_url, fname):
    # not too sure whether this is working...seems something's wrong
    album_id = album_url[len('http://imgur.com/a/'):]
    html = requests.get(album_url).text

    soup = BeautifulSoup(html)
    hits = soup.select('.album-view-image-link a')
    hit_idx = 0
    for hit in hits:
        im_url = match['href']
        if '?' in im_url:
            im = im_url[im_url.rfind('/') + 1:im_url.rfind('?')]
        else:
            im = im_url[im_url.rfind('./') + 1:]
            WriteIm(im, fname)
            hit_idx += 1
# ------------------------------------------------------------------------------


def SaveImFromLink(submission_link):
    if link.endswith(('.jpg', 'jpeg', '.tif', '.png')):
        WriteIm(link, sys.argv[1]+'/'+submission.title)
        print('Saving %s' % submission.title)
    elif 'http://imgur/a/' in link:
        print('Saving album %s ' % submission.title)
        WriteAlbum(link, sys.argv[1]+'/'+submission.title+'_'
                   + str(hit_idx))
# ------------------------------------------------------------------------------


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage ./subreddit_scraper.py [-subreddit]')
    else:

        scraper = praw.Reddit(client_id='wni8KuJvkU88hg',
                              client_secret='vF1am1wndJ9oBC0DaIm7x8C7Em4',
                              user_agent='Subreddit scraper test',
                              username='subreddit_scraper',
                              password='11235Scrape')
        sub = scraper.subreddit(sys.argv[1])

        if not os.path.exists(sys.argv[1]):
            os.makedirs(sys.argv[1])
            for submission in sub.top(time_filter='all', limit=100):
                link = submission.url
                SaveImFromLink(link)
        else:
            for submission in sub.hot(limit=25):
                link = submission.url
                SaveImFromLink(link)
# ------------------------------------------------------------------------------
