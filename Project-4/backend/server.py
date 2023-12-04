from flask import Flask, render_template, make_response, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime #this is to keep track of the dates
import bcrypt
import html
import hashlib
from secrets import token_urlsafe


app = Flask(__name__) #setting this equal to the file name (web.py)
CORS(app, origins='http://localhost:3000/', supports_credentials=True)

#Establish the mongo database
#localhost for localhost mongo for docker
mongo_client = MongoClient('localhost')
db = mongo_client["colosseum"]
user_collection = db["users"]
auth_token_collection = db["auth_tokens"]
listings_collection = db["listings"]
email_token_collection = db["email_tokens"]

# Delete collection records. --- ALERT """ FOR TESTING ONLY MAKE SURE TO REMOVE
# chat_collection.delete_many({})
# user_collection.delete_many({})
# auth_token_collection.delete_many({})
# xsrf_token_collection.delete_many({})
# MAKE SURE YOU REMOVE THE LINES ABOVE.

#Splits up the cookie string into a useable cookie dictionary
def cookieSearch(self, request):
    cookies = request.headers.get("Cookie", "").replace("; ", ";").split(";") # -> [visits=0, auth_token=token]
    cookie_dic = {}
    for cookie in cookies:
        c = cookie.split("=")
        cookie_dic[c[0]] = c[1]
    return cookie_dic

#Set up the home page ----------------------------------------------------------------------------------------------------------------------------
@app.route("/") #index.html
def home():
    #index_html
    #app = Flask(__name__, template_folder='../../client/public')
    response = make_response(render_template("index.html"), 200)
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response

@app.route("/login") #index.html
def logPage():
    #index_html
    #app = Flask(__name__, template_folder='../../client/public')
    response = make_response(render_template("login.html"), 200)
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response

@app.route('/verify/<path:verification_code>')
def verify_email(verification_code):
    # Use verification_code variable here in your logic

    record = auth_token_collection.find_one({"token": verification_code})
    if record is not None:
        user_email = record['email']
        user_collection.find_one_and_update({"username": user_email}, {"$set": {"verified": True}})
        pass
        #return home page
    else:
        #return error message
        pass

    #return f"Verification Code: {verification_code}"

@app.route("/register") #index.html
def regPage():
    #index_html
    #app = Flask(__name__, template_folder='../../client/public')
    response = make_response(render_template("register.html"), 200)
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response

@app.route("/createListing") #index.html
def create_Listing():
    #index_html
    #app = Flask(__name__, template_folder='../../client/public')
    response = make_response(render_template("createListing.html"), 200)
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response

@app.route("/auction") #index.html
def auction():
    #index_html
    #app = Flask(__name__, template_folder='../../client/public')
    response = make_response(render_template("auction.html"), 200)
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response

@app.route("/auctionWon") #index.html
def auctionWon():
    #index_html
    #app = Flask(__name__, template_folder='../../client/public')
    response = make_response(render_template("auctionWon.html"), 200)
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response

@app.route("/myAuction") #index.html
def myAuction():
    #index_html
    #app = Flask(__name__, template_folder='../../client/public')
    response = make_response(render_template("myAuction.html"), 200)
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response

def check_auth(auth_tok, username):
    #auth_tok => string (from request)
    #username => string (from request)
    #collection_from_db => auth_token_collection (collection object)
    #good_or_nah = 0
    record = auth_token_collection.find_one({"auth_token": hashlib.sha256(auth_tok.encode()).hexdigest()}) #hexdigest turns the bytes to a string
    if record == None:
        return 0
    elif record['username'] == username:
        return 1
    else:
        return 0

#
@app.route("/check_auth")
def smd():
    data = request.json
    #not sure if auth_token can be accessed by data['auth_token'}{
    return check_auth(data['auth_token'], data['username'])



    #return good_or_nah


#Set up the registration form ---------------------------------------------------------------------------------------------------------------------
@app.route("/registerUser", methods =['POST'])

def process_register():

        data = request.json
        data['username'] = html.escape(data['username'])
        data['password'] = html.escape(data['password'])

        if user_collection.find_one({"username": data.get("username")}) is None:
            # Store username and salted, hashed password in database
            salt = bcrypt.gensalt()
            the_hash = bcrypt.hashpw(data.get("password").encode(), salt)#df
            user_collection.insert_one({"username": data.get("username"), "password": the_hash, "verfied": False})

            # Possibly create new response headers before returning response
            # response = make_response(render_template("index.html"), 200)
            # response.headers["X-Content-Type-Options"] = "nosniff"
            return jsonify({"message": "User successfully added", "code": 1})
        # If the user already exists, give an error
        else:
            return jsonify({"message": "Username already exists", "code": 0})



