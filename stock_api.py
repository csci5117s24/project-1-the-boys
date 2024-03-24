
import requests
import json
import csv
import pandas as pd
import numpy as np
import os
from datetime import date, timedelta
# import lightweight-charts



def SPCSV():
    file = open('static\csv\constituents.csv')
    csvreader = csv.reader(file)
    spAll = []
    
    for row in csvreader:
        spAll.append({"symbol":row[0],"name":row[1]})
    print(len(spAll))
    
    return spAll

def query_stock(ticker):
    
    today=date.today()
    if(date.weekday(today)>4):
        daysBack= date.weekday(today)-4
        today=  today-timedelta(days=daysBack)
    elif(date.weekday(today)==0):
        today = today-timedelta(days=3)
    else:
        today= today-timedelta(days=1)
       
    url=f'https://api.polygon.io/v1/open-close/{ticker}/{today}?adjusted=true&apiKey={os.environ.get("POLYGON.IO_API_KEY")}'
    
    r = requests.get(url)
    stockData = r.json()
    return stockData
    