
import requests
import json
import csv
import pandas as pd
import numpy as np
def fetch_tops():
    #change below to make the url changeable
    url="https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/2024-01-03?adjusted=true&apiKey=JppXf9iaJ1aRS17NPdbBO1Xu6cWwL9QA"
    results = requests.get(url)
    parsedResults = results.json()
    results = parsedResults['results']
    
    topStock=''
    high=0
    for stock in results:
        change=stock['h']-stock['l']
        if(change>high):
            topStock=stock.get('T')
            high=change
            stockHigh = stock['h']
            stockLow = stock['l']
    
    return [topStock,int(high), stockHigh, stockLow]


def SPCSV():
    file = open('static\csv\constituents.csv')
    csvreader = csv.reader(file)
    spAll = []
    for row in csvreader:
        spAll.append({"symbol":row[0],"name":row[1]})
    print(len(spAll))
    
    return spAll

def top_gainers():
    data=pd.read_html("https://markets.businessinsider.com/index/market-movers/s&p_500")
    print(data[0].columns.str.strip())
    
  
    gname=[]
    gprice=[]
    # gainList = [i for i in range(15) {"gname":data[0]["Name"].get(i),"gprice":data[0]["Latest Price Previous Close"].get(i)}]
    gainList=[]
    for i in range(15):
        gainList.append({"gname":data[0]["Name"].get(i),"gprice":data[0]["Latest Price Previous Close"].get(i),"gpercent":data[0]["+/- %"].get(i)})
        
    # for i in range(13):
    #     gname.append(data[0]["Name"].get(i))
    #     gprice.append(data[0]["Latest Price Previous Close"].get(i))
    #     gpercent.append(data[0]["+/- %"].get(i))
    #     Lname.append(data[1]["Name"].get(i))
    #     Lprice.append(data[1]["Latest Price Previous Close"].get(i))
    #     Lpercent.append(data[1]["+/- %"].get(i))

    

    
    return gainList