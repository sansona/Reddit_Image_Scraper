#!/usr/bin/python3
import time
import os
import sys
import imghdr
import smtplib

from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase


SMTPServer = ''
from_address = ''
to_addresses = ['']
USERNAME = ''
PASSWORD = ''

if len(sys.argv) == 2:
    try:
        date = time.strftime('%Y%m%d')
        subreddit = sys.argv[1]

        os.chdir(sys.argv[1])

        msg = MIMEMultipart()
        msg['Subject'] = date + '-' + subreddit
        msg['From'] = from_address
        msg['To'] = ', '.join(to_addresses)

        # text component
        message = 'Hot posts from r/%s as of %s!' % (subreddit, date)
        msg.attach(MIMEText(message, 'plain', 'utf-8'))

        # image component
        filename = 'Sleepy pup'
        attachment = open(filename, 'rb')
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)  # python 3.x has known encoding bug
        # (TODO): figure out how to append correct filetype
        part.add_header('Content-Disposition',
                        "attachment; filename= %s" % (filename + '.jpeg'))
        msg.attach(part)

        s = smtplib.SMTP_SSL(SMTPServer)
        s.connect(SMTPServer, 465)
        s.login(USERNAME, PASSWORD)
        '''
        for file in directory:
            with open(file, 'rb') as fp:
                im = fp.read()
            msg.add_attachment(im, maintype='image',
                               subtype=imghdr.what(None, im))
'   '''

        s.sendmail(from_address, to_addresses, msg.as_string())
        print('Email sent')
    except:
        sys.exit('Sending failed')

else:
    print('Usage: ./email_files.py [-subreddit]')
