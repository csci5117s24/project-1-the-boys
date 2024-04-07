

from flask import Flask, render_template, url_for, request, redirect, session,send_file, g
from jinja2 import Environment, Template
import os
import filetype
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
import io

app = Flask(__name__, static_url_path='/static')
environment = Environment

import json
from six.moves.urllib.request import urlopen
from functools import wraps

from flask_cors import cross_origin
from jose import jwt
app.secret_key = os.environ["FLASK_SECRET"]
# from auth import *
oauth = OAuth(app)
splist=SPCSV()

picture="/static/images/profile-user.png"
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

#Page Nav
@app.route("/", methods=['GET', 'POST'])
def mainpage():
    yourid, subs, follows = [], [], []
    
    
    url_for('static', filename = 'styling/style.css')
    stockData, posts = '', get_recent_posts()
    subs=[]
    follows=[]
    search=''
    if(request.args.get("stock-datalist")):
        
        ticker=request.args.get("stock-datalist")
        for stock in splist:
            if stock.get("symbol")==ticker:
                name=stock.get("name")
        stockData = query_stock(ticker,name)
        stockData["name"] = name
        if(stockData["domain"] is None):            
            
            stockData["domain"] = name.split(" ")[0]
    picture=None
    yourid=[]
    if request.args.get("searchPosts"):
        search = request.args.get("searchPosts")
        with get_db_cursor(True) as cur:
            posts =search_posts_db(search, cur)
        
    if session.get("user",None):
        if session["user"].get("userinfo"):
            userSession=session["user"].get("userinfo")
            user = userSession.get("sub")
            
            with get_db_cursor(True) as cur:
                cur.execute("select ticker, name from stocks where ticker in (select ticker FROM subscriptions WHERE uid = %s)",(str(session["user"].get("userinfo").get("sub")),))
                subs= subs+cur.fetchall()
                cur.execute("select poster FROM followers WHERE follower = %s",(session["user"].get("userinfo").get("sub"),))
                follows = follows+cur.fetchall()
                yourid+=[session["user"].get("userinfo").get("sub")]
        
    
    return render_template('mainpage.html', splist=splist,  posts=posts,subscriptions=subs,followers=follows, stockData = stockData, userPFP=picture,yourid=yourid, search=search) 



@app.route("/profile", methods=['GET'])
@cross_origin(headers=["Content-Type", "Authorization"])
@cross_origin(headers=["Access-Control-Allow-Origin", "http://localhost:"])
# @requires_auth
def profilepage():
    url_for('static', filename = 'styling/style.css')
    if not session.get("user",None):
        return redirect("/login")
    with get_db_cursor(True) as cur:
        
        cur.execute(f"SELECT ID FROM USERS WHERE username = '{session['username']}'")
        id=cur.fetchall()
        
        posts=get_posts_by_id(id, cur)
        
        
        cur.execute(f"SELECT username, avatar, realname FROM Users WHERE ID='{id[0][0]}'")
        user=cur.fetchall()
        print(user)
        postList=[]
        username=user[0][0]
        realname=user[0][2]
        userSession=session["user"].get("userinfo")
        picture = userSession.get("picture")    
        
        for post in posts:
            key=posts[post]["posterID"]
            posts[post]["username"]=user[0][0]
            posts[post]["avatar"]=user[0][1]
            posts[post]["name"]=user[0][2]
             
         
        postList=posts
        
        
        return render_template('profile.html',username=username,realname=realname,posts=postList, stocks=splist,userid=id[0][0], userPFP=picture) 

    
#Authorization
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
#user interaction
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


@app.route("/unsubscribe/<ticker>", methods=['GET'])
def unsubscribe(ticker):
    url_for('static', filename = 'styling/style.css')
    user=session["user"].get("userinfo").get("sub")
    with get_db_cursor(True) as cur:
            cur.execute("delete from subscriptions where uid = %s and ticker = %s",(user,ticker),)
    return redirect("/")


@app.route("/unfollow/<uid>", methods=['GET'])
def unfollow(uid):
    url_for('static', filename = 'styling/style.css')
    user=session["user"].get("userinfo").get("sub")
    with get_db_cursor(True) as cur:
            cur.execute("delete from followers where follower = %s and poster = %s",(user,uid),)
    return redirect("/")

@app.route("/deletePost/<pid>", methods=['GET'])
def deletePost(pid):
    url_for('static', filename = 'styling/style.css')
    user=session["user"].get("userinfo").get("sub")
    with get_db_cursor(True) as cur:
            cur.execute("delete from posts where ID = %s and postID = %s",(user,pid))
    return redirect("/")
            
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
# @requires_auth
@app.route("/Post",methods=['POST'])
def post():
    with get_db_cursor(True) as cur:
        tags=request.form.getlist("tags")
        user=session["user"].get("userinfo").get("sub")
        ticker=request.form.get("stock-datalist")
        postContent = request.form.get("description")
        cur.execute("INSERT INTO posts (tags, ID, postContent ) VALUES (%s, %s,%s)", (tags,session["user"].get("userinfo").get("sub"),postContent,))
    return redirect("/")

    
