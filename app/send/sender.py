# Sending Email
'''

'''

import smtplib

from email.message import EmailMessage
import datetime

from validate_email import validate_email

class Sender:    
    def __init__(self, config, templateHelper = None):
        self.file_encoding = config.file_encoding
        self.smtp_host = config.smtp_host
        self.smtp_host_port = config.smtp_host_port
        self.smtp_account_username = config.smtp_account_username
        self.smtp_account_password = config.smtp_account_password
        self.smtp_account_from = config.smtp_account_from
        self.templateHelper = templateHelper

    def sendMessage(self, client):
        name_client = client.contact
        email_client = client.email
        date_now =f"{datetime.datetime.now():%d/%m/%Y}"
        time_now =f"{datetime.datetime.now():%H:%M %p}"

        msg = EmailMessage()

        msg.set_content("""\

        Service send email - peruvianit.

        [1] https://github.com/peruvianit

        """)

        msg['Subject'] = self.templateHelper.get_title_template()
        msg['From'] = self.smtp_account_from
        msg['To'] = email_client

        # Add the html version.  This converts the message into a multipart/alternative
        # container, with the original text message as the first part and the new html
        # message as the second part.

        try:
            with open("../templates/{name_template}/index.html".format(name_template = self.templateHelper.name_template), encoding=self.file_encoding) as fp:
                message_html = fp.read()
                msg.add_alternative(message_html.format(name_client=name_client, date_now=date_now, time_now=time_now), subtype='html')
        except IOError as e:
            raise IOError("Problem open template : {}".format(e))

        server = smtplib.SMTP(self.smtp_host, self.smtp_host_port)
        server.ehlo()
        server.starttls()

        #Next, log in to the server
        server.login(self.smtp_account_username, self.smtp_account_password)

        server.send_message(msg)
        server.quit()


    def verify_email(self, email):
        return True # TO DO 
