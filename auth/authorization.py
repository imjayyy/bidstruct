from flask import Flask, request, jsonify
from flask_pymongo import PyMongo, ObjectId
import bcrypt
import jwt
from datetime import datetime, timedelta
from models.connection import users
# auth_blueprint.py
from flask import Blueprint, current_app
from flask_jwt import JWT, jwt_required, current_identity

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data['email']
    password = data['password']

    # Check if the email is already in use
    if users.find_one({'email': email}):
        return jsonify({'message': 'Email already exists'}), 400

    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Insert the user into the database
    user_id = users.insert_one({'email': email, 'password': hashed_password})
    
    return jsonify({'message': 'User registered successfully'}), 201

@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    # Find the user by email
    user = users.find_one({'email': email})

    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        # Generate a JWT token
        token = jwt.encode({'user_id': str(user['_id']), 'email' : user['email'], 'exp': datetime.utcnow() + current_app.config['JWT_EXPIRATION_DELTA']}, current_app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token})

    return jsonify({'message': 'Invalid credentials'}), 401




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
    user_id = str(current_identity.get('_id'))
    return jsonify({'message': 'This is a protected route for authenticated users.',
                    'user_id': user_id
                    })
