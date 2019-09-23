# Python standard libraries
import json
import os
from flask import Flask, render_template, redirect, request, url_for
import sqlite3 as sql
import numpy as np
from graph import build_graph

from flask_login import (
                         LoginManager,
                         current_user,
                         login_required,
                         login_user,
                         logout_user,
                         )
from oauthlib.oauth2 import WebApplicationClient
import requests

# Internal imports
from db import init_db_command
from user import User

# Configuration
GOOGLE_CLIENT_ID = '780948375532-gpg6gl3o6t2cpamhejtf5ut70b42rbtu.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = 'IIsvknkPfRG-odskaxklenDz'
GOOGLE_DISCOVERY_URL = (
                        "https://accounts.google.com/.well-known/openid-configuration"
                        )


# Flask app setup
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

# User session management setup
# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.init_app(app)

# Naive database setup
try:
    init_db_command()
except sql.OperationalError:
    # Assume it's already been created
    pass


# OAuth 2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)

# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route('/')
def home():
    if current_user.is_authenticated:
        return render_template('home.html', username = current_user.name, profile_picture = current_user.profile_pic)
    else:
        return '<a class="button" href="/login">Google Login</a>'

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

@app.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    
    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
                                             authorization_endpoint,
                                             redirect_uri=request.base_url + "/callback",
                                             scope=["openid", "email", "profile"],
                                             )
    return redirect(request_uri)

@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
                                                            token_endpoint,
                                                            authorization_response=request.url,
                                                            redirect_url=request.base_url,
                                                            code=code
                                                            )
    token_response = requests.post(
                                   token_url,
                                   headers=headers,
                                   data=body,
                                   auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
                                   )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    # Create a user in your db with the information provided
    # by Google
    user = User(
                id_=unique_id, name=users_name, email=users_email, profile_pic=picture
                )

    # Doesn't exist? Add it to the database.
    if not User.get(unique_id):
        User.create(unique_id, users_name, users_email, picture)

    # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage
    return redirect(url_for("home"))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route('/entersensor')
def new_sensor():
    return render_template('add_sensor.html')

@app.route('/addsensor', methods=['POST', 'GET'])
def add_sensor():
    if request.method == 'POST':
        s_nm = request.form['sensor_name']
        s_type = request.form['sensor_type']

        random_id = np.random.randint(0,10000)
        User.add_sensor(random_id, current_user.id, s_nm, s_type)

        return render_template('result.html')


@app.route('/displaysensors')
def display_sensors():
    sensor_list = User.get_sensors(current_user.id)
    humidity_sensors = []
    temperature_sensors = []
    for sensor in sensor_list:
        sensor_dict = dict(zip(sensor.keys(), sensor))
        if sensor_dict["sensor_type"] == "Humidity":
            humidity_sensors.append(sensor_dict["sensor_name"])
        elif sensor_dict["sensor_type"] == "Temperature":
            temperature_sensors.append(sensor_dict["sensor_name"])
    
    plot_url = build_graph(humidity_sensors, temperature_sensors)

    return render_template('display_sensors.html', graph=plot_url)

@app.route('/list')
def list():
    rows = User.list()
    return render_template('list.html', rows=rows)

if __name__ == '__main__':
    app.run(ssl_context="adhoc")


            