@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )





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
            return redirect("/profile")
        else:
            print("found no users with query: ")
            cur.execute("INSERT INTO Users (ID, realname) VALUES (%s, %s)", (session["user"].get("userinfo").get("sub"),token.get("userinfo").get("given_name")))
            print("\n added\n")
            return render_template("login.html")
            
#Call functions non-session user


@app.route("/stocks/<ticker>")
def stockRedirect():
    pass


@app.route("/profile/<user>", methods=['GET'])
def profilepageUser(user):
    url_for('static', filename = 'styling/style.css')
    with get_db_cursor(True) as cur:
        cur.execute(f"SELECT ID FROM Users WHERE username='{user}'")
        id = cur.fetchall()
        print(cur.fetchall())
        posts=get_posts_by_id(id, cur)
        cur.execute(f"SELECT username, avatar, realname FROM Users WHERE ID='{id[0][0]}'")
        user=cur.fetchall()
        username=user[0][0]
        realname=user[0][2]
        picture=user[0][1]
        
        
        return render_template('profile.html',username=username,realname=realname,posts=posts, stocks=splist,userid=id[0][0], userPFP=picture) 
 

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
    
    with get_db_cursor(False) as cur:
        cur.execute("select avatar,avatarmimetype FROM users WHERE ID = %s",(str(session["user"].get("userinfo").get("sub")),)) 
        returnval = cur.fetchall()
    stream = io.BytesIO(returnval[0][0])
    session['user']['userinfo']['picture'] = stream
    return send_file(stream,mimetype=returnval[0][1])


@app.route("/getAvatar/<uid>")
def getAvatarWithUid(uid):
    print(uid)
    with get_db_cursor(False) as cur:
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
    
    
@app.route("/api/searchPosts", methods=["POST", "GET"])
def searchPosts():
    
    subs=[]
    follows=[]
    picture=None
    yourid=[]
    searchFor = request.get_json()
    print("searchFor", searchFor)
    stockData = searchFor
    if session.get("user",None):
        if session["user"].get("userinfo"):
            userSession=session["user"].get("userinfo")
            user = userSession.get("sub")
            
            with get_db_cursor(True) as cur:
                cur.execute("select ticker, name from stocks where ticker in (select ticker FROM subscriptions WHERE uid = %s)",(str(session["user"].get("userinfo").get("sub")),))
                subs= subs+cur.fetchall()
                cur.execute("select poster FROM followers WHERE follower = %s",(session["user"].get("userinfo").get("sub"),))
                follows = follows+cur.fetchall()
                yourid+=[session["user"].get("userinfo").get("sub")]
                searchPosts = search_posts_db(searchFor['searchPosts'], cur)
    else:
        with get_db_cursor(True) as cur:
            searchPosts = search_posts_db(searchFor['searchPosts'], cur)
    
    
    print(splist,  searchPosts,subs,follows, stockData,picture,yourid)
    return render_template('mainpage.html', splist=splist,  posts=searchPosts,  subscriptions=subs,followers=follows, stockData = stockData, userPFP=picture,yourid=yourid) 

@app.route("/api/queryStock", methods=["POST", "GET"])
def stockSearch():
    yourid, subs, follows = [], [], []
    url_for('static', filename = 'styling/style.css')
    
    if request.method=="POST" and request.content_type=="application/json":
        input_data = request.get_json()
        print(input_data)
        if input_data["type"]=="Search":
            with get_db_cursor(True) as cur:
                posts = search_posts_db(input_data['searchPosts'], cur)
                stockData = input_data
        elif input_data["type"]=="Stock":
            ticker = input_data['stock-datalist']
            name=''
            for stock in splist:
                if stock.get("symbol")==ticker:
                    name=stock.get("name")
            if len(input_data['searchFor']):
                posts = search_posts_db(input_data['searchFor'])
            else:
                posts = get_recent_posts()
            stockData=query_stock(ticker,name)
            stockData["name"] = name
            if(stockData["domain"] is None):            
                stockData["domain"] = name.split(" ")[0] 
    
    if session.get("user",None):
        if session["user"].get("userinfo"):
            userSession=session["user"].get("userinfo")
            user = userSession.get("sub")
            
            with get_db_cursor(True) as cur:
                cur.execute("select ticker, name from stocks where ticker in (select ticker FROM subscriptions WHERE uid = %s)",(str(session["user"].get("userinfo").get("sub")),))
                subs= subs+cur.fetchall()
                cur.execute("select poster FROM followers WHERE follower = %s",(session["user"].get("userinfo").get("sub"),))
                follows = follows+cur.fetchall()
                yourid+=[session["user"].get("userinfo").get("sub")]
    
    return render_template('mainpage.html', splist=splist,  posts=posts,subscriptions=subs,followers=follows, stockData = stockData, userPFP=picture,yourid=yourid) 





