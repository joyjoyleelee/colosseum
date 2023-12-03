from flask import Flask, make_response, render_template, send_from_directory, request, redirect
from flask_socketio import SocketIO
from pymongo import MongoClient

# My imports:
from user_functions import User

app = Flask(__name__)
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
"""

mongo_client = MongoClient("localhost")
DB = mongo_client["NewRome"]

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
    print(username)
    print(password)
    user.register(username, password, DB)
    return redirect("/")
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
        response = make_response(redirect("/"))
        response.set_cookie("auth_token", str(auth_token), max_age=3600, httponly=True)
        return response

@app.route("/auctions_create")
def render_auctions_create():
    response = make_response(render_template("auctions_create.html"), 200)
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response



# Host All Static Files
@app.route("/<path:file>")
def static_files(file):
    response = make_response(send_from_directory("static", file), 200)
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response

""" 
    --- Web Socket Connections Below ---
"""

@socketio.on("listing-create")
def connect(printStr):
    print(printStr)

socketio.run(app=app, host = "0.0.0.0", port = 8080, allow_unsafe_werkzeug=True)