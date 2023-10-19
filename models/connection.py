import pymongo



client = pymongo.MongoClient('localhost:27017')

mydb = client['Bidstruct']
portals = mydb['portals']
users = mydb['users']
portal_list = mydb['portalList']
categories = mydb['categories']
user_profile = mydb['profile']
profile_portals = mydb['profilePortals']
stripe_customer = mydb['stripeCustomer']