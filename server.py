
from flask import Flask, render_template, url_for, request, redirect
from jinja2 import Environment, Template
import os
from contextlib import contextmanager
import json
from stock_api import fetch_tops

app = Flask(__name__)
environment = Environment

@app.route("/", methods=['GET'])
def mainpage():
    url_for('static', filename = 'styling/style.css')
    tops = fetch_tops()
    
    return render_template('mainpage.html', topStock=tops) #This will be changed when the basic frame is created and then used as an extension for all of our pages
















