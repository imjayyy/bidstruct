

from models.connection import mydb, portal_list
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from models.portalModel import Portal
mailing_clients = mydb['mailingClients'] 
client_portals = mydb["clientPortals"]


port = 465  # For SSL
smtp_server = "mail.privateemail.com"
sender_email = "bids@constructionbidreports.com"  # Enter your address
# receiver_email = "your@gmail.com"  # Enter receiver address
# password = "Checkmate1!"
password = "Checkmate1!"
message = """\
Subject: Hi there

This message is sent from Python."""




class Mailing_Clients():

    def add( email, name, active, portal_list):
        client = {"name"   : name,
                  "email"  :  email,
                  "active" : active,
                  "portals_list" : portal_list

                  }
        mailing_clients.update_one({"email" : email}, {"$set" : client }, upsert= True )
    
    @staticmethod
    def view_all():
        return list(mailing_clients.find())

    def send_email(receiver_email):        
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg['Subject'] = "Your Weekly Bid Reports.. "
            with open('admin\email_template\email_template.html', 'r') as file:
                html_content = file.read()
            msg.attach(MIMEText(html_content, 'html'))
            server.sendmail(sender_email, receiver_email, msg.as_string())


    def generate_file(self, portal_list):
        portal_list = (portal_list.get_json())
        print(type(portal_list))
        for portal in portal_list:
            portal_number = portal['portalId']
            print(f"geting data for {portal_number}")
            Portal.get_portal_data(portal_number)

    def get_all_portal_data(self):
        list_ = Portal.getPortalList()
        self.generate_file(list_)