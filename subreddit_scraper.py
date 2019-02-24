#!/usr/bin/python3
import praw
import requests
from bs4 import BeautifulSoup

import shutil
import argparse
import time
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
    '''
    handles function routing from different types of inputs
    '''
    if link.endswith(('.jpg', 'jpeg', '.tif', '.png')):

        WriteIm(link, sys.argv[1]+'/'+submission.title)
        print('Saving %s' % submission.title)
    elif 'http://imgur/a/' in link:
        print('Saving album %s ' % submission.title)
        WriteAlbum(link, sys.argv[1]+'/'+submission.title+'_'
                   + str(hit_idx))
# ------------------------------------------------------------------------------


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Scrapes images from subreddit')
    parser.add_argument('S', help='subreddit to scrape', type=str)
    parser.add_argument('L', help='max number submissions to scrape',
                        nargs='?', default=25, const=25, type=int)
    args = parser.parse_args()

    # fill in own credentials!
    scraper = praw.Reddit(client_id='wni8KuJvkU88hg',
                          client_secret='vF1am1wndJ9oBC0DaIm7x8C7Em4',
                          user_agent='Subreddit scraper test',
                          username='subreddit_scraper',
                          password='11235Scrape')
    sub = scraper.subreddit(args.S)

    # if first time running, scrape top posts
    if not os.path.exists(args.S):
        os.makedirs(sys.argv[1])
        for submission in sub.top(time_filter='all', limit=args.L):
            link = submission.url
            SaveImFromLink(link)
        print('%s images scraped from %s' % ((
            len(os.listdir(args.S))), args.S))
    # if directory exists already, scrape hot posts
    else:
        # archive old files
        if len(os.listdir(args.S)) > 10:
            shutil.make_archive(time.strftime('%Y%m%d'), 'zip', args.S)

            for root, dirs, files in os.walk(args.S):
                for f in files:
                    if not f.endswith('.zip'):
                        os.remove(os.path.join(root, f))
                        print('Removed %s' % f)

            print('Archived to %s' % time.strftime('%Y%m%d') + '.zip')

        starting_count = len(os.listdir(args.S))
        for submission in sub.hot(limit=args.L):
            link = submission.url
            SaveImFromLink(link)
        print('%s images scraped from %s' % ((
            len(os.listdir(args.S)) - starting_count), args.S))

        # ------------------------------------------------------------------------------
