"""Copyright (c) 2020 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from .env import config



def emailEmpl(emplEmail, lastName, firstName, device_code, col, na, sec):
    sender_email = "onboarding@cisco.com"
    smtp_server = "outbound.cisco.com"
    message = MIMEMultipart("alternative")
    message["Subject"] = "Welcome on board!"
    message["From"] = sender_email
    message["To"] = emplEmail

#./app/backend/email/on-boarding_temp1.html

    
    with open('./app/backend/email/on-boarding_temp1.html', 'r') as file:
      html = file.read()
    
    
    if sec:
      sec_info = "You have been provisioned for Duo services for multi-factor authentication"
      sec_action = r"""
          You are now protected by Umbrella.
        """
    else:
      sec_info = "You are now protected by Umbrella"
      sec_action = ""
    
    if na:
      na_info = "You have been provisioned for Meraki services for network access"
      na_action = r"""
          Download the Meraki Systems Manager for your devices from this <a href="m.meraki.com">link</a>.<br>
          Your network ID is the following: 007-978-7409
        """
    else:
      na_info = "No network access services were provisioned"
      na_action = ""
    

    webex_action = ""
    if col:
      webex_info = "You have been provisioned for Webex services"
      if device_code == 'null' :
        webex_action = r"""
          Download the Webex App for your devices from this <a href="https://www.webex.com/downloads.html">link</a>.
        """
      else :
        webex_action = r"""
          Download the Webex App for your devices from this <a href="https://www.webex.com/downloads.html">link</a>.<br>
          Activate your Webex video device using the following code:
        """ + device_code
    else:
      webex_info = "No Webex services were provisioned"

    html = html.format(webex_info, webex_action, na_info, na_action, sec_info, sec_action)


    content = MIMEText(html, "html")
    message.attach(content)

    # fp1 = open('./app/backend/email/logocisco.png', 'rb')
    # image1 = MIMEImage(fp1.read())
    # fp1.close()
    # image1.add_header('Content-ID', '<ciscologo>')
    # message.attach(image1)

    # fp2 = open('./app/backend/email/collab.png', 'rb')
    # image2 = MIMEImage(fp2.read())
    # fp2.close()
    # image2.add_header('Content-ID', '<collabicon>')
    # message.attach(image2)

    # fp3 = open('./app/backend/email/network.png', 'rb')
    # image3 = MIMEImage(fp3.read())
    # fp3.close()
    # image3.add_header('Content-ID', '<networkicon>')
    # message.attach(image3)

    # fp4 = open('./app/backend/email/security.png', 'rb')
    # image4 = MIMEImage(fp4.read())
    # fp4.close()
    # image4.add_header('Content-ID', '<securityicon>')
    # message.attach(image4)

    context = ssl.create_default_context()
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server,25) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        try :
            server.sendmail(sender_email, emplEmail, message.as_string())
        except Exception as e: 
            print('Email is not sent!')
            print(e)


#emailEmpl("aalmodha@cisco.com", 'Almodhabri', 'Majed', '987654321', True, True, True)