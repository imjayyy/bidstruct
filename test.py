import csv
import json
from models.connection import categories


# csv_file = 'data.csv'

# with open(csv_file, 'r') as csv_input:
#     csv_reader = csv.DictReader(csv_input)
#     data = [row for row in csv_reader]

# categories.insert_many(data)


ls = [
    {'_id': {'$oid': '653aef5abe867985ad4ca67c'}, 'profile_id': {'$oid': '653836c97e361c1a21f806d2'}, 'portal_id': '21147', 
     'portals': [{'_id': {'$oid': '6526cdc1518a72e0eddfef35'}, 'portalId': '21147', 'portalName': 'Birmingham City Schools', 'portalState': 'AL'}]}, {'_id': {'$oid': '653aef5abe867985ad4ca67d'}, 'profile_id': {'$oid': '653836c97e361c1a21f806d2'}, 'portal_id': '55902', 'portals': [{'_id': {'$oid': '6526cdc1518a72e0eddfef36'}, 'portalId': '55902', 'portalName': 'Birmingham-Jefferson County Transit Authority', 'portalState': 'AL'}]}, {'_id': {'$oid': '653aef5abe867985ad4ca67e'}, 'profile_id': {'$oid': '653836c97e361c1a21f806d2'}, 'portal_id': '24103', 'portals': [{'_id': {'$oid': '6526cdc1518a72e0eddfee8e'}, 'portalId': '24103', 'portalName': 'City of National City', 'portalState': 'CA'}]}, {'_id': {'$oid': '653aef5bbe867985ad4ca67f'}, 'profile_id': {'$oid': '653836c97e361c1a21f806d2'}, 'portal_id': '46106', 'portals': [{'_id': {'$oid': '6526cdc1518a72e0eddfee8b'}, 'portalId': '46106', 'portalName': 'City of Burlingame', 'portalState': 'CA'}]}, {'_id': {'$oid': '653aef5bbe867985ad4ca680'}, 'profile_id': {'$oid': '653836c97e361c1a21f806d2'}, 'portal_id': '42510', 'portals': [{'_id': {'$oid': '6526cdc1518a72e0eddfee87'}, 'portalId': '42510', 'portalName': 'City of Vallejo', 'portalState': 'CA'}]}, {'_id': {'$oid': '653aef5bbe867985ad4ca681'}, 'profile_id': {'$oid': '653836c97e361c1a21f806d2'}, 'portal_id': '39473', 'portals': [{'_id': {'$oid': '6526cdc1518a72e0eddfee94'}, 'portalId': '39473', 'portalName': 'Contra Costa Transportation Authority', 'portalState': 'CA'}]}, {'_id': {'$oid': '653aef5bbe867985ad4ca682'}, 'profile_id': {'$oid': '653836c97e361c1a21f806d2'}, 'portal_id': '31333', 'portals': [{'_id': {'$oid': '6526cdc1518a72e0eddfef39'}, 'portalId': '31333', 'portalName': 'City of Fort Myers', 'portalState': 'FL'}]}, {'_id': {'$oid': '653aef5cbe867985ad4ca683'}, 'profile_id': {'$oid': '653836c97e361c1a21f806d2'}, 'portal_id': '49083', 'portals': [
    {
        '_id': {'$oid': '6526cdc1518a72e0eddfef46'}, 'portalId': '49083', 'portalName': 'Nassau County', 'portalState': 'FL'}]}, {'_id': {'$oid': '653aef5cbe867985ad4ca684'}, 'profile_id': {'$oid': '653836c97e361c1a21f806d2'}, 'portal_id': '50907', 'portals': [{'_id': {'$oid': '6526cdc1518a72e0eddfef34'}, 'portalId': '50907', 'portalName': 'Austin Transit Partnership', 'portalState': 'TX'}]}, {'_id': {'$oid': '653aef5cbe867985ad4ca685'}, 'profile_id': {'$oid': '653836c97e361c1a21f806d2'}, 'portal_id': '39494', 'portals': [{'_id': {'$oid': '6526cdc1518a72e0eddfef37'}, 'portalId': '39494', 'portalName': 'Capital Metropolitan Transportation Authority', 'portalState': 'TX'}]}, {'_id': {'$oid': '653aef5cbe867985ad4ca686'}, 'profile_id': {'$oid': '653836c97e361c1a21f806d2'}, 'portal_id': '44198', 'portals': [{'_id': {'$oid': '6526cdc1518a72e0eddfef3f'}, 'portalId': '44198', 'portalName': 'Ennis Independent School District', 'portalState': 'TX'}]}, {'_id': {'$oid': '653aef5cbe867985ad4ca687'}, 'profile_id': {'$oid': '653836c97e361c1a21f806d2'}, 'portal_id': '53284', 'portals': [{'_id': {'$oid': '6526cdc1518a72e0eddfef3a'}, 'portalId': '53284', 'portalName': 'City of Grand Prairie', 'portalState': 'TX'}]}, {'_id': {'$oid': '653aef5dbe867985ad4ca688'}, 'profile_id': {'$oid': '653836c97e361c1a21f806d2'}, 'portal_id': '32621', 'portals': [{'_id': {'$oid': '6526cdc1518a72e0eddfef43'}, 'portalId': '32621', 'portalName': 'Indianapolis Airport Authority', 'portalState': 'IN'}]}, {'_id': {'$oid': '653aef5dbe867985ad4ca689'}, 'profile_id': {'$oid': '653836c97e361c1a21f806d2'}, 'portal_id': '48213', 'portals': [{'_id': {'$oid': '6526cdc1518a72e0eddfef3e'}, 'portalId': '48213', 'portalName': 'DOWL / Farr West Engineering', 'portalState': 'NV'}]}, {'_id': {'$oid': '653aef5dbe867985ad4ca68a'}, 'profile_id': {'$oid': '653836c97e361c1a21f806d2'}, 'portal_id': '40669', 'portals': [{'_id': {'$oid': '6526cdc1518a72e0eddfef3c'}, 'portalId': '40669', 'portalName': 'City of Reno', 'portalState': 'NV'}]}]


# print((ls[0]))

# item = {'_id': {'$oid': '653aef5abe867985ad4ca67c'}, 
#       'profile_id': {'$oid': '653836c97e361c1a21f806d2'}, 
#       'portal_id': '21147', 
#       'portals': 
#       [{'_id': {'$oid': '6526cdc1518a72e0eddfef35'}, 'portalId': '21147', 'portalName': 'Birmingham City Schools', 'portalState': 'AL'}]}




payload = []
for item in ls:
    template =  {
        "state": item['portals'][0]['portalState'],
        "projectName": [
            {
                "portalId": item["portal_id"],
                "portalName": item['portals'][0]['portalName']
            }
        ]
    }
    state_found = False
    for i in payload:
        if i['state'] == item['portals'][0]['portalState']:
            i['projectName'].append(template['projectName'][0])
            state_found = True
    if not state_found:
        payload.append(template)

print(payload)

ad = [
    {'state': 'AL', 
     'projectName': [
         {'portalId': '21147', 'portalName': 'Birmingham City Schools'}, 
         {'portalId': '55902', 'portalName': 'Birmingham-Jefferson County Transit Authority'}]}
         , 
    {'state': 'CA', 
     'projectName': [
         {'portalId': '24103', 'portalName': 'City of National City'}, 
         {'portalId': '46106', 'portalName': 'City of Burlingame'}, 
         {'portalId': '42510', 'portalName': 'City of Vallejo'}, 
         {'portalId': '39473', 'portalName': 'Contra Costa Transportation Authority'}]}, 
    {'state': 'FL', 
     'projectName': [
         {'portalId': '31333', 'portalName': 'City of Fort Myers'}, 
         {'portalId': '49083', 'portalName': 'Nassau County'}]}, 
    {'state': 'TX', 
     'projectName': [
         {'portalId': '50907', 'portalName': 'Austin Transit Partnership'}, 
         {'portalId': '39494', 'portalName': 'Capital Metropolitan Transportation Authority'}, 
         {'portalId': '44198', 'portalName': 'Ennis Independent School District'}, 
         {'portalId': '53284', 'portalName': 'City of Grand Prairie'}]}, 
    {'state': 'IN', 
     'projectName': [
         {'portalId': '32621', 'portalName': 'Indianapolis Airport Authority'}]}, 
    {'state': 'NV', 
     'projectName': [
         {'portalId': '48213', 'portalName': 'DOWL / Farr West Engineering'}, 
         {'portalId': '40669', 'portalName': 'City of Reno'}]}]