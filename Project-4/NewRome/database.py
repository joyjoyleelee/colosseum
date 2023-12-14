import hashlib
import uuid
import html
import time

"""
    Database File
    This file stores a class which handles all database related functionality e.g.:
    - Registered User
    - Login User
    - Authenticate User

"""

""" --------------------------------- Database Format -----------------------------------------
    DB["COLLECTION_USERS"] - Stores Emails -- {username: '', password: ''}
    DB["COLLECTION_TOKENS"] - Stores Any Tokens -- {username: '', auth_token: ''}
    DB["COLLECTION_EMAILS"] - Stores Emails -- {username: '', password: '', email: ''}
    DB["COLLECTION_LISTINGS] - Stores All Listings -- format is a dictionary marked below
    {creator: '', creator_token: '', title: '', desc: '', time: '', open: bool, bidders: {}, winner: '', bid: int, 
    _id: '', img: '/path/image.format'}
    ---------------------------------  ---------------- -----------------------------------------
"""

class Database:

    def escape_HTML_listing(self, listing):
        """ This function takes a listing and replaces it with the HTML escaped version.
        {creator: '', creator_token: '', title: '', desc: '', time: '',
        open: bool, bidders: [{}], winner: '', bid: int}
        """
        listing['creator'] = html.escape(listing['creator'])
        listing['creator_token'] = html.escape(listing['creator_token'])
        listing['title'] = html.escape(listing['title'])
        listing['desc'] = html.escape(listing['desc'])
        listing['time'] = html.escape(listing['time'])
        listing['winner'] = html.escape(listing['winner'])
        listing['bid'] = html.escape(listing['bid'])
        return listing

    def add_new_listing(self, username, auth_token, listing_json, DB):
        """ This function takes in variables to create one specific listing and adds it to the database"""
        title = listing_json.get("title")
        desc = listing_json.get("desc")
        bid = listing_json.get("bid")
        time = listing_json.get("time")
        id = str(uuid.uuid4())
        # Process the image to store it in the right format. The image contacts http://localhost:8080/ <- remove it
        img = listing_json.get("img")
        img = img.split("/static/")[1]
        # Create new listing dictionary and add to the database
        COLLECTION_LISTINGS = DB["COLLECTION_LISTINGS"]
        new_listing = {'creator': username, 'creator_token': auth_token, 'title': title,
                       'desc': desc, 'time': time, 'open': True, 'bidders': {},
                       'winner': '', 'bid': bid, '_id': id, 'img': img}
        COLLECTION_LISTINGS.insert_one(new_listing)
        self.track_timer(id, DB) # Begin timer for it
        print(f'Database.add_new_listing(self, username, auth_token, listing_json, DB): \n{new_listing}')

    def update_listing(self):
        """ This function takes in variables to update one specific listing and adds it to the database
            variables: bid = #, bidder = ''
        """
        pass

    def retrieve_all_listings(self, DB):
        """ This function reads through the database. It returns a JSON string (A list of Dictionaries
            Each dictionary represents one individual listing. Listing Format
            {creator: '', creator_token: '', title: '', desc: '', time: '', open: bool, bidders: [{}],
            winner: '', bid: int, _id: '', img: '/path/image.format'}
        """
        all_listings = []
        COLLECTION_LISTINGS = DB["COLLECTION_LISTINGS"]
        DB_objs = COLLECTION_LISTINGS.find({})
        for listing in DB_objs:
            new_listing = self.escape_HTML_listing(listing)
            all_listings.append(new_listing)
        return all_listings

    def retrieve_open_listings(self, DB):
        """ This function mimicks retrieve all listings, but it only returns open ones"""
        all_listings = []
        COLLECTION_LISTINGS = DB["COLLECTION_LISTINGS"]
        DB_objs = COLLECTION_LISTINGS.find({'open': True})
        for listing in DB_objs:
            new_listing = self.escape_HTML_listing(listing)
            all_listings.append(new_listing)
        return all_listings

    def retrieve_won_listings(self, winner_name, DB):
        """ This function retrieve all listings won by user. Returns a list of json strings"""
        all_listings = []
        COLLECTION_LISTINGS = DB["COLLECTION_LISTINGS"]
        all_listings = []
        COLLECTION_LISTINGS = DB["COLLECTION_LISTINGS"]
        DB_objs = COLLECTION_LISTINGS.find({'winner': winner_name})
        for listing in DB_objs:
            new_listing = self.escape_HTML_listing(listing)
            all_listings.append(new_listing)
        return all_listings

    def retrieve_user_listings(self, username, DB):
        """ This function retrieve all listings created by the user. Returns a list of json strings"""
        all_listings = []
        COLLECTION_LISTINGS = DB["COLLECTION_LISTINGS"]
        all_listings = []
        COLLECTION_LISTINGS = DB["COLLECTION_LISTINGS"]
        DB_objs = COLLECTION_LISTINGS.find({'creator': username})
        for listing in DB_objs:
            new_listing = self.escape_HTML_listing(listing)
            all_listings.append(new_listing)
        return all_listings

    def get_username(self, auth_token, DB):
        # This function takes in a user token and returns the username from the database
        if auth_token == "":
            return "Guest"
        COLLECTION_TOKENS = DB["COLLECTION_TOKENS"]
        auth_token_h = hashlib.sha256(auth_token.encode()).digest()
        DB_obj = COLLECTION_TOKENS.find_one({'auth_token': auth_token_h})
        username = DB_obj.get("username", "Guest")
        return username

    def update_bid(self, username, DB, id_list, bid_num):
        listings = DB["COLLECTION_LISTINGS"]
        filter = {"_id": id_list}
        new_bid = int(bid_num)
        DB_obj = listings.find_one(filter)
        curr_bid = int(DB_obj.get("bid"))
        # add the user to the dictionary
        listings.update_one(filter, {"$set": {f"bidders.{username}": bid_num}})
        if new_bid > curr_bid:
            listings.update_one({"_id": id_list}, {"$set": {"bid": str(new_bid)}})

    def get_bid(self, id, DB):
        COLLECTION_LISTINGS = DB["COLLECTION_LISTINGS"]
        DB_obj = COLLECTION_LISTINGS.find_one({"_id": id})
        curr_bid = DB_obj.get("bid")  # Time left in seconds
        return curr_bid

    def get_time(self, list_id, DB):
        COLLECTION_LISTINGS = DB["COLLECTION_LISTINGS"]
        DB_obj = COLLECTION_LISTINGS.find_one({"_id": list_id})
        curr_time = DB_obj.get("time")  # Time left in seconds
        return curr_time

    def track_timer(self, listing_id, DB):
        """ This function sets the timer for each specific listing"""
        COLLECTION_LISTINGS = DB["COLLECTION_LISTINGS"]
        filter = {"_id": listing_id}
        DB_obj = COLLECTION_LISTINGS.find_one({"_id": listing_id})
        new_time = int(DB_obj.get("time"))
        while int(new_time) > 0:
            new_time -= 1
            COLLECTION_LISTINGS.update_one(filter, {"$set": {"time": str(new_time)}})
            time.sleep(1)
        # Update winner, etc
            if int(new_time) == 0:
                print(True)
                bidders = DB_obj.get("bidders")
                w = "" # Winner
                n = 0 # Highest bid
                for b in bidders:
                    val = bidders[b]
                    if val > n:
                        n = val
                        w = b
                COLLECTION_LISTINGS.update_one(filter, {"$set": {"time": str(0)}})
                COLLECTION_LISTINGS.update_one(filter, {"$set": {"winner": w}})
                COLLECTION_LISTINGS.update_one(filter, {"$set": {"open": False}})







    # def update_listing
    # def update(self, id, DB):
    #     """ This function updates every timer in the database for all listings."""
    #     COLLECTION_LISTINGS = DB["COLLECTION_LISTINGS"]
    #     DB_objs = COLLECTION_LISTINGS.find({})
    #     for objs in DB_objs:
    #         # For every listing in the database
    #         status = objs.get("open")
    #         t = objs.get("time")
    #         bidders = objs.get("bidders") # Dictionary of bidders
    #         winner = objs.get("winner") #
    #         # Update time
    #         t -= 0
    #
    #         # Update the listing in the Database
    #
    #     return

    # def update_timer(self, bid_id, DB):
    #     COLLECTION_LISTINGS = DB["COLLECTION_LISTINGS"]
    #     while True:
    #         DB_obj = COLLECTION_LISTINGS.find_one({"_id": bid_id})
    #         curr_time = DB_obj.get("time")  # Time left in seconds
    #         curr_status = DB_obj.get("open")  # True or False
    #         new_time = curr_time-1
    #         myquery = {"_id": bid_id} #
    #         newvalues = {"$set": {"time": new_time}}
    #         COLLECTION_LISTINGS.update_one(myquery, newvalues)
    #         if curr_time == 0:
    #             openvalue = {"$set": {"open": False}}
    #             COLLECTION_LISTINGS.update_one(myquery, openvalue) # listing is now closed
    #             break
    #         time.sleep(1)

    # {creator: '', creator_token: '', title: '', desc: '', time: '', open: bool, bidders: {}, winner: '', bid: int,
    #  _id: '', img: '/path/image.format'}



    def xxx(self, DB):
        # Resets The Entire Databases. Only for testing
        u = DB["COLLECTION_USERS"]
        t = DB["COLLECTION_TOKENS"]
        e = DB["COLLECTION_EMAILS"]
        l = DB["COLLECTION_LISTINGS"]
        u.delete_many({})
        t.delete_many({})
        e.delete_many({})
        l.delete_many({})