#!/usr/bin/python3
import praw
import requests
import cv2
from bs4 import BeautifulSoup

import random
import shutil
import argparse
import time
import os
import sys

# ------------------------------------------------------------------------------


def GenerateRandomFileName(name_len=10):
    '''
    used in WriteIm when submission.title not appropriate for filename
    '''
    return '/' + ''.join(['%s' % random.randint(0, 9) for
                          n in range(0, name_len)])
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
        except (FileNotFoundError, OSError):
            '''
            if submission post has some oddity that makes it incompatible
            with file naming conventions (backslashes or too long
            , rename to some random integer
            '''
            new_fname = GenerateRandomFileName()
            with open(sys.argv[1]+new_fname, 'wb') as f:
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
        #print('Saving %s' % submission.title)
    elif 'http://imgur/a/' in link:
        WriteAlbum(link, sys.argv[1]+'/'+submission.title+'_'
                   + str(hit_idx))
        #print('Saving album %s ' % submission.title)
# ------------------------------------------------------------------------------


def ConvertImToVid(directory, w_max=960, h_max=720, fps=1.0):
    '''
    uses cv2.VideoWriter to make video from images scraped. 

    Called w/ -v arg
    '''
    ims = [file for file in os.listdir(directory) if not file.endswith('.zip')]

    # cv2 only supports .avi & MJPQ combo, keep as is
    vid_name = directory + '.avi'
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    video = cv2.VideoWriter(vid_name, fourcc, fps, (w_max, h_max))

    # loop to resize im to (w, h)_max, append to video
    for image in ims:
        im_path = os.path.join(directory, image)
        frame = cv2.imread(im_path)
        frame = cv2.resize(frame, (w_max, h_max))
        video.write(frame)

    video.release()
    cv2.destroyAllWindows()
    shutil.move(vid_name, directory+'/'+vid_name)
    print('%s generated' % vid_name)
# ------------------------------------------------------------------------------


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Scrapes images from subreddit')
    parser.add_argument('subreddit', help='subreddit to scrape', type=str)
    parser.add_argument('L', help='max number submissions to scrape',
                        nargs='?', default=25, const=25, type=int)
    parser.add_argument('-v', '--video',
                        help='create video from all images in directory',
                        action='store_true')

    args = parser.parse_args()

    # fill in own credentials!
    scraper = praw.Reddit(client_id='',
                          client_secret='',
                          user_agent='',
                          username='',
                          password='')

    sub = scraper.subreddit(args.subreddit)

    # if first time running, scrape top posts
    if not os.path.exists(args.subreddit):
        os.makedirs(sys.argv[1])
        print('Scraping...')
        for submission in sub.top(time_filter='all', limit=args.L):
            link = submission.url
            SaveImFromLink(link)
        print('%s images scraped from %s' % ((
            len(os.listdir(args.subreddit))), args.subreddit))
    # if directory exists already, scrape hot posts
    else:
        # archive old files
        if len(os.listdir(args.subreddit)) > args.L:
            date = time.strftime('%Y%m%d')
            shutil.make_archive(date, 'zip', args.subreddit)

            for root, dirs, files in os.walk(args.subreddit):
                for f in files:
                    if not f.endswith('.zip'):
                        os.remove(os.path.join(root, f))

            print('Archived to %s' % date+'.zip')
            shutil.move(date + '.zip', args.subreddit+'/'+date+'.zip')

        # scrape hot posts if directory already present
        starting_count = len(os.listdir(args.subreddit))
        print('Scraping...')
        for submission in sub.hot(limit=args.L):
            link = submission.url
            SaveImFromLink(link)
        print('%s images scraped from %s' % ((
            len(os.listdir(args.subreddit)) - starting_count), args.subreddit))

    if args.video:
        ConvertImToVid(args.subreddit)

        # ------------------------------------------------------------------------------
