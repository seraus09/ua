#!/usr/bin/env python3
import sys
import os
import smtplib

sender =  ''
destination = ''

USERNAME = ""
PASSWORD = ""

def print_ip():
    """Get N numbers list ip which will send to """
    with open("ip.txt") as myfile,  open("ip_tmp.txt", "w") as out:
        head = [next(myfile) for x in range(7)]
        for line in myfile:
            out.write(line)
    return ''.join(head)

def send_email():
    """The Function for send email to ..."""
    server = smtplib.SMTP('', 465) # host and port 
    server.ehlo()
    server.starttls()
    server.login(USERNAME,PASSWORD)
    subject = ' '
    email_text = "Here need to write the text of the messages"
    message = 'From: %s\nTo: %s\nSubject: %s\n\n%s' % ( sender,destination, subject, email_text)

    server.set_debuglevel(1) # Out debug to stdout
    server.sendmail(sender,dest_email, message)
    server.quit()

if __name__ == '__main__':
    send_email()
    os.remove("ip.txt")
    os.rename("ip_tmp.txt", "ip.txt")
