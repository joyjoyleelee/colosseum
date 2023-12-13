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
        ret = False
        COLLECTION_USERS = DB["COLLECTION_USERS"]
        test = COLLECTION_USERS.find_one({"auth_token":auth_token})
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

    # 5
    def bid_isNumber(self, bid_value, DB):
        """ This function takes in the current user bid value. It checks whether the user input bid value is allowed.
            It returns False if the entered bid is not a valid input i.e. not a number.
            It returns True if the entered bid is allowed.
        """
        COLLECTION_LISTINGS = DB["COLLECTION_LISTINGS"]

    # 6
    def bid_isBelow(self, bid_value, DB):
        """ This function takes in the user input bid value. It checks weather it's below
            It retunrs False if the entered is under.
            It returns True if the entered bid is correct.
        """

    # 2
    def listing_hasImage(self, img, DB):
        """ This function takes in the image currently stored in the HTML. It checks whether the user has entered an image.
            It returns False if the user has not entered an image.
            It returns True if the user has entered a valid image.
            This is important because the create listing functionality requires that an image be uploaded FIRST
            and submitted before submitting a listing. This function allows us to enforce that and prevent listing creation
        """
        COLLECTION_LISTINGS = DB["COLLECTION_LISTINGS"]

    # 4
    def listing_isImage(self, img, DB):
        """ This function takes in the image currently stored in the HTML. It checks whether the user has entered an image.
            It returns False is the uploaded file is not an image.
            It returns True if the image is within the correct format.
        """
        COLLECTION_LISTINGS = DB["COLLECTION_LISTINGS"]

    # 7
    def incorrect_login(self, username, password, DB):
        """ This function takes in the username and password entered. It checks whether the username OR
            password entered is correct.
            It returns False if either password OR username are incorrect.
            It returns True if BOTH username and password are correct.
        """
        COLLECTION_USERS = DB["COLLECTION_USERS"]