
from flask import Flask, render_template, url_for, request, redirect
from jinja2 import Environment, Template
import os
from contextlib import contextmanager
import json

app = Flask(__name__)
environment = Environment

@app.route("/", methods=['GET'])
def mainpage():
    url_for('static', filename = 'styling/style.css')
    return render_template('mainpage.html') #This will be changed when the basic frame is created and then used as an extension for all of our pages
