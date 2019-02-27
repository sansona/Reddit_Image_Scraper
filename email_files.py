import time
import sys
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

# WIP
from_address = ''
to_address = []

if len(sys.argv == 2):
    date = time.strftime('%Y%m%d')
    subreddit = sys.argv[1]

    msg = MIMEMultipart()
    msg['Subject'] = date + subreddit
    msg['From'] = from_address
    msg['To'] = ', '.join(to_address)

    for file in directory:
        fp = open(file, 'rb')
        im = MIMEImage(fp.read())
        fp.close()
        msg.attach(im)

    s = smtplib.SMTP('localhost')
    s.sendmail(from_address, to_address, msg.as_string())
    s.quit()


else:
    print('Usage: ./email_files.py [-subreddit]')
