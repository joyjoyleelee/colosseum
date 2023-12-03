import hashlib
from secrets import token_urlsafe

import bcrypt
"""
    This file contains methods related to the user
    - Register
    - Login
    - Authenticate
"""

class User:
    # def __int__(self, username, passcode):
    #     self.username = username
    #     self.passcode = passcode
    def register(self, username, passcode, DB):
        salt = bcrypt.gensalt(12)
        passcode_hashed = bcrypt.hashpw(passcode.encode(), salt)
        COLLECTION_USER = DB["COLLECTION_USERS"]
        COLLECTION_USER.insert_one({"username": username, "password": passcode_hashed})

    def login(self, username_in, passcode_in, DB):
        authToken = ""
        # Logs in user and returns authToken
        # Function returns authToken otherwise it could not log in user
        COLLECTION_USER = DB["COLLECTION_USERS"]
        COLLECTION_TOKEN = DB["COLLECTION_TOKENS"]
        DB_Item = COLLECTION_USER.find_one({"username": username_in})
        # Verify user
        if (DB_Item != None):
            password = DB_Item.get("password", "")
            # Verify password
            if (bcrypt.checkpw(passcode_in.encode(), password)):
                authToken = token_urlsafe(12) #creates unique token
                authToken_hashed = hashlib.sha256(authToken.encode()).digest()
                COLLECTION_TOKEN.insert_one({"username": username_in, "authToken": authToken_hashed})
        return authToken

    def authenticate(self, userToken):
        # Authenticates user via token
        pass

