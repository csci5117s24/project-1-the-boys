







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

app = Flask(__name__)
environment = Environment

pool = None


app = Flask(__name__)
environment = Environment
app.secret_key = os.environ["FLASK_SECRET"]




@app.route("/", methods=['GET'])
def mainpage():
    url_for('static', filename = 'styling/style.css')
    splist=SPCSV()
    splist.pop(0)
    return render_template('frame.html', splist=splist) #This will be changed when the basic frame is created and then used as an extension for all of our pages



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

@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    print (session["user"])
    with get_db_cursor(True) as cur:
        query = ("select ID FROM users WHERE id= %s",(session["user"].get("userinfo").get("sub")))
        print("printing"+str(session["user"].get("sub")))
        cur.execute("select ID FROM users WHERE ID = %s",(str(session["user"].get("userinfo").get("sub")),)) 
        returnval = cur.fetchall()
        if len(returnval) != 0:
            print("found users with query: " +"and userinfo of" + str(returnval[0]))  

            return render_template("profile.html")
        else:
            print("found no users with query: ")
            cur.execute("INSERT INTO Users (ID, realname) VALUES (%s, %s)", (session["user"].get("userinfo").get("sub"),token.get("userinfo").get("given_name")))
            print("\n added\n")
            return render_template("login.html")
            

        

def setup():
    global pool
    DATABASE_URL = os.environ['DATABASE_URL']
    current_app.logger.info(f"creating db connection pool")
    pool = ThreadedConnectionPool(1, 100, dsn=DATABASE_URL, sslmode='require')


@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

@contextmanager
def get_db_connection():
    try:
        setup()
        connection = pool.getconn()
        yield connection

    finally:
        pool.putconn(connection)


@contextmanager
def get_db_cursor(commit=False):
    with get_db_connection() as connection:
        cursor = connection.cursor(cursor_factory=DictCursor)
        try:
            yield cursor
            if commit:
              connection.commit()
        finally:
            cursor.close()

@app.route("/profile", methods=['GET'])
def profilepage():
    url_for('static', filename = 'styling/style.css')
    return render_template('profile.html') #This will be changed when the basic frame is created and then used as an extension for all of our pages


        

@app.route("/submitUser", methods=['POST'])
def userCreate():
    createUser(request)
    return redirect("/profile")

@app.route("/signup", methods=['GET'])
def signup():
    return render_template("signup.html")











