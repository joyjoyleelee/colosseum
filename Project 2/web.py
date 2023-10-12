from flask import Flask, render_template, make_response, url_for, request, send_from_directory

app = Flask(__name__) #setting this equal to the file name (web.py)

@app.route("/") #index.html
def home():
    response = make_response(render_template("index.html"), 200)
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response

@app.route("/next") #next.html
def next():
    response = make_response(render_template("next.html"), 200)
    response.headers["X-Content-Type-Options"] = "nosniff"
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


app.run(host = "0.0.0.0", port = 8080)

<<<<<<< HEAD
"""If you were able to clone the project, make a comment here with your name and COMMIT"""
#Joy was here :)
=======

""" MARCO ADDED THESE COMMENTS FOR TESTING
LET'S SEE IF IT WORKS
"""

"""
rizzlordswang57
iyanu was here l
"""

"""Joy's branch"""
>>>>>>> 79c1c0caac3309a76f661ce1a00992dc383ce2cb
#hello world
