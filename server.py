







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
    return render_template('mainpage.html', splist=splist) #This will be changed when the basic frame is created and then used as an extension for all of our pages





@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")


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











