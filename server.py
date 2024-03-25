

from flask import Flask, render_template, url_for, request, redirect
from jinja2 import Environment, Template
import os
import filetype
from flask import Flask, render_template, redirect, jsonify
from flask import current_app, g, request, url_for, session,send_file
from contextlib import contextmanager
import json
from jsonify import *
from urllib.parse import quote_plus, urlencode
from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from contextlib import contextmanager
import logging
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import DictCursor
from stock_api import *
from database_stuff import *
from werkzeug.utils import secure_filename
from io import *
import io
from datetime import date, timedelta
app = Flask(__name__)
environment = Environment

import json
from six.moves.urllib.request import urlopen
from functools import wraps

from flask_cors import cross_origin
from jose import jwt
app.secret_key = os.environ["FLASK_SECRET"]
# from auth import *
oauth = OAuth(app)

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)
oauth.register(
    "auth0",
    client_id=os.environ.get("AUTH0_CLIENT_ID"),
    client_secret=os.environ.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{os.environ.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)
AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")

class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response

app.config['OAUTH2_ISSUER'] = "https://dev-byqpo5m3kywgc0q4.us.auth0.com"
app.config['OAUTH2_CLIENT_ID'] = os.environ.get("AUTH0_CLIENT_ID")
app.config['OAUTH2_CLIENT_SECRET'] = os.environ.get("AUTH0_CLIENT_SECRET")
# from flask_oauth2_validation import OAuth2Decorator
# oauth2 = OAuth2Decorator(app)

@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response
def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    auth = session.get("Authorization", None)
    if not auth:
        raise AuthError({"code": "authorization_header_missing",
                        "description":
                            "Authorization header is expected"}, 401)

    parts = auth.get("access_token",None)
    print(parts[0])
    # if parts[0].lower() != "bearer":
    #     raise AuthError({"code": "invalid_header",
    #                     "description":
    #                         "Authorization header must start with"
    #                         " Bearer"}, 401)
    # elif len(parts) == 1:
    #     raise AuthError({"code": "invalid_header",
    #                     "description": "Token not found"}, 401)
    # elif len(parts) > 2:
    #     raise AuthError({"code": "invalid_header",
    #                     "description":
    #                         "Authorization header must be"
    #                         " Bearer token"}, 401)

    token = parts
    return token

def requires_auth(f):
    """Determines if the Access Token is valid
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_auth_header()
        jsonurl = urlopen("https://"+AUTH0_DOMAIN+"/.well-known/jwks.json")
        jwks = json.loads(jsonurl.read())
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        print(jwks)
        print("printing header")
        print(unverified_header)
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=API_AUDIENCE,
                    issuer="https://"+AUTH0_DOMAIN+"/"
                )
            except jwt.ExpiredSignatureError:
                raise AuthError({"code": "token_expired",
                                "description": "token is expired"}, 401)
            except jwt.JWTClaimsError:
                raise AuthError({"code": "invalid_claims",
                                "description":
                                    "incorrect claims,"
                                    "please check the audience and issuer"}, 401)
            except Exception:
                raise AuthError({"code": "invalid_header",
                                "description":
                                    "Unable to parse authentication"
                                    " token."}, 401)

            _request_ctx_stack.top.current_user = payload
            return f(*args, **kwargs)
        raise AuthError({"code": "invalid_header",
                        "description": "Unable to find appropriate key"}, 401)
    return decorated


# @requires_auth
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
    
    splist=SPCSV()
    splist.pop(0)
    recent_posts=get_recent_posts()
    stockData=''
    if(request.args.get("stock")):
        ticker=request.args.get("stock")
        stockData = query_stock(ticker)
    for stock in splist:
        stock['link'] = f'https://finance.yahoo.com/quote/{stock["symbol"]}?.tsrc=fin-srch'
    subs=[]
    follows=[]
    if session["user"].get("userinfo"):
        user=session["user"].get("userinfo").get("sub")
        
        with get_db_cursor(True) as cur:
            cur.execute("select ticker, name from stocks where ticker in (select ticker FROM subscriptions WHERE uid = %s)",(str(session["user"].get("userinfo").get("sub")),))
            subs= subs+cur.fetchall()
            cur.execute("select poster FROM followers WHERE follower = %s",(session["user"].get("userinfo").get("sub"),))
            follows = follows+cur.fetchall()
            print(follows)  
    print(subs)
    
    return render_template('mainpage.html', splist=splist,  posts=recent_posts,subscriptions=subs,followers=follows,stockData=stockData) #This will be changed when the basic frame is created and then used as an extension for all of our pages
    return render_template('mainpage.html', splist=splist,  recent=recent_posts,subscriptions=subs,followers=follows,stockData=stockData) #This will be changed when the basic frame is created and then used as an extension for all of our pages

# # @requires_auth
@app.route("/editProfile", methods=['POST'])
def editProfile():
    file = request.files["image"]
    file.filename = secure_filename(file.filename)

    print(file.filename)
    mimetype = filetype.guess(file).mime
    print(mimetype)
    fs=file.read()
    with get_db_cursor(True) as cur:
        print(request.form)

        cur.execute("UPDATE users SET (username,realname,avatar,avatarmimetype) = (%s,%s,%s,%s) WHERE ID = %s",(request.form['username'],request.form['realname'],fs,str(mimetype),session["user"].get("userinfo").get("sub"),))
        cur.execute("select * FROM users WHERE ID = %s",(str(session["user"].get("userinfo").get("sub")),)) 
        returnval = cur.fetchall()
        session["username"]=returnval[0][1]
        session["realname"]=returnval[0][2]
        return redirect("/profile")

    
    
    
@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    session["Authorization"]=token
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
            return redirect("/profile/" + returnval[0][0])
        else:
            print("found no users with query: ")
            cur.execute("INSERT INTO Users (ID, realname) VALUES (%s, %s)", (session["user"].get("userinfo").get("sub"),token.get("userinfo").get("given_name")))
            print("\n added\n")
            return render_template("login.html")
            

# @requires_auth
@app.route("/Post",methods=['POST'])
def post():
    with get_db_cursor(True) as cur:
        tags=request.form.getlist("tags")
        user=session["user"].get("userinfo").get("sub")
        ticker=request.form.get("stock")
        postContent = request.form.get("description")
        cur.execute("INSERT INTO posts (tags, ID, postContent ) VALUES (%s, %s,%s)", (tags,session["user"].get("userinfo").get("sub"),postContent,))
        return render_template('profile.html')

@app.route("/stocks", methods=["GET"])
def viewStocks():
    splist=SPCSV()
    splist.pop(0)
    stockData=''
    
    if(request.args.get("stock")):
        ticker=request.args.get("stock")
        stockData = query_stock(ticker)
        
    
    return render_template('stock_view.html', stocks=splist, stockData=stockData)

@app.route("/stocks/<ticker>")
def stockRedirect():
    pass

@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )



@app.route("/profile", methods=['GET'])
@cross_origin(headers=["Content-Type", "Authorization"])
@cross_origin(headers=["Access-Control-Allow-Origin", "http://localhost:"])
# @requires_auth
def profilepage():
    url_for('static', filename = 'styling/style.css')
    with get_db_cursor(True) as cur:
        cur.execute("select * FROM posts WHERE ID = %s",(str(session["user"].get("userinfo").get("sub")),)) 
        posts = cur.fetchall()
        splist=SPCSV()
        splist.pop(0)
        cur.execute("select * FROM users WHERE ID = %s",((str(session["user"].get("userinfo").get("sub")),)))
        userret=cur.fetchall()
        return render_template('profile.html',username=userret[0][1],realname=userret[0][2],posts=posts, stocks=splist,userid=session["user"].get("userinfo").get("sub")) #This will be changed when the basic frame is created and then used as an extension for all of our pages


@app.route("/profile/<user>", methods=['GET'])
def profilepageUser(user):
    url_for('static', filename = 'styling/style.css')
    with get_db_cursor(True) as cur:
        cur.execute("select * FROM posts WHERE ID = %s",(user,)) 
        posts = cur.fetchall()
        print("printing posts")
        print(posts)
        splist=SPCSV()
        splist.pop(0)        
        cur.execute("select * FROM users WHERE ID = %s",(user,)) 
        userret=cur.fetchall()
        return render_template('profile.html',username=userret[0][1],realname=userret[0][2],posts=posts, stocks=splist,userid=user) #This will be changed when the basic frame is created and then used as an extension for all of our pages

# @requires_auth
@app.route("/follow/<uid>")
def follow(uid):
    with get_db_cursor(True) as cur:
        user=session["user"].get("userinfo").get("sub")
        cur.execute("INSERT INTO followers (follower, poster ) VALUES (%s, %s)", (user,uid,))
        return redirect("/profile")

# @requires_auth
@app.route("/getAvatar")
def getAvatar():
    with get_db_cursor(True) as cur:
        cur.execute("select avatar,avatarmimetype FROM users WHERE ID = %s",(str(session["user"].get("userinfo").get("sub")),)) 
        returnval = cur.fetchall()
        stream = io.BytesIO(returnval[0][0])
        print(returnval[0][1])
        return send_file(stream,mimetype=returnval[0][1])


@app.route("/getAvatar/<uid>")
def getAvatarWithUid(uid):
    with get_db_cursor(True) as cur:
        cur.execute("select avatar,avatarmimetype FROM users WHERE ID = %s",(uid,)) 
        returnval = cur.fetchall()
        stream = io.BytesIO(returnval[0][0])
        print(returnval[0][1])
        return send_file(stream,mimetype=returnval[0][1])
        

@app.route("/submitUser", methods=['POST'])
def userCreate():
    createUser(request)
    return redirect("/profile")


@app.route("/signup", methods=['GET'])
def signup():
    return render_template("signup.html")


# @requires_auth
@app.route("/followStock/<ticker>")
def followStock(ticker):
    with get_db_cursor(True) as cur:
        cur.execute("INSERT INTO subscriptions (uid,ticker) VALUES (%s,%s)",(session["user"].get("userinfo").get("sub"),ticker,))
        print("executed")
        return redirect("/")

@app.route("/unfollowStock/<ticker>")
def unfollowStock(ticker):
    with get_db_cursor(True) as cur:
        cur.execute("INSERT INTO subscriptions (uid,ticker) VALUES (%s,%s)",(session["user"].get("userinfo").get("sub"),ticker,))
        print("executed")
        return redirect("/")
@app.route("/api/searchPosts")
def searchPosts():
    splist=SPCSV()
    splist.pop(0)
    
    searchPosts = search_posts_db(request.args.get("searchPosts"))
    stockData = ''
    if(request.args.get("stock")):
        ticker=request.args.get("stock")
        stockData = query_stock(ticker)
    for stock in splist:
        stock['link'] = f'https://finance.yahoo.com/quote/{stock["symbol"]}?.tsrc=fin-srch'
    
    
    return render_template('mainpage.html', splist=splist, posts=searchPosts, stockData = stockData)






