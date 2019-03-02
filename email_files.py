#!/usr/bin/python3

from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase

import time
import os
import sys
import imghdr
import smtplib

# ------------------------------------------------------------------------------
# Sends auto-generated emails containing contents of chosen folder.
#
# Intended to be used with conjunction with subreddit_scraper.py, though is
# similarly self contained
# ------------------------------------------------------------------------------

# user configs - remember to remove before pushing!
SMTPServer = ''
from_address = ''
to_addresses = []
USERNAME = ''
PASSWORD = ''
os.chdir()

if len(sys.argv) == 2:
    date = time.strftime('%Y/%m/%d')
    subreddit = sys.argv[1]

    msg = MIMEMultipart()
    msg['Subject'] = date + '-r/' + subreddit
    msg['From'] = from_address
    msg['To'] = ', '.join(to_addresses)

    # text component
    message = 'Hot posts from r/%s as of %s!' \
        '\n\nBeep boop. I am a bot. This is an auto-generated email.' \
        '\n\nPlease do not respond since I am not sentient. Beep boop' % (
            subreddit, date)
    msg.attach(MIMEText(message, 'plain', 'utf-8'))

    # image component
    for file in os.listdir(subreddit):
        # establish payload
        filename = subreddit + '/' + file
        if filename.endswith('zip'):
            pass
        else:
            attachment = open(filename, 'rb')
            part = MIMEBase('application', 'octet-stream')
            part.set_payload((attachment).read())
            # python 3.x has known encoding bug
            encoders.encode_base64(part)

            # for cross OS compatibility, ensure correct extension
            extension = str(imghdr.what(filename))
            if extension == 'None':
                # imghdr buggy, default .jpeg since majority are .jpeg
                extension = 'jpeg'

            part.add_header('Content-Disposition',
                            "attachment; filename= %s" % (
                                file + '.' + extension))
            msg.attach(part)
            print('%s attached' % file)

    s = smtplib.SMTP_SSL(SMTPServer)
    s.connect(SMTPServer, 465)
    s.login(USERNAME, PASSWORD)

    print('Sending...')
    s.sendmail(from_address, to_addresses, msg.as_string())
    print('Email sent')

else:
    print('Usage: ./email_files.py [-subreddit]')
