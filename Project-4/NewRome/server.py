import datetime
import json
import os
import time
from os.path import join, dirname, realpath

from flask import Flask, flash, request, redirect, url_for, session
from flask import make_response, render_template, send_from_directory
from flask_socketio import SocketIO
from pymongo import MongoClient
from werkzeug.utils import secure_filename



UPLOADS_PATH = join(dirname(realpath(__file__)), 'static/client_images')

# My Imports
from database import Database
from user_functions import User
from auth import Auth


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
Validate = Auth()

@app.route("/") #index.html
def render_home():
    response = make_response(render_template("index.html"), 200)
    response.headers["X-Content-Type-Options"] = "nosniff"
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
        session["username"] = Database.get_username(auth_token, DB) #
        return response

@app.route("/account")
def render_account_info():
    response = make_response(render_template("account.html"), 200)
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route("/auctions_create", methods=["GET", "POST"])
def render_auctions_create():
    # Validate user token
    if not Validate.user_isAuthorized(request.cookies.get("auth_token", ""), DB):
        return make_response(redirect("/account"), 401)
    # User's not logged in
    if request.method == "GET":
        response = make_response(render_template("auctions_create.html", filename='client_images/default.png', creator="Me"), 200)
        response.headers["X-Content-Type-Options"] = "nosniff"
        return response
    elif request.method == 'POST':
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
            username = Database.get_username(request.cookies.get("auth_token"), DB)
            return render_template('auctions_create.html',filename='client_images/'+filename, creator=username)
        return "Must submit an image"

@app.route("/auctions_list")
def render_auctions_list():
    # Validate user token
    if not Validate.user_isAuthorized(request.cookies.get("auth_token", ""), DB):
        return make_response(redirect("/account"), 401)
    # User's not logged in
    response = make_response(render_template("auctions_list.html", filename='client_images/default.png'), 200)
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response

@app.route("/auctions_won")
def render_auctions_won():
    # Validate user token
    if not Validate.user_isAuthorized(request.cookies.get("auth_token", ""), DB):
        return make_response(redirect("/account"), 401)
    # User's not logged in
    response = make_response(render_template("auctions_won.html", filename='client_images/default.png'), 200)
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response

""" 
    --- Easter Eggs ---
"""
@app.route("/dark_web")
def render_dark_web():
    # Validate user token
    if not Validate.user_isAuthorized(request.cookies.get("auth_token", ""), DB):
        return make_response(redirect("/account"), 401)
    # User's not logged in
    response = make_response(render_template("dark_web.html", filename='client_images/dark-default.png'), 200)
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response

@app.route("/light-web")
def render_light_web():
    # Validate user token
    if not Validate.user_isAuthorized(request.cookies.get("auth_token", ""), DB):
        return make_response(redirect("/account"), 401)
    # User's not logged in
    response = make_response(render_template("light_web.html"),200)
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response



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

@socketio.on('listing-create')
def connect(listing_json):

    """ This function takes in a JSON format dictionary of the info needed to create the listing.
        It creates the listing and adds it to the database. Then it emits back to JavaScript
        So that JavaScript can update all listings
    """
    # Error Message
    if not Validate.listing_hasImage(listing_json.get('img')):
        e_mesg = "400 - Upload your image and submit that first!"
        socketio.emit("display_error", e_mesg)
    else:
        if listing_json.get("bid","").isalpha() or listing_json.get("time").isalpha():
            # Error Message
            e_mesg = "400 - Must submit and int or float"
            socketio.emit("display_error", e_mesg)
            # Rest of the Code
        else:
            # Rest of the Code
            auth_token = request.cookies.get('auth_token', 'Guest')
            username = Database.get_username(auth_token, DB)
            Database.add_new_listing(username, auth_token, listing_json, DB)
            all_listings = Database.retrieve_user_listings(username, DB)
            socketio.emit("display_user_listings", all_listings)

@socketio.on("retrieve_won_listings")
def history_user():
    # print("Retrieving user history from server")
    """ This function retrieves and displays all user created listings via Web Sockets"""
    auth_token = auth_token = request.cookies.get('auth_token', 'Guest')
    username = Database.get_username(auth_token, DB)
    all_listings = Database.retrieve_won_listings(username, DB)
    socketio.emit("display_won_listings", all_listings)

@socketio.on("retrieve_open_listings")
def history_all():
    auth_token = request.cookies.get('auth_token', 'Guest')
    username = Database.get_username(auth_token, DB)
    open_listings = Database.retrieve_open_listings(DB)
    socketio.emit("display_open_listings", open_listings)


@socketio.on("retrieve_user_listings")
def history_user():
    # print("Retrieving user history from server")
    """ This function retrieves and displays all user created listings via Web Sockets"""
    auth_token = auth_token = request.cookies.get('auth_token', 'Guest')
    username = Database.get_username(auth_token, DB)
    all_listings = Database.retrieve_user_listings(username, DB)
    socketio.emit("display_user_listings", all_listings)

@socketio.on("update_bid")
def up_bid(json_dict):
    bid_value = json.loads(json_dict)
    bid_value = bid_value.get("price")
    # Error Message
    if not Validate.bid_isNumber(bid_value):
        e_mesg = "400 - Must submit and int or float"
        socketio.emit("display_error", e_mesg)
    # Rest of the Code
    # if  Database.valid_bid() == True:
    auth_token = auth_token = request.cookies.get('auth_token', 'Guest')
    username = Database.get_username(auth_token, DB)
    pydict = json.loads(json_dict)
    # Check to see if its own bid.
    DB_obj = DB["COLLECTION_LISTINGS"].find_one({"_id": pydict.get('iditem')})
    creator = DB_obj.get("creator")
    if creator == username:
        e_mesg = "Can't submit on your own bid"
        socketio.emit("display_error", e_mesg)
    else:
        # It's not own bid
        Database.update_bid(username, DB, pydict.get('iditem'), pydict.get('price'))
        id = pydict.get("iditem")
        new_bid = Database.get_bid(id, DB)
        data = {'id': id, 'new_bid': new_bid}
    # socketio.emit("update_bid_client", data)


@socketio.on("update_listings")
def retrieve_updates():
    """ This function goes through the database and constantly updates the timer remaining on each auction
        It returns nothing it's intended for functionality, NOT for actual use.
    """
    all_listings = Database.retrieve_all_listings(DB)
    # print(f"This is what I'm updating with:--------------------\n{all_listings}\n---------------")
    socketio.emit("display_updated_listings", all_listings)

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

""" ----- Rate Limiting -----"""


ip_list = DB["COLLECTION_IP"]
bans = DB["COLLECTION_BANS"]

# def get_client_ip():
#     # Check X-Real-IP header first, then fallback to remote_addr
#     client_ip = request.headers.get('X-Real-IP', request.remote_addr)
#     print(client_ip)
#     return f'Client IP Address: {client_ip}'


@app.before_request
def DOS_prevention():
    # Function verifies that user is allowed to make a request
    curr_time = time.time()
    client_ip = request.remote_addr
    ip_list.insert_one({"ip": client_ip, "time": curr_time})
    visits = list(ip_list.find({"ip": client_ip}))
    #TimeLimit is the time tracking the allotted requests
    timeLimit = 10
    for i in visits:
        if curr_time-i["time"]>timeLimit:
            visits.remove(i)
            ip_list.delete_one(i)
    existing = bans.find({"ip": client_ip})
    for document in existing:
        if curr_time - document["time"] < 30:
            response = make_response("You are still banned")
            response.status_code = 429
            return response
        bans.delete_one({"_id": document["_id"]})

    #Limit is the number of requests allowed in 10 seconds
    limit = 50
    if len(visits)>limit:
        bans.insert_one({"ip": client_ip, "time": curr_time})
        response = make_response("You are still banned")
        response.status_code = 429
        return response


@app.errorhandler(429)
def handle_DOS_error(error):
    return f"Too many requests Refresh After 30 seconds"


@app.after_request
def add_header(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response


socketio.run(app=app, host = "0.0.0.0", port = 8080, allow_unsafe_werkzeug=True)