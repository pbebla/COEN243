import smtplib
from threading import Thread
import time
import os
from email.message import EmailMessage
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
def email_alert(subject, body, to, i):
    msg = MIMEMultipart()
    msg.attach(MIMEText(body, 'plain'))
    msg['subject'] = subject
    msg['to'] = to

    user = "sportsman2325@gmail.com"
    msg['from'] = user
    password = "zrasbhjwffjuwyox"
    
    fp = open("test%d.png" % i, 'rb')
    img = MIMEImage(fp.read())
    fp.close()
    msg.attach(img)
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user,password)
    server.send_message(msg)
    server.quit()


#email_alert("Hey", "Hello World", "sportsman2325@gmail.com")
