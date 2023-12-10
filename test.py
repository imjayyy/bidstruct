import pymongo

# client = pymongo.MongoClient('localhost:27017')
# uri = "mongodb+srv://haithum:87UrsHcu1hyh3Gj5@cluster0.zexhhvh.mongodb.net/?retryWrites=true&w=majority"
# client = pymongo.MongoClient(uri)



# mydb = client['Bidstruct']
# portals = mydb['portals']
# users = mydb['users']
# admin = mydb['admin']
# portal_list = mydb['portalList']
# mailingClients = mydb['mailingClients']
# categories = mydb['categories']
# user_profile = mydb['profile']
# profile_portals = mydb['profilePortals']
# stripe_customer = mydb['stripeCustomer']

from admin.mailing_list import Mailing_Clients

from main import app

with app.app_context():

    Mailing_Clients().get_all_portal_data()