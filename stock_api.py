
import requests
import json
import csv
import pandas as pd
import numpy as np
import os
# import lightweight-charts



def SPCSV():
    file = open('static\csv\constituents.csv')
    csvreader = csv.reader(file)
    spAll = []
    
    for row in csvreader:
        spAll.append({"symbol":row[0],"name":row[1]})
    print(len(spAll))
    
    return spAll


    
def query_stock():
    pass