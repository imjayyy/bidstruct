from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_pymongo import PyMongo, ObjectId
import bcrypt
import jwt
from datetime import datetime, timedelta
from models.connection import users
# auth_blueprint.py
from flask import Blueprint, current_app
from flask_jwt import JWT, jwt_required, current_identity
from flask_cors import CORS, cross_origin
from stripe_ import fetch_subscription_data
from flask_restful import reqparse, abort, Api, Resource
import random
import string
from admin.mailing_list import Mailing_Clients





auth_blueprint = Blueprint('auth', __name__)

api = Api(auth_blueprint)
CORS(auth_blueprint, resources={r"/auth/*": {"origins": "*"}})

@auth_blueprint.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    print(str(response.headers))
    return response


@auth_blueprint.route('/register', methods=['POST'])
# @cross_origin()
def register():
    """
    Register User ... Form Data : "email" "password"
    """
    data = request.get_json()
    email = data['email']
    if users.find_one({'email': email}):
        return jsonify({'message': 'Email already exists'}), 400
    payload = {
        'email': email,
        'exp': datetime.utcnow() + timedelta(hours=24)  # Token expires in 24 hours
    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    confirmation_link = f'https://api.bidstruct.com/auth/confirm-email?token={token}'

    Mailing_Clients().send_confirmation_email(email, confirmation_link)
    # password = data['password']

    # # Check if the email is already in use


    # # Hash the password
    # hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # # Insert the user into the database
    # user_id = users.insert_one({'email': email, 'password': hashed_password})
    
    return jsonify({'message': 'Confirmation link sent to email'}), 201



@auth_blueprint.route('/confirm-email', methods=['GET', 'POST'])
def confirm():
    token = request.args.get('token')
    if not token:
        flash('Token is missing/expired.', 'error')
        return render_template('email_template/set_password.html', new_user = True,  token = token)
    payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
    email = payload['email']
    user_ = users.find_one({'email' : email})
    if not user_ :
        if request.method == 'POST':
            password = request.form.get('password')
            token = request.form.get('token')
            try:
                payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                user_id = users.insert_one( {'email': email,'password':hashed_password} )
                flash('SignUp Successful. Please log in now.', 'error')

                return redirect("https://bidstruct.com/?modal=true&type=signin")
            except:
                flash('Error submitting form. Please try again.', 'error')
                return redirect(url_for('auth.confirm'))

        return render_template('email_template/set_password.html', new_user = True,  token = token)


    else:
        flash('Please sign up again, the account already exists or the token is expired.', 'error')
        return redirect(url_for('auth.confirm'))



@auth_blueprint.route('/login', methods=['POST'])
# @cross_origin()
def login():
    """
    Login User ... Form Data : "email" "password"
    """
    data = request.get_json()
    email = data['email']
    password = data['password']

    # Find the user by email
    user = users.find_one({'email': email})

    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        # Generate a JWT token
        # subscription = fetch_subscription_data(user['email'])
        token = jwt.encode({    'user_id': str(user['_id']), 
                                'email' : user['email'], 
                                'exp': datetime.utcnow() + current_app.config['JWT_EXPIRATION_DELTA']}, 
                                current_app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token})

    return jsonify({'message': 'Invalid credentials'}), 401



@auth_blueprint.route('/forgot-password', methods=['POST'])
def forgot_password():
    """ Forgot Password method --> Form Data : 'email' """
    data = request.get_json()
    print(data)
    try:
        email = data['email']
    except:
        return jsonify({'message' : 'Please provide with your email address.'}), 200

    user = users.find_one({'email': email})
    if user:
        payload = {
            'email': email,
            'exp': datetime.utcnow() + timedelta(hours=24)  # Token expires in 24 hours
        }
        token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
        confirmation_link = f'https://api.bidstruct.com/auth/change-pass?token={token}'
        Mailing_Clients().send_password_reset_email(email, confirmation_link)
        return jsonify({'message' : 'Email has been sent to your email address.'}), 200
    else:
        return jsonify({'error' : 'Email does not exist'}), 400


@auth_blueprint.route('/change-pass', methods=['GET', 'POST'])
def change_pass():
    """ Page generated from backend to change password """
    token = request.args.get('token')
    if not token:
        flash('Token is missing/expired.', 'error')
        return render_template('email_template/set_password.html', new_user = True,  token = token)
    payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
    email = payload['email']
    user_ = users.find_one({'email' : email})
    if user_ :
        if request.method == 'POST':
            password = request.form.get('password')
            token = request.form.get('token')
            try:
                payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                user_id = users.update_one( {'email': email},{ '$set' : {'password':hashed_password}} )
                flash('SignUp Successful. Please log in now.', 'error')
                return redirect("https://bidstruct.com/?modal=true&type=signin")
            except:
                flash('Error submitting form. Please try again.', 'error')
                return redirect(url_for('auth.confirm'))
    flash("The account does not exist.", 'error')
    return render_template('email_template/set_password.html', new_user = True,  token = token)





def authenticate(email, password):
    user = users.find_one({'email': email})
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return user

def identity(payload):
    user_id = payload['user_id']
    return users.find_one({'_id': ObjectId(user_id)})


@auth_blueprint.route('/protected', methods=['GET'])
@jwt_required()
def protected_route():
    """
    Test Route for checking logged in users. 
    """
    user_id = str(current_identity.get('_id'))
    return jsonify({'message': 'This is a protected route for authenticated users.',
                    'user_id': user_id
                    })
