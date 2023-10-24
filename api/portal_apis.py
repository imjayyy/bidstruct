from flask import Flask, request, jsonify
from flask_pymongo import PyMongo, ObjectId
import bcrypt
import jwt
from datetime import datetime, timedelta
from models.connection import users
from flask import Blueprint, current_app
from flask_jwt import JWT, jwt_required, current_identity
from models.portalModel import Portal
from models.profile import Profile
from stripe_ import checkout_function, stripe_keys, handle_checkout_session, fetch_subscription_data
import stripe
from flask_cors import CORS, cross_origin
from bson import json_util
import json


portal_api_blueprint = Blueprint('portal_api', __name__)

CORS(portal_api_blueprint, support_credentials=True)

@portal_api_blueprint.route('/getPortalData', methods=['POST'])
@jwt_required()
@cross_origin(supports_credentials=True)
def getPortalData():
    """
    Logged in User, getting Portal Data... 
    """
    data = fetch_subscription_data(current_identity.get('email'))
    if data['subscription'] == None:
        return jsonify({"error": 'You are not subscribed to the any package.'}), 400
    elif data['product']['active'] == False:
        return jsonify({"error": 'Your package has expired, please resubscribe.'}), 400

    elif request.form:
        portal_id = request.form.get('portalId') 
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
@cross_origin(supports_credentials=True)
def get_users_profiles_list():
    """
    Logged In Required: Get All Users Profiles..
    """
    user_id = str(current_identity.get('_id'))
    list__ = Profile.get_users_profiles_list(user_id)
    return list__, 200


@portal_api_blueprint.route('/listPortalsByState', methods=['GET'])
def listPortalsByState():
    """
    Getting Portal List by state... 
    """
    if request.form:
        portalState = request.form.get('portalState')  
        if portalState:
            data = Portal.list_portals_by_state(portalState)
            return list(data), 200
        else:
            return jsonify({"error":"portalState field is missing from the form data"}), 400
    else:
        return jsonify({"error": "No form data found in the request."}), 400


@portal_api_blueprint.route('/getProfilePortalList', methods=['GET'])
@jwt_required()
@cross_origin(supports_credentials=True)
def getProfilePortalList():
    """
    Getting Portal List for a specific User Profile... Form Data : ["profileName":str]
    """
    user_id = str(current_identity.get('_id'))
    if request.form:
        profileName = request.form.get('profileName')  
        if profileName:
            data = Profile.get_portal_list(profileName, user_id)
            data = json.loads(json_util.dumps(data))
            return jsonify(list(data)), 200
        else:
            return jsonify({"error":"profileName field is missing from the form data"}), 400
    else:
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
# @cross_origin(supports_credentials=True)
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
# @cross_origin(supports_credentials=True)
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
# @cross_origin(supports_credentials=True)
def get_subscription_data():
    email = str(current_identity.get('email'))
    context = fetch_subscription_data(email)
    return context

@portal_api_blueprint.route('/addPortalsToProfile', methods=['POST'])
@jwt_required()
@cross_origin(supports_credentials=True)
def addPortalsToProfile():
    """
    Logged in User, Add Portals to Profile. Form Data : str:"profileName", Array:"portalsList" 
    """
    user_id = str(current_identity.get('_id'))

    if request.form:
        profileName = request.form.get('profileName') 
        portalsList = request.form.getlist('portalsList') 
        if profileName and portalsList:
            message = Profile.add_portals(user_id, profileName, portalsList)
            return jsonify({"success": message}), 200

        else:
            return jsonify({"error": "Field 'profileName' or 'portalsList' is missing from the form data."}), 400
    else:
        return jsonify({"error": "No form data found in the request."}), 400






@portal_api_blueprint.route("/stripe-webhook", methods=["POST"])
@cross_origin(supports_credentials=True)
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


