
import requests
import json
import csv
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