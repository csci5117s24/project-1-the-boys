from contextlib import contextmanager
import json
from urllib.parse import quote_plus, urlencode
from authlib.integrations.flask_client import OAuth
from contextlib import contextmanager
import logging
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import DictCursor
from stock_api import *
from flask import Flask, render_template, url_for, request, redirect, current_app, app
import os





def setup():
    global pool
    DATABASE_URL = os.environ['DATABASE_URL']
    current_app.logger.info(f"creating db connection pool")
    pool = ThreadedConnectionPool(1, 500, dsn=DATABASE_URL, sslmode='require')


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

def createUser(request):
    with get_db_cursor(True) as cur:
        current_app.logger.info("submitting form")
        cur.execute("INSERT INTO userinfo (username, password) VALUES (%s, %s)", (request.form.get("username","test"),request.form.get("password","test")))
 
 
 
       
def get_user_info(postList: dict, cur):
    
    userInfo={}
    for  post in postList:
        cur.execute("SELECT username, avatar, realname FROM Users WHERE ID=%s", [postList[post]["posterID"]]) #Rewrite with separate function
        user=cur.fetchall()
        key=postList[post]["posterID"]
        userInfo[key]={
            "username":user[0][0],
            "avatar":user[0][1],
            "name":user[0][2]
        }
    for post in postList:
        
        key=postList[post]["posterID"]
        postList[post]["username"]=userInfo[key]["username"]
        postList[post]["avatar"]=userInfo[key]["avatar"]
        postList[post]["name"]=userInfo[key]["name"]
    
            
    return postList


def createPostList(posts, cur):
    postList={}
   
    for post in posts:
        key = post[0]
        postList[key]={
        "tags":post[1],
        "posterID":post[2],
        "content":post[3]}
    
    return postList


def get_recent_posts():
    with get_db_cursor(True) as cur:
        cur.execute("SELECT * FROM Posts ORDER BY postID DESC")
        posts=cur.fetchall()
        postList = createPostList(posts, cur)
        updatedPostList = get_user_info(postList, cur)
        
        return updatedPostList

def get_stock_list():
    with get_db_cursor(True) as cur:
        cur.execute("SELECT * FROM Stocks")
        
def search_posts_db(query, cur):

    
    cur.execute(f"SELECT * FROM Posts WHERE postContent LIKE '%{query}%'")
    posts = cur.fetchall()
    postList = createPostList(posts, cur)
    updatedPostList = get_user_info(postList,cur)
    return updatedPostList
def get_posts_by_id(user, cur):
    
        
        cur.execute(f"SELECT * FROM Posts WHERE ID='{user[0][0]}'")
        posts = cur.fetchall()
        postList = createPostList(posts, cur)
        updatedPostList = get_user_info(postList,cur)
        return updatedPostList

def find_ticker_via_post(id,cur):
    cur.execute("SELECT ticker FROM Postmeta WHERE PID=%s",[id])    
    ticker = cur.fetchall()
    return ticker
