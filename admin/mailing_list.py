

from models.connection import mydb, portal_list
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from models.portalModel import Portal
from datetime import datetime
import pandas as pd



mailing_clients = mydb['mailingClients'] 
client_portals = mydb["clientPortals"]
portals = mydb["portals"]


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

    def add(self, email, name, active, portal_list):
        client = {"name"   : name,
                  "email"  :  email,
                  "active" : active,
                  "portals_list" : portal_list

                  }
        mailing_clients.update_one({"email" : email}, {"$set" : client }, upsert= True )
    
    def view_all(self):
        return list(mailing_clients.find())

    def send_email(self, receiver_email):        
        context = ssl.create_default_context()
        csv_filename = f"csvs/{receiver_email}.csv"
        with open(csv_filename, "rb") as file:
            attachment = MIMEApplication(file.read(), Name=csv_filename)
        attachment["Content-Disposition"] = f"attachment; filename={csv_filename}"
    
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg['Subject'] = "Your Weekly Bid Reports.. "
            msg.attach(attachment)
            with open('admin/email_template/email_template.html', 'r') as file:
                html_content = file.read()
            msg.attach(MIMEText(html_content, 'html'))
            server.sendmail(sender_email, receiver_email, msg.as_string())

    def generate_data(self, portal_list):
        portal_list = (portal_list.get_json())
        print(type(portal_list))
        for portal in portal_list:
            portal_number = portal['portalId']
            print(f"geting data for {portal_number}")
            Portal.get_portal_data(portal_number)

    def get_all_portal_data(self):
        list_ = Portal.getPortalList()
        self.generate_data(list_)

    def generate_and_send_csv(self, email, portals_list):
        portal_list = []
        for x in portals_list:
            try:
                portal_list.append(x['portalId'])
            except:
                pass
        cursor = portals.find({'portal' : {'$in' : portal_list }})

        portal_data_list = [doc["portal_data"] for doc in cursor]
        # Flatten the list of portal_data
        flat_portal_data_list = [item for sublist in portal_data_list for item in sublist]

        # Create a DataFrame
        df = pd.DataFrame(flat_portal_data_list)
        try:
            df = df.drop(columns=['categoryIds'])
        except:
            pass
        # Save DataFrame to CSV
        df.to_csv(f"csvs/{email}.csv", index=False)
        self.send_email(email)


    def start_mailing_service(self):
        clients = self.view_all()
        for i,client in enumerate(clients):
            if i > 42:
                self.generate_and_send_csv(client['email'], client['portals_list'])
                print(i, client['email'], 'email sent @ : ', datetime.now().strftime("%d/%m/%Y, %H:%M:%S") )
