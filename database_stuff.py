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
    pool = ThreadedConnectionPool(1, 100, dsn=DATABASE_URL, sslmode='require')


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
        


def get_recent_posts():
    with get_db_cursor(True) as cur:
        cur.execute("SELECT * FROM Posts")
        posts=cur.fetchall()
        
        postList={}
        for post in posts:
            key = f'post_id_{post[0]}'
            postList[key]={
            "tags":post[1],
            "posterID":post[2],
            "content":post[3]}

    with get_db_cursor(True) as cur:
        userInfo={}
        for  post in postList:
            cur.execute("SELECT username, avatar FROM Users WHERE ID=%s", [postList[post]["posterID"]]) #Rewrite with separate function
            user=cur.fetchall()
           
            key=postList[post]["posterID"]
            userInfo[key]={
                "username":user[0][0],
                "avatar":user[0][1]
            }
        for post in postList:
            key=postList[post]["posterID"]
            postList[post]["username"]=userInfo[key]["username"]
            postList[post]["avatar"]=userInfo[key]["avatar"]
        
            
        return postList
def get_user_info(id):
    
    return True
def get_stock_list():
    with get_db_cursor(True) as cur:
        cur.execute("SELECT * FROM Stocks")
        print(cur.fetchall())
def search_posts(query):
    with get_db_cursor(True) as cur:
        cur.execute(f'SELECT * FROM Posts WHERE postContent LIKE %{query}%')
        print(cur.fetchall())
    
        

    