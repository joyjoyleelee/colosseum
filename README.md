# colosseum
this is for our 312 project guys :)

## Tasks
### LO1
- [X] Set up the registration form
    - [X] Store username and salted, hashed password in database
- [X] Set up the login form
    - [X] Check if username and salted, hashed password exists in database

#### IF YES
- [X] Set authentication cookie
- [ ] Display username somewhere

#### IF NO
- [X] Error message (error page)

### LO2
- [ ] Create user post form (with title + description)
    - [ ] ESCAPE HTML IN USERNAME, TITLE, DESCRIPTION
    - [ ] Check if user is authenticated (auth token) and creator of post
    - IF YES
        - [ ] Make post in chat (with username, title + description)
        - [ ] Store post in database (with username, title + description)
    - IF NO
        - [ ] Don’t post (maybe error message?)
- [ ] Set up path to get chat history


### LO3
- [ ] Add like button to each post
    - [ ] Add likes to posts database
    - [ ] Check the database for the message and - increment the like count. 
    - [ ] Prevent user from liking the same post twice
- [ ] Remove like from post
    - [ ] Subtract like from posts database