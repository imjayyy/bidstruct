from flask import Flask, request, jsonify, make_response
from flask_pymongo import PyMongo, ObjectId
import bcrypt
import jwt
from datetime import datetime, timedelta
from models.connection import users
from flask import Blueprint, current_app
from flask_jwt import JWT, jwt_required, current_identity
from models.portalModel import Portal
from models.profile import Profile
from stripe_ import checkout_function, stripe_keys, handle_checkout_session, fetch_subscription_data, get_products_list
import stripe
from flask_cors import CORS, cross_origin
from bson import json_util
import json

from flask_restful import Api


portal_api_blueprint = Blueprint('portal_api', __name__)

# CORS(portal_api_blueprint)

api = Api(portal_api_blueprint)

@portal_api_blueprint.after_request
def after_request(response):
    # response.headers.add('Access-Control-Allow-Origin', '*')
    # response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    # response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    # print(request.headers)
    # print(response.headers)
    return response




@portal_api_blueprint.route('/getPortalData', methods=['POST'])
@jwt_required()

def getPortalData():
    """
    Logged in User, getting Portal Data... 
    """
    data = fetch_subscription_data(current_identity.get('email'))
    if data['subscription'] == None:
        return jsonify({"error": 'You are not subscribed to the any package.'}), 400
    elif data['product']['active'] == False:
        return jsonify({"error": 'Your package has expired, please resubscribe.'}), 400

    else :
        data = request.get_json()  
        if  data != {}:
            portal_id = data.get('portalId') 
            if portal_id:
                data = Portal.get_portal_data(portal_id)
                return data, 200
            else:
                return jsonify({"error": "Field 'portalId' is missing from the form data."}), 400
        else:
            return jsonify({"error": "No form data found in the request."}), 400


@portal_api_blueprint.route('/getPortalList', methods=['GET'])
def getPortalList():
    """
    Getting Portal List... 
    """
    data = Portal.getPortalList()
    return data, 200


@portal_api_blueprint.route('/getAvailableStates', methods=['GET'])
def getAvailableStates():
    """
    Getting Available States List... 
    """
    data = Portal.get_available_states()
    return list(data), 200


@portal_api_blueprint.route('/getUsersProfilesList', methods=['GET'])
@jwt_required()

def get_users_profiles_list():
    """
    Logged In Required: Get All Users Profiles..
    """
    user_id = str(current_identity.get('_id'))
    list__ = Profile.get_users_profiles_list(user_id)
    return jsonify({"profiles" : list__}), 200


@portal_api_blueprint.route('/listPortalsByState', methods=['POST'])
@jwt_required()

def listPortalsByState():
    """
    Getting Portal List by state... 

    """
    # return {'msg':"Hey"}
    data = request.get_json()
    if data != {} :
        portalState = data.get('portalState')  
        if portalState:
            data = Portal.list_portals_by_state(portalState)
            return list(data), 200
        else:
            return jsonify({"error":"portalState field is missing from the form data"}), 400
    else:
        return jsonify({"error": "No form data found in the request."}), 400


@portal_api_blueprint.route('/getProfilePortalList', methods=['POST'])
@jwt_required()

# @cross_origin
def getProfilePortalList():
    """
    Getting Portal List for a specific User Profile... Form Data : ["profileName":str]
    """
    user_id = str(current_identity.get('_id'))
    data = request.get_json()
    print(data)
    if data != {} :
        profileName = data.get('profileName').get("profile_name")
        if profileName:
            data = Profile.get_portal_list(profileName, user_id)    
            data = json.loads(json_util.dumps(data))
            payload = []
            for item in data:
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

            return jsonify(payload), 200
        else:
            print({"error":"profileName field is missing from the form data"})
            return jsonify({"error":"profileName field is missing from the form data"}), 400
    else:
        print({"error":"No form data found in the request."})
        return jsonify({"error": "No form data found in the request."}), 400


@portal_api_blueprint.route('/getCatList', methods=['GET'])
def getCatList():
    """
    Getting Categories List... 
    """
    data = Portal.getCatList()
    return data, 200


@portal_api_blueprint.route('/addProfile', methods=['POST'])
@jwt_required()

# 
def addProfile():
    """
    Logged in User, Add Profile. Form Data : "profileName"
    """
    user_id = str(current_identity.get('_id'))
    data = request.get_json()
    if data != {} :
        profileName = data.get('profileName')       
        if profileName:
            data = Profile.add_profile(user_id, current_identity.get('email'), profileName)
            return data, 200
        else:
            return jsonify({"error": "Field 'profileName' is missing from the form data."}), 400
    else:
        return jsonify({"error": "No form data found in the request."}), 400


@portal_api_blueprint.route('/checkout', methods=['POST'])
@jwt_required()
def checkout():
    """
    Logged in User, Stripe Checkout, It returns a checkout URL of Stripe where payment info will be provided by the user. FormData : "quantity"
    """
    data = request.get_json()
    if data != {} :
        quantity = data.get('quantity')       
        if quantity:
            user_id = (current_identity.get('_id'))
            user = (users.find_one({"_id" : user_id} ))
            response = checkout_function(request.host, user['email'], quantity)
            return response, 200
        else:
            return jsonify({"error": "Field 'quantity' is missing from the form data."}), 400
    else:
        return jsonify({"error": "No form data found in the request."}), 400

@portal_api_blueprint.route('/get_subscription_data', methods=['POST'])
@jwt_required()
def get_subscription_data():
    email = str(current_identity.get('email'))
    data = fetch_subscription_data(email)
    if data['subscription'] == None:
        return data, 200
    return data, 200

@portal_api_blueprint.route('/addPortalsToProfile', methods=['POST'])
@jwt_required()
def addPortalsToProfile():
    """
    Logged in User, Add Portals to Profile. Form Data : str:"profileName", Array:"portalsList" 
    """
    user_id = str(current_identity.get('_id'))
    data = request.get_json()
    if data != {} :
        profileName = data.get('profileName') 
        portalsList = data.get('portalsList') 
        if profileName and portalsList:
            message = Profile.add_portals(user_id, profileName, portalsList)
            return jsonify({"success": message}), 200

        else:
            return jsonify({"error": "Field 'profileName' or 'portalsList' is missing from the form data."}), 400
    else:
        return jsonify({"error": "No form data found in the request."}), 400




@portal_api_blueprint.route("/get-package-details", methods=["POST"])
def get_package_details():
    """ Get package list and description """
    return make_response(get_products_list(), 200)
    






@portal_api_blueprint.route("/stripe-webhook", methods=["POST"])
def stripe_webhook():
    """
    Stripe Webhook, Stripe hits this webhook to save user data for a successful checkout.
    """
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get("Stripe-Signature")
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, stripe_keys["endpoint_secret"]
        )
    except ValueError as e:
        # Invalid payload
        return "Invalid payload", 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return "Invalid signature", 400
    # Handle the checkout.session.completed event
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        # Fulfill the purchase...
        print(session)
        handle_checkout_session(session)

    return "Success", 200


