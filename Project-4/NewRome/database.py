import hashlib
import uuid
import html

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

    def update_bid(self, username, DB, id_list,bid_num):
        listings = DB["COLLECTION_LISTINGS"]
        # add the user to the dictionary
        listings.update_one({"_id" :  id_list}, {"$set": {f"bidders.{username}": bid_num }})
        dict = listings.find_one({"_id" :  id_list}).get("bidders")
        bidn =  listings.find_one({"_id" :  id_list}).get("bid")
        #maxbid = max(dict.values())
        print(bidn)
        print(bid_num)
        if bidn < bid_num:
            print("im higher")
            maxbid = bid_num
            listings.update_one({"_id": id_list}, {"$set": {"bid": maxbid}})
    def valid_bid(self,bid_num):
         return bid_num.isnumeric()





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