"""Sending email class using smtplib 
"""
from email.mime import multipart
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import xml.etree.ElementTree as et
import smtplib, ssl

# Get the credential from credentials.xml
email_creds = et.parse('emailCredentials.xml').getroot()
sender = email_creds[0].text
pwd = email_creds[1].text
gmail_server = email_creds[2].text
port_server = email_creds[3].text

# Send email
def send_email(name, emailaddr, height, ave_height, total):
    to_email = emailaddr
    subject = "Your height information"
    message_text = """\
        Hi %s, 

        This is information about your height, your height: %s cm. The average height is %s cm out of %s people. 

        Thanks,

        Survey Teams
        """% (name, height, ave_height, total)

    message_html="""\
        <html>
            <body>
                <p>Hi %s,<br><br>
                This is information about your height, your height: <strong>%s</strong> cm.<br>
                The average height is <strong>%s</strong> cm out of <strong>%s</strong> people.<br> 
                <br>
                Thanks,<br><br>
                Survey Teams
                </p>
            </body>
        </html>
        """% (name, height, ave_height, total)

    msg = MIMEMultipart("alternative")
    msg['Subject'] = subject
    msg['To'] = to_email
    msg['From'] = sender
    # Convert into plain/html MIMEText object
    part1 = MIMEText(message_text,'plain')
    part2 = MIMEText(message_html, 'html')

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    msg.attach(part1)
    msg.attach(part2)

    # Create secure connection with server and send email
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(gmail_server,port_server, context=context) as gmail:
            gmail.login(sender, pwd)
            gmail.sendmail(sender,emailaddr, msg.as_string())
    except:
        print("Sending email failed!")    

