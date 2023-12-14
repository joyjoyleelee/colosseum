import os
from os.path import join, dirname, realpath

from flask import Flask, flash, request, redirect
from flask import make_response, render_template, send_from_directory
from flask_socketio import SocketIO
from pymongo import MongoClient
from werkzeug.utils import secure_filename

UPLOADS_PATH = join(dirname(realpath(__file__)), 'static/client_images')

# My Imports
from database import Database
from user_functions import User



app = Flask(__name__)
UPLOAD_FOLDER =UPLOADS_PATH
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'jfif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["SECRET_KEY"] = "Marco_is_always_the_key"
socketio = SocketIO(app)
"""
        --  Establish the mongo database --
        Set up collections for the following:
        - Registered usernames (username, password) = COLLECTION_USERS
        - Tokens (authToken, username) = COLLECTION_TOKENS
        - Listing (creator, creator_authToken, time_remaining, open(bool), bidders[], current
                    winner, title, description, id) = COLLECTION_LISTINGS
        A Listing includes info below: 
        creator_username, creator_authToken, time_remaining, open: (true or false) 
        bidders[], winner, current_bid
        Each dictionary represents one individual listing. Listing Format:
        {creator: , creator_token: , time_remaining: , open: true, bidders: [], winner: , bid: 0}
"""

mongo_client = MongoClient("localhost")
DB = mongo_client["NewRome"]
Database = Database() # Database Object I create for functionality

Database.xxx(DB)

@app.route("/") #index.html
def render_home():
    response = make_response(render_template("index.html"), 200)
    response.headers["X-Content-Type-Options"] = "nosniff"
    flash('hey')
    return response

# Register and Login User
@app.route("/register", methods=["POST"])
def register_user():
    user = User()
    username = request.form['username_reg']
    password = request.form['password_reg']
    user.register(username, password, DB)
    return redirect("/account")
@app.route("/login", methods=["POST"])
def login_user():
    user = User()
    username = request.form["username_login"]
    password = request.form["password_login"]
    auth_token = user.login(username, password, DB)
    if auth_token == "":
        response = make_response("Account Doesn't Exist", 404)
        return response
    else:
        response = make_response(redirect("/auctions_create"))
        response.set_cookie("auth_token", str(auth_token), max_age=3600, httponly=True)
        return response

@app.route("/account")
def render_account_info():
    response = make_response(render_template("account.html"), 200)
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response

@app.route("/auctions_create")
def render_auctions_create():
    response = make_response(render_template("auctions_create.html", filename='client_images/default.png'), 200)
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response

@app.route("/auctions_list")
def render_auctions_list():
    response = make_response(render_template("auctions_list.html", filename='client_images/default.png'), 200)
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response

@app.route("/auctions_won")
def render_auctions_won():
    response = make_response(render_template("auctions_won.html", filename='client_images/default.png'), 200)
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response

@app.route("/dark_web")
def render_dark_web():
    response = make_response(render_template("dark_web.html", filename='client_images/dark-default.png'), 200)
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/listing-img', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return "Missing Image"
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return "Missing Image"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template('auctions_create.html',filename='client_images/'+filename)
        return "Must submit an image"




# Host All Static Files
@app.route("/<path:file>")
def static_files(file):
    response = make_response(send_from_directory("static", file), 200)
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response

@app.route("/static/<file>")
def image_file(file):
    response = make_response(send_from_directory("static", file), 200)
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response
""" 
    --- Web Socket Connections Below ---
"""

@socketio.on("listing-create")
def connect(listing_json):
    """ This function takes in a JSON format dictionary of the info needed to create the listing.
        It creates the listing and adds it to the database. Then it emits back to JavaScript
        So that JavaScript can update all listings
    """
    print(f'def connect(listing_json): \n{listing_json}')
    auth_token = request.cookies.get('auth_token', 'Guest')
    username = Database.get_username(auth_token, DB)
    Database.add_new_listing(username, auth_token, listing_json, DB)
    all_listings = Database.retrieve_user_listings(username, DB)
    socketio.emit("display_user_listings", all_listings) # Publish all user listings immediately after creating one


@socketio.on("retrieve_user_listings")
def history_user():
    print("Retrieving user history from server")
    """ This function retrieves and displays all user created listings via Web Sockets"""
    auth_token = auth_token = request.cookies.get('auth_token', 'Guest')
    username = Database.get_username(auth_token, DB)
    all_listings = Database.retrieve_user_listings(username, DB)
    socketio.emit("display_user_listings", all_listings)
@socketio.on("update_bid")
def up_bid(bidId,price):
    if  Database.valid_bid() == True:
        auth_token = auth_token = request.cookies.get('auth_token', 'Guest')
        username = Database.get_username(auth_token, DB)
        Database.update_bid(username,DB,bidId,price)


socketio.run(app=app, host = "0.0.0.0", port = 8080, allow_unsafe_werkzeug=True)