#import smtplib
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from PyQt4.QtGui import *
from PyQt4.QtCore import *

def email():


    try:
        fromaddr = "senders email address"
        password = "enter senders password"
        toaddr = "receiversemailaddress"

        # instance of MIMEMultipart
        msg = MIMEMultipart()

        # storing the senders email address
        msg['From'] = fromaddr

        # storing the receivers email address
        msg['To'] = toaddr

        # storing the subject
        msg['Subject'] = "Alert!!"

        # string to store the body of the mail
        body = "Limit Crossed"

        # attach the body with the msg instance
        msg.attach(MIMEText(body, 'plain'))

        directory = "Snaps/"
        # open the file to be sent
        for filename in os.listdir(directory):
            temp = directory+ filename
            attachment = open(temp, "rb")

            # instance of MIMEBase and named as p
            p = MIMEBase('application', 'octet-stream')

            # To change the payload into encoded form
            p.set_payload((attachment).read())

            # encode into base64
            encoders.encode_base64(p)

            p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

            # attach the instance 'p' to instance 'msg'
            msg.attach(p)

        # creates SMTP session
        s = smtplib.SMTP('smtp.gmail.com', 587)

        # start TLS for security
        s.starttls()

        # Authentication
        s.login(fromaddr, password)

        # Converts the Multipart msg into a string
        text = msg.as_string()

        # sending the mail
        s.sendmail(fromaddr, toaddr, text)

        # terminating the session
        s.quit()

        print("Email Sent")

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Email Information")
        msg.setText("Email sent")
        msg.setStandardButtons(QMessageBox.Ok)
        # msg.buttonClicked.connect(sys.exit)
        retval = msg.exec_()

    except:
        print("Please check your Internet Connectivity")
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("ERROR")
        msg.setText("Please check your Internet Connectivity")
        msg.setStandardButtons(QMessageBox.Ok)
        # msg.buttonClicked.connect(sys.exit)
        retval = msg.exec_()
