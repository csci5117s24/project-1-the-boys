
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
    spAll = {}
    spList = []
    for row in csvreader:
        symbol, name = row[0], row[1]
        spList.append({"symbol":symbol,"name":name, "link":f'https://finance.yahoo.com/quote/{symbol}?.tsrc=fin-srch'})
        spAll[symbol]={"symbol":symbol,"name":name, "link":f'https://finance.yahoo.com/quote/{symbol}?.tsrc=fin-srch'
    }
    spList.pop(0)    
    
    
    return spAll, spList

def query_stock(ticker, name):
    
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
    print(name)
    url = "https://api.brandfetch.io/v2/search/{name}"

    headers = {
        "accept": "application/json",
        "Referer": "localhost:5000"
    }

    response = requests.get(url, headers=headers)
    brandData = response.json()
    
    logo = brandData[0].get("icon")
    
    
    stockData["logo"] = logo
    
    return stockData
    