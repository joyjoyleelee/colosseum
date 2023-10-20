from flask import Flask, render_template, make_response, url_for, request, send_from_directory, redirect
from pymongo import MongoClient
from secrets import token_urlsafe
import bcrypt

app = Flask(__name__) #setting this equal to the file name (web.py)

#Establish the mongo database
mongo_client = MongoClient('localhost')
db = mongo_client["colosseum"]
chat_collection = db["chat"]
user_collection = db["users"]
auth_token_collection = db["auth_tokens"]
xsrf_token_collection = db["xsrf"]

#Set up the home page ----------------------------------------------------------------------------------------------------------------------------
@app.route("/") #index.html
def home():
    response = make_response(render_template("index.html"), 200)
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response

@app.route("/next") #next.html
def next():
    response = make_response(render_template("next.html"), 200)
    response.headers["X-Content-Type-Options"] = "nosniff"
    print(request)
    return response

#Set up the visit counter page ----------------------------------------------------------------------------------------------------------------------------
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

#Set up the registration form ---------------------------------------------------------------------------------------------------------------------
@app.route("/register", methods =['GET', 'POST'])
def register():
    #print(request.form.get('username_reg')) # -> gets the username input
    #print(request.get_data()) # -> b'username_reg=hi&password_reg=here'
    if (request.method == 'POST'):
        #Check if the user does not exist yet -> valid
        if (user_collection.find_one({"username": request.form['username_reg']}) == None):
            #Store username and salted, hashed password in database
            #print("this is a test")
            print(request)
            salt = bcrypt.gensalt()
            the_hash = bcrypt.hashpw(request.form['password_reg'].encode(), salt)
            user_collection.insert_one({"username": request.form['username_reg'], "password": the_hash})

            #Make response - USER DOES NOT EXIST -> GOOD
            response = make_response(render_template("index.html"), 200)
            response.headers["X-Content-Type-Options"] = "nosniff"
        #If the user already exists, give an error
        else:
            #Make response - USER ALREADY EXISTS -> NOT GOOD
            response = make_response("User already exists", 404)
            response.headers["X-Content-Type-Options"] = "nosniff"
        return response

#Set up the login form-----------------------------------------------------------------------------------------------------------------------------
@app.route("/login", methods =['GET', 'POST'])
def login():
    #print(request.get_data()) # -> b'username_login=hi&password_login=here'
    #DB represents database
    user_database = user_collection.find_one({"username": request.form['username_login']})
    if(user_database == None):
        #Make response - NO USERS EXIST YET -> NOT GOOD
        response = make_response("Nothing in database", 404)
        response.headers["X-Content-Type-Options"] = "nosniff"
    else:
        #Access the password associated with the username
        database_password = user_database.get("password", b'none')
        print(database_password)
        #Access the password associated with what the user gave us
        input_password = request.form['password_login'].encode()
        print(input_password)
        #If the user does not exist in the database, then database_password = b"none"
        if (database_password == b'none'):
            #Make response if USER DOES NOT EXIST
            response = make_response("User does not exist", 404)
            response.headers["X-Content-Type-Options"] = "nosniff"
        #Compare if the passwords are the same - returns True or False
        elif (bcrypt.checkpw(input_password, database_password)):
            auth_token = token_urlsafe(13) #creates unique token, the 13 is the entropy

            #Make response if PASSWORDS MATCH
            response = make_response(render_template("index.html"), 200)
            response.headers["X-Content-Type-Options"] = "nosniff"

            #Set the authentication cookie and add to auth_token database named "auth_tokens"
            response.set_cookie("auth_token", str(auth_token), max_age= 7200)
            auth_token_collection.insert_one({"username": request.form['username_login'], "auth_token": str(auth_token)})

        else:
            #Make response if PASSWORDS DO NOT MATCH
            response = make_response(render_template("index.html"), 404)
            response.headers["X-Content-Type-Options"] = "nosniff"
    return response

app.run(host = "0.0.0.0", port = 8000)


""" MARCO ADDED THESE COMMENTS FOR TESTING
LET'S SEE IF IT WORKS
"""

"""Joy's branch"""