#Set up the login form-----------------------------------------------------------------------------------------------------------------------------
@app.route("/loginUser", methods =['POST'])
def login():
    print('marco')
    # print(request.get_data()) # -> b'username_login=hi&password_login=here'
    # DB represents database
    print(request)
    data = request.json
    data['username'] = html.escape(data['username'])
    data['password'] = html.escape(data['password'])
    print(data)
    islogin = 0
    user_database = user_collection.find_one({"username": data['username']})
    if (user_database == None):
        # Make response - NO USERS EXIST YET -> NOT GOOD

        response = make_response('0', 404)
        response.headers["X-Content-Type-Options"] = "nosniff"
    else:
        # Access the password associated with the username
        database_password = user_database.get("password", b'none')
        print(database_password)
        # Access the password associated with what the user gave us
        input_password = data['password'].encode()
        print(input_password)
        # If the user does not exist in the database, then database_password = b"none"
        if (database_password == b'none'):
            # Make response if USER DOES NOT EXIST
            response = make_response('0', 404)
            response.headers["X-Content-Type-Options"] = "nosniff"
        # Compare if the passwords are the same - returns True or False
        elif (bcrypt.checkpw(input_password, database_password)):
            auth_token = token_urlsafe(13)  # creates unique token, the 13 is the entropy

            # Make response if PASSWORDS MATCH
            #response = make_response(render_template("index.html"), 200)
            response = make_response('1',200)

            response.headers["X-Content-Type-Options"] = "nosniff"

            # Set the authentication cookie and add to auth_token database named "auth_tokens"
            auth_token_hashed = hashlib.sha256(auth_token.encode('utf-8')).digest()
            response.set_cookie("auth_token", str(auth_token), max_age=3600, httponly=True)
            response.set_cookie("cookie_name", data['username'])
            auth_token_collection.insert_one(
                {"username": data['username'], "auth_token": auth_token_hashed})
            islogin =1
            return response

        else:
            # Make response if PASSWORDS DO NOT MATCH
            #response = make_response(render_template("index.html"), 404)
            response = make_response(0, 404)
            response.headers["X-Content-Type-Options"] = "nosniff"
            return response
    #response.headers['thierry'] = islogin

    print(response)
    return response

#Helper function for create listing
def createImage(data, photo_data, content_length, content_type, auth_token):
    if(auth_token != None):
        received_data = b''
        #If the length is less than 2048, we can read it in one go
        if content_length <= 2048:
                received_data = photo_data.body
        #Otherwise we receive the data in chunks
        else:
            received_data = photo_data.body
            been_read = len(photo_data.body)
            while been_read < content_length:
                received_data += photo_data.recv(content_length - len(photo_data.body))
                been_read += (content_length - len(photo_data.body))
        print(f'data received: {received_data}')
        boundary = content_type.split("boundary=")[1]
        print(f'BOUNDARY: {boundary}')
        split_data = received_data.split(boundary.encode())
        user_data = auth_token_collection.find_one({"auth_token": hashlib.sha256(auth_token.encode()).hexdigest()}) #hexdigest turns the bytes to a string
        current_user = user_data["_id"]
        print(f'current user: {current_user}')

        #If the user exists, parse the image data and add to user database
        if(user_data != None):
            filename = "/market/backend/image/" + str(current_user) + ".jpg" #im lazy and using the username ID as filename
            with open("." + filename, 'wb') as newFile: #write to the end of a new file IN BYTES
                #Get the image bytes from each part
                for eachPart in split_data:
                    print(f'eachPart: {eachPart}')
                    if (b'\r\n\r\n' in eachPart):
                        headers = eachPart.split("\r\n\r\n".encode())[0]
                        print(f'headers: {headers}')
                        if b"Content-Disposition: form-data" in headers:
                            print("WE MADE IT")
                            image_bytes = eachPart.split("\r\n\r\n".encode())[1]
                            data = image_bytes.replace(b'\r\n', b"").replace(b"--", b"")
                            #Save this image as a file on your server
                            newFile.write(data)
                    else:
                        data = eachPart.replace(b'\r\n', b"").replace(b"--", b"")
                        newFile.write(data)

            #Store the filename of this image in your database as part of this user's profile
            user_collection.find_one_and_update({"username": user_data["username"]}, {"$set":{"filename": filename}})

#Create the listings-----------------------------------------------------------------------------------------------------------------------------
@app.route("/create-listing", methods =['POST'])
def createListing():
    # WHAT I NEED IN THE DATA: ********************************************************************************
    # ID, Item name, Item description, End date, Price
    print(f'request headers cookie: {request.headers.get("Cookies")}')
    data = request.json
    print(f'data: {data}')
    cookie_dict = cookieSearch(request)
    auth_token = cookie_dict.get("auth_token")
    print(f'auth token: {auth_token}')
    #If user is authenticated
    user_data = auth_token_collection.find_one({"auth_token": hashlib.sha256(auth_token.encode()).hexdigest()}) #hexdigest turns the bytes to a string
    if(user_data != None):
        check_auth(auth_token, data['username'])
        if(user_data != None):
            current_user = user_data["_id"]
            print(f'current user: {current_user}')
            #NOTE: gonna need to reformat date in order to compare -> WEBSOCKETS
            listing = {"Item name": data.get("item_name"),
                        "Item description": data.get("item_description"),
                        "Start date": str(datetime.now()),
                        "End date": data.get("end_date"),
                        "Price": data.get("price"),
                        "Current user bidding": None,
                        "User who posted listing": current_user,
                        }
            print("user is authenticated woo")
            addPhoto(listing, data, auth_token)
            listings_collection.insert_one(listing)
            return jsonify(listing)

