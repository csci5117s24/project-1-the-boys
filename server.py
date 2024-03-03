

from flask import Flask, render_template, url_for, request, redirect
from jinja2 import Environment, Template
import os
from flask import Flask, render_template, redirect
from flask import current_app, g, request, url_for, session
from contextlib import contextmanager
import json
from urllib.parse import quote_plus, urlencode
from authlib.integrations.flask_client import OAuth
from contextlib import contextmanager
import logging
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import DictCursor
from stock_api import *
from database_stuff import *

app = Flask(__name__)
environment = Environment


app.secret_key = os.environ["FLASK_SECRET"]


oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=os.environ.get("AUTH0_CLIENT_ID"),
    client_secret=os.environ.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{os.environ.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + os.environ.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": os.environ.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )


@app.route("/", methods=['GET'])
def mainpage():
    url_for('static', filename = 'styling/style.css')
    gainers=top_gainers()
    splist=SPCSV()
    splist.pop(0)
    return render_template('mainpage.html', splist=splist) #This will be changed when the basic frame is created and then used as an extension for all of our pages



@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    print (session["user"])
    with get_db_cursor(True) as cur:
        query = ("select ID FROM users WHERE id= %s",(session["user"].get("userinfo").get("sub")))
        print("printing"+str(session["user"].get("sub")))
        cur.execute("select * FROM users WHERE ID = %s",(str(session["user"].get("userinfo").get("sub")),)) 
        returnval = cur.fetchall()
        if len(returnval) != 0:
            print("found users with query: " +"and userinfo of" + str(returnval[0][0]))  
            session["username"]=returnval[0][1]
            session["realname"]=returnval[0][2]
            session["avatar"]=returnval[0][3]
            return render_template("profile.html")
        else:
            print("found no users with query: ")
            cur.execute("INSERT INTO Users (ID, realname) VALUES (%s, %s)", (session["user"].get("userinfo").get("sub"),token.get("userinfo").get("given_name")))
            print("\n added\n")
            return render_template("login.html")
            

        



@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )



@app.route("/profile", methods=['GET'])
def profilepage():
    url_for('static', filename = 'styling/style.css')
    return render_template('profile.html',username=session["username"],realname=session["realname"]) #This will be changed when the basic frame is created and then used as an extension for all of our pages


        

@app.route("/submitUser", methods=['POST'])
def userCreate():
    createUser(request)
    return redirect("/profile")


@app.route("/signup", methods=['GET'])
def signup():
    return render_template("signup.html")











