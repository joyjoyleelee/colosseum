import hashlib
from datetime import datetime

"""
We need a "validator" CLASS, that takes care of all sorts of validation we need to pay attention to?
"Validate" meaning by that, we need to prevent users from entering inputs that will corrupt the server.
E.g. Someone sends in character bid instead of an int. Or they do not upload an image first before creating a listing.
THESE WILL BE USED FOR ERROR MESSAGES DISPLAY AND TO SAFEGUARD OUR CORE FUNCTIONALITY.
This Validator object needs the following functions to return a bool:
"""
class Auth:
    def user_isAuthorized(self, auth_token, DB):
        """ This function takes in the current user auth token as an input. Checks whether the user is logged in.
            It returns False if the user cannot be authenticated. e.g. No auth token or not a recognized user.
            It returns True if the user is authenticated.
        """
        if auth_token == "":
            return False
        else:
            COLLECTION_TOKENS = DB["COLLECTION_TOKENS"]
            auth_token_h = hashlib.sha256(auth_token.encode()).digest()
            ret = False
            test = COLLECTION_TOKENS.find_one({"auth_token": auth_token_h})
            if test != None:
                ret = True
            return ret

    # 3
    def listing_isOpen(self, listing_json, DB):
        """ This function verifies that the listing is available to be bid on.
            It returns False is the listing is already closed i.e. no longer accepting entries.
            It returns True if the bid is open.
        """
        COLLECTION_LISTINGS = DB["COLLECTION_LISTINGS"]
        listing = COLLECTION_LISTINGS.find_one({"_id", listing_json[id]})
        if listing != None:
            #TODO: Change time based on what the time key actually is, assumes we are using the native javascript time string
            js_time = datetime.strptime(listing["time"], "%a %b %d %Y %H:%M:%S GMT%z")
            current_time = datetime.utcnow()
            if current_time>=js_time:
                return True
            else:
                print("auction is past done")
                return False
        else:
            print("listing DNE")
            return False

    # 5
    def bid_isNumber(self, bid_value):
        """ This function takes in the current user bid value. It checks whether the user input bid value is allowed.
            It returns False if the entered bid is not a valid input i.e. not a number.
            It returns True if the entered bid is allowed.
        """
        if str(bid_value).isalpha():
            return False
        return True


    # 6
    #TODO: Make sure id is the listing id
    def bid_isBelow(self, bid_value, id, DB):
        """ This function takes in the user input bid value. It checks weather it's below
            It retunrs False if the entered is under.
            It returns True if the entered bid is correct.
        """
        COLLECTION_LISTINGS = DB["COLLECTION_LISTINGS"]
        listing = COLLECTION_LISTINGS.find_one({"_id", id})
        #TODO: Make sure that "bid" is the correct key in the DB
        price = listing["bid"]
        if price >= bid_value:
            return False
        else:
            return True

    # 2
    def listing_hasImage(self, img: str):
        """ This function takes in the image currently stored in the HTML. It checks whether the user has entered an image.
            It returns False if the user has not entered an image.
            It returns True if the user has entered a valid image.
            This is important because the create listing functionality requires that an image be uploaded FIRST
            and submitted before submitting a listing. This function allows us to enforce that and prevent listing creation
        """
        if img.__contains__("client_images/default.png") or img == "":
            return False
        else:
            return True

    # 4
    def listing_isImage(self, img):
        """ This function takes in the image currently stored in the HTML. It checks whether the user has entered an image.
            It returns False is the uploaded file is not an image.
            It returns True if the image is within the correct format.
        """
        return img[-3:] == "png" or img[-3:] == "jpg" or img[-3:] == "gif" or img[-4:] == "jpeg" or img[-4:] == "jfif"


    # 7
    def incorrect_login(self, username, password, DB):
        """ This function takes in the username and password entered. It checks whether the username OR
            password entered is correct.
            It returns False if either password OR username are incorrect.
            It returns True if BOTH username and password are correct.
        """
        COLLECTION_USERS = DB["COLLECTION_USERS"]
        user_info = COLLECTION_USERS.find_one({"username",username})
        if user_info == None:
            print("Username does not exist in DB")
            return False
        elif user_info["password"] == password:
            return True
        else:
            print("incorrect password")
            return False