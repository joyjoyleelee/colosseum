from flask import Flask, render_template, make_response, url_for, request, send_from_directory
from pymongo import MongoClient
import bcrypt

app = Flask(__name__) #setting this equal to the file name (web.py)

#Establish the mongo database
mongo_client = MongoClient('mongo_host')
db = mongo_client["colosseum"]
chat_collection = db["chat"]
user_collection = db["users"]
auth_token_collection = db["tokens"]
xsrf_token_collection = db["xsrf"]

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


app.run(host = "0.0.0.0", port = 8000)


""" MARCO ADDED THESE COMMENTS FOR TESTING
LET'S SEE IF IT WORKS
"""

"""Joy's branch"""