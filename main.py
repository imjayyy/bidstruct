from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from datetime import timedelta
from flask_jwt import JWT, jwt_required, current_identity
from auth.authorization import authenticate, identity, auth_blueprint
from api.portal_apis import portal_api_blueprint
from flask_admin import Admin
from flask_basicauth import BasicAuth
from flask_admin.contrib.pymongo import ModelView

from models.profile import User


app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/Bidstruct'  # Replace with your MongoDB URI
app.config['MONGODB_SETTINGS'] = {'DB': 'BidStruct'}
db = PyMongo(app).db

# JWT secret key
app.config['SECRET_KEY'] = 'kjdfaslkdjhfoiwuehfnoeih923keydaw23rfws'

# JWT expiration time
app.config['JWT_EXPIRATION_DELTA'] = timedelta(days=3)
jwt = JWT(app, authenticate, identity)

app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(portal_api_blueprint, url_prefix='/api')


# Configure basic authentication
app.config['BASIC_AUTH_USERNAME'] = 'user'
app.config['BASIC_AUTH_PASSWORD'] = 'pass'
basic_auth = BasicAuth(app)

# Initialize Flask-Admin
admin = Admin(app, name='Flask-Admin Example', template_mode='bootstrap3')

@app.route("/")
def hello_world():
    return "<p> Welcome to BidStruct APIs..!!! </p>"

@app.route("/success")
def success():
    return "Success"

@app.route("/cancel")
def cancelled():
    return "Cancel"

if __name__ == '__main__':
    app.run(debug=True)