#Create the photo-----------------------------------------------------------------------------------------------------------------------------
@app.route("/add-photo", methods =['POST'])
def addPhoto(listing, data, auth_token):
    content_length = data.headers.get("content_length")
    content_type = data.headers.get("content_type")
    #If a photo was uploaded AND user is authenticated -> create listing
    user_data = auth_token_collection.find_one({"auth_token": hashlib.sha256(auth_token.encode()).hexdigest()}) #hexdigest turns the bytes to a string
    if(user_data != None):
        if(request.body != b''):
            photo = createImage(data, request.body, content_length, content_type, auth_token)
            listing["Photo"] = photo
        else:
            return jsonify({"message": "No image uploaded"})

#Helper function for the 3 auction pages - returns ALL listings
def totalListings():
    # Function returns a list of all listings
    ret_list = []
    all_posts = listings_collection.find({})
    for p in all_posts:
        #Escape HTML in the posts
        p["item_name"] = html.escape(p["item_name"])
        p["item_description"] = html.escape(p["item_description"])
        p["current_user_bidding"] = html.escape(p["current_user_bidding"])
        p["user_posted"] = html.escape(p["user_posted"])
        ret_list.append(jsonify(p))
    return ret_list

#Helper function for the 3 auction pages - determines whether an auction has ended or not
#TRUE - if auction has ended, F ALSE - if auction is ongoing
def auctionEnded(end_date):
    #Auction date in the format: YYYY/MM/DD/HR/MN
    end_list = end_date.split("/") #[year, month, day, hour, minute]
    #Current date using datetime imports
    now = str(datetime.now()).split(" ") #['2023-11-11', '18:37:21.560362']
    current_date = now[0].split('-') # ['2023', '11', '11']
    current_time = now[1].split(':') # ['18', '38', '33.673144']

    #Compare current year with auction year
    if current_date[0] < end_list[0]:
        return False
    elif current_date[0] == end_list[0]:
        #Compare current month with auction month
        if current_date[1] < end_list[1]:
            return False
        elif current_date[1] == end_list[1]:
            #Compare current day with auction day
            if current_date[2] < end_list[2]:
                return False
            elif current_date[2] == end_list[2]:
                #Compare current hour with auction hour
                if current_time[0] < end_list[3]:
                    return False
                elif current_time[0] == end_list[3]:
                    #Compare current min with auction min
                    if current_time[1] < end_list[4]:
                        return False
                    else:
                        return True
                else:
                    return True
            else:
                return True
        else:
            return True
    else:
        return True
#Set up the 3 listing pages-----------------------------------------------------------------------------------------------------------------------------
#SEND BACK A LIST OF JSON DICTS - EACH DICT IS A LISTING
@app.route("/winnings", methods =['GET'])
#find user through auth cookie
def postWinnings():
    # WHAT I NEED IN THE DATA: **********************
    #{"headers": {all the headers}}
    data = request.json
    auth_token = data.get("auth_token")
    user_data = auth_token_collection.find_one({"auth_token": hashlib.sha256(auth_token.encode()).hexdigest()}) #hexdigest turns the bytes to a string
    #If the user is authenticated, then find all their won auctions
    if (user_data != None):
        current_user = user_data["_id"]
        actually_won = []
        maybe_won = listings_collection.find({"Current user bidding": current_user})
        for listing in maybe_won:
            #If the auction has ended, then added to user's auctions won list
            if auctionEnded(listing.get("end_date")):
                actually_won.append(listing)
        return jsonify({"message": "Won auctions found", "auctions": actually_won})
    else:
        return jsonify({"message": "No auctions found"})

@app.route("/postedAuctions", methods =['GET'])
#find user through auth cookie
def userPostedAuctions():
    # WHAT I NEED IN THE DATA: **********************
    #{"headers": {all the headers}}
    data = request.json
    auth_token = data.get("auth_token")
    user_data = auth_token_collection.find_one({"auth_token": hashlib.sha256(auth_token.encode()).hexdigest()}) #hexdigest turns the bytes to a string
    #If user is authenticated, then find all the auctions they posted
    if (user_data != None):
        current_user = user_data["_id"]
        user_posted = listings_collection.find({"User who posted listing": current_user})
        return jsonify({"message": "Posted auctions found", "auctions": user_posted})
    else:
        return jsonify({"message": "No auctions found"})


@app.route("/auctions", methods =['GET'])
#start with sending ALL auctions - might need to change to just the ones still running later
def totalAuctions():
    allposts = totalListings()
    return jsonify({"message": "All auctions found", "auctions": allposts}) #should be a list of JSON dicts






app.run(host = "0.0.0.0", port = 8080)
