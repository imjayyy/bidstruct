from datetime import datetime 
from Scrapper.scrapper import get_data
from flask import jsonify

from models.connection import portals, portal_list, categories



class Portal:
    def __init__(self) -> None:
        pass

    def update_portal_data(portal_number):
        data_dict = {
            'portal' : portal_number,
            'time' : datetime.now(),
            'portal_data' : get_data(portal_number),
        }
        portals.update_one( {'portal' : portal_number} , {'$set' : data_dict}, upsert=True )

    def get_portal_data(portal_number):

        data = portals.find_one({'portal' : portal_number}, {'_id' : 0}  )    
        # cursor_data = [record for record in data]
        if data == None:
            Portal.update_portal_data(portal_number)
            data = portals.find_one({'portal' : portal_number}, {'_id' : 0} )    
        
        # Parse the date string into a datetime object
        # date_obj = datetime.strptime(data['time'], "%Y-%m-%dT%H:%M:%S.%f%z")

        date_difference =  datetime.now() - data['time']
        if date_difference.days >= 2:
            Portal.update_portal_data(portal_number)

        data = portals.find_one({'portal' : portal_number}, {'_id' : 0} )    

        return jsonify(data)

    def getCatList():
        data = categories.find({} , {'_id' : 0})    
        cursor_data = [record for record in data]
        return jsonify(cursor_data)

    def getPortalList():
        data = portal_list.find({} , {'_id' : 0})    
        cursor_data = [record for record in data]
        return jsonify(cursor_data)
