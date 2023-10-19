from flask import Flask, render_template, make_response, url_for, request, send_from_directory,bcrypt,redirect
from pymongo import MongoClient
from secrets import token_urlsafe


app = Flask(__name__) #setting this equal to the file name (web.py)
mongo_client = MongoClient("mongodb://mongo:27017")
db = mongo_client["cse312"]
chat_collection = db["chat"]
users_collection = db['users']


@app.route("/") #index.html
def home():
    response = make_response(render_template("index.html"), 200)
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response

@app.route("/next") #next.html
def next():
    response = make_response(render_template("next.html"), 200)
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response

@app.route("/visit-counter") #visit-counter.html
def cookie():
    #Get the cookie value from the request
    cookie_value = int(request.cookies.get("visits", 0))
    cookie_value+=1

    #Create the response
    response = make_response(render_template("visit-counter.html", value = cookie_value), 200) #you can create variables (like value) and use in HTML!
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.set_cookie("visits", str(cookie_value), max_age= 7200)
    return response

@app.route("/<path:file>")
def pathRoute(file):
    response = make_response(send_from_directory("static", file), 200)
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response

@app.route("/registration",methods =['POST'])
def register():
    #Store username and salted, hashed password in database
    salt = bcrypt.gensalt()
    the_hash = bcrypt.hashpw(request.form('password').encode(), salt)
    users_collection.insert_one({"username": request.form['username'], "password": the_hash})
    return redirect(url_for('/'))

@app.route("/login",methods =['POST'])
def login():
    #DB represents database
    DB = users_collection.find_one({"username": request.form['username']})
    # access the password associated with the username
    Pw = DB.get("password", b"none")
    # access the password associated with what the user gave us
    passw = request.form('password').encode()
    # compare if the passwords are the same
    if bcrypt.checkpw(passw, Pw):
        n

app.run(host = "0.0.0.0", port = 8080)

<<<<<<< HEAD
"""If you were able to clone the project, make a comment here with your name and COMMIT"""
#Joy was here :)
=======

""" MARCO ADDED THESE COMMENTS FOR TESTING
LET'S SEE IF IT WORKS
"""

"""
rizzlordswang57
i hate it. Iyanu k
"""

"""Joy's branch"""
>>>>>>> 79c1c0caac3309a76f661ce1a00992dc383ce2cb
#hello world
