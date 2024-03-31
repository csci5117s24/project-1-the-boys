
import requests
import json
import csv
import pandas as pd
import numpy as np
import os
from datetime import date, timedelta
# import lightweight-charts



def SPCSV():
    file = open('static/csv/constituents.csv')
    csvreader = csv.reader(file)
    
    spList = []
    for row in csvreader:
        symbol, name = row[0], row[1]
        spList.append({"symbol":symbol,"name":name, "link":f'https://finance.yahoo.com/quote/{symbol}?.tsrc=fin-srch'})
    spList.pop(0)    
    
    
    return spList

def query_stock(ticker, name):
    print(ticker,name)
    today=date.today()
    if(date.weekday(today)>4):
        daysBack= date.weekday(today)-4
        today=  today-timedelta(days=daysBack)
    elif(date.weekday(today)==0):
        today = today-timedelta(days=3)
    else:
        today= today-timedelta(days=1)
    print(today)
    #url=f'https://api.polygon.io/v1/open-close/{ticker}/{today}?adjusted=true&apiKey={os.environ.get("POLYGON.IO_API_KEY")}'
    url=f'https://api.polygon.io/v2/aggs/ticker/{ticker}/prev?adjusted=true&apiKey={os.environ.get("POLYGON.IO_API_KEY")}'
    
    r = requests.get(url)
    stockResponse = r.json()
    print(stockResponse)
    stockData = {
        'symbol':stockResponse.get('ticker'),
        'name': stockResponse.get('name'),
        'domain':stockResponse.get('domain'),
        'from':today,
        'open':stockResponse.get('results')[0].get('o'),
        'close':stockResponse.get('results')[0].get('c'),
        'high':stockResponse.get('results')[0].get('h'),
        'low':stockResponse.get('results')[0].get('l'),
        'volume':stockResponse.get('results')[0].get('v')
        
    }
    print(stockData)
    
    
    return stockData
    