#!/usr/bin/python3
import time
import os
import sys
import imghdr
import smtplib
from email.message import EmailMessage
from email.MIMEText import MIMEText

SMTPServer = ''
from_address = ''
to_addresses = []
USERNAME = ''
PASSWORD = ''

if len(sys.argv == 2):
    date = time.strftime('%Y%m%d')
    subreddit = sys.argv[1]

    os.chdir(sys.argv[1])
    try:
        msg = EmailMessage()
        msg['Subject'] = date + subreddit
        msg['From'] = from_address
        msg['To'] = ', '.join(to_addresses)

        message = 'Test string from python!'
        msg.attach(MIMEText(message))

        s = smtplib.SMTP(SMTPServer, 587)
        s.login(USERNAME, PASSWORD)
        '''
        for file in directory:
            with open(file, 'rb') as fp:
                im = fp.read()
            msg.add_attachment(im, maintype='image',
                               subtype=imghdr.what(None, im))
    '   '''

        s.sendmail(from_address, to_addresses, msg.as_string())

    except:
        sys.exit('Sending failed: %s' % 'CUSTOM_ERROR')


else:
    print('Usage: ./email_files.py [-subreddit]')
