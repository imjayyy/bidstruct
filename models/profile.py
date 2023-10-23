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
        profileNameCount = user_profile.count_documents({'user_id': user_id, 'profile_name' : profile_name })
        if profileNameCount > 0:
            return f"User already has a profile named : '{profile_name}', Profile Name must be unique."
        
        if data['subscription'] == None:
            return 'You are not subscribed to the any package.'
        elif count < data['subscription']['quantity'] :
            user_profile.insert_one({
                "user_id" : user_id,
                "profile_name" : profile_name            
            })
            return "Profile Added"
        return f"User Already Has {data['subscription']['quantity']} Profiles."

    def add_portals(user_id, profileName, portal_id):            
        profile_id = user_profile.find_one({'user_id': user_id, "profile_name" : profileName})
        # return portal_id
        if profile_id:
            try:
                profile_id = profile_id['_id']
                profile_portals.delete_many({ "profile_id" : profile_id })
                print(portal_id)
                for portal in portal_id:
                    profile_portals.insert_one({"profile_id": profile_id, "portal_id": str(portal)})
                    
                return ("Portals Added to profile.", True)
            except Exception as e:
                return (e, False)
        else:
            return (f"Profile with the name {profileName} Does not Exist, Please create one.", False)
        
    def get_portal_list(profileName, user_id):
        profile_id = user_profile.find_one({'user_id': user_id, "profile_name" : profileName})['_id']
        pipeline = [{"$match": {"profile_id": profile_id}},
                        {"$lookup": {"from": "portalList",
                                     "localField": "portal_id",
                                     "foreignField": "portalId",
                                     "as": "portals"}}]

        portals_info = list( profile_portals.aggregate(pipeline) )

        return portals_info

    def get_users_profiles_list(user_id):
        p_list = user_profile.find( {"user_id" : user_id} , {"_id" : 0} )
        return list(p_list)