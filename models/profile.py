from models.connection import users, user_profile, profile_portals
from flask_admin.contrib.pymongo import ModelView
from flask_admin import model
from flask import current_app
from flask_admin.contrib.pymongo.filters import BooleanEqualFilter
from stripe_ import fetch_subscription_data


class User():
    pass


class Profile():
    def __init__(self) -> None:
        pass
    
    def add_profile(user_id, email, profile_name):
        count = user_profile.count_documents({ "user_id" : user_id })

        data = fetch_subscription_data(email)

        if data['subscription'] == None:
            return 'You are not subscribed to the any package.'
        elif count < data['subscription']['quantity'] :
            user_profile.insert_one({
                "user_id" : user_id,
                "profile_name" : profile_name            
            })
            return "Profile Added"
        return f"User Already Has {data['subscription']['quantity']} Profiles."

    def add_portals(profile_id, portal_id):            
        try:
            profile_portals.delete_many({ "profile_id" : profile_id })
            for portal in portal_id:
                profile_portals.insert_one({"profile_id": profile_id, "portal_id": portal})
            return ("Portals Added to profile.", True)
        except Exception as e:
            return (e, False)
        
    def get_portal_list(profile_id):
        pipeline = [
            {
                "$match": {"profile_id": profile_id}
            },
            {
                "$lookup": {
                    "from": "PortalList",
                    "localField": "portal_id",
                    "foreignField": "portalId",
                    "as": "portals"
                }
            },
            {
                "$unwind": "$portals"
            },
            {
                "$project": {
                    "_id": 0,
                    "portalId": "$portals.portalId",
                    "portalName": "$portals.portalName",
                    "portalState": "$portals.portalState"
                }
            }
        ]


        portals_info = list( profile_portals.aggregate(pipeline) )

        return portals_info
