# colosseum
this is for our 312 project guys :)

## Tasks
### LO1
- [X] Set up the registration form
    - [X] Store username and salted, hashed password in database
- [X] Set up the login form
    - [X] Check if username and salted, hashed password exists in database
    - IF YES
        - [X] Set authentication cookie
        - [X] Display username somewhere

    - IF NO
        - [X] Error message (error page)

### LO2
- [X] Create user post form (with title + description)
    - [X] ESCAPE HTML IN USERNAME, TITLE, DESCRIPTION
    - [X] Check if user is authenticated (auth token) and creator of post
    - IF YES
        - [X] Make post in chat (with username, title + description)
        - [X] Store post in database (with username, title + description)
    - IF NO
        - [X] Don’t post (maybe error message?)
- [X] Set up path to get chat history


### LO3
- [X] Add like button to each post
    - [X] Add likes to posts database
    - [X] Check the database for the message and - increment the like count. 
    - [X] Prevent user from liking the same post twice
- [X] Remove like from post
    - [X] Subtract like from posts database
