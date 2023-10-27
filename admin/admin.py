from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask import Flask, request, session, redirect, url_for
from flask import Blueprint
from werkzeug.security import check_password_hash, generate_password_hash
from models.connection import admin, users, stripe_customer, portals, portal_list
from functools import wraps
import bcrypt
from stripe_ import get_all_customers, get_recent_transactions
from models.portalModel import Portal
admin_blueprint = Blueprint('admin', __name__, template_folder='templates')



def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function



@admin_blueprint.route('/', methods=["GET", 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the user exists in the database
        user = admin.find_one({'username': username})
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            # If the user exists and the password is correct, set up the session
            session['username'] = username
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid Username / Password.', 'error')
    return render_template('/admin/login.html', var = 'Login Admin')


@admin_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Check if the username is already taken
        existing_user = admin.find_one({'username': username})

        if existing_user:
            flash('Username already taken. Please choose a different username.', 'error')
        else:
            # Hash the password before storing it
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            # Store the user in the database
            user_data = {
                'username': username,
                'password': hashed_password,                
            }
            admin.insert_one(user_data)
            
            flash('Registration successful. You can now log in.', 'success')
            return redirect(url_for('/admin/'))  # Redirect to the login page 

    return render_template('admin/login.html', var = 'Register Admin')  # Create an HTML template for the registration form



@admin_blueprint.route('/dashboard', methods=["GET", 'POST'])
def dashboard():
    TOTAL_CUSTOMERS = users.count_documents({})
    ACTIVE_SUBSCRIPTIONS = len(get_all_customers())
    TOTAL_PORTALS = portal_list.count_documents({})
    ACTIVE_STATES = len(Portal.get_available_states())    

    transactions = get_recent_transactions()["data"]

    return render_template("/admin/index.html", TOTAL_CUSTOMERS = TOTAL_CUSTOMERS, 
                           TOTAL_PORTALS= TOTAL_PORTALS, ACTIVE_SUBSCRIPTIONS=ACTIVE_SUBSCRIPTIONS, 
                           ACTIVE_STATES = ACTIVE_STATES, transactions=transactions )