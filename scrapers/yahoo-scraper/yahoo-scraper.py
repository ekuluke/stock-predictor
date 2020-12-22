#scrape
import sys
import os
import yfinance as yf
import pandas as pd

pd.set_option('max_columns', None)
# pd.set_option('max_rows', None)
input = sys.argv[1]

def readFile(path):
    data = []
    if os.stat(path).st_size == 0:
        return None
    try:
        f = open(path, 'r')
        lines = f.readlines()
        if len(lines) > 1:
            for line in lines:
                line = line.replace('\n', '')
                if line != "":
                    data.append(line)
        elif len(lines) == 1:
            if lines[0] != "":
                lines[0] = lines[0].replace('\n', '')
                data = lines[0]
        return data
    except FileNotFoundError:
        return None

def stockData(stockName):
    try:
        print("----------------------------------------")
        print("Looking for " + stockName + " stock data")
        print("----------------------------------------")
        stock = yf.Ticker(stockName)
    except:
        print("unable to find stock data for: " + stockName)
    hist = stock.history(period="1y")
    open = hist["Open"]
    close = hist["Close"]
    high = hist["High"]
    low = hist["Low"]
    vol = hist["Volume"]
    print("Open Prices")
    print(hist["Open"])
    print("----------------------------------------")
    print("Close Prices")
    print(hist["Close"])
    print("----------------------------------------")
    print("Volumes")
    print(hist["Volume"])
    print("----------------------------------------")
    #HLPCT
    #CHANGEPCT

if input == None:
    print("no input exiting!")
    sys.exit()

if input.find("txt") == -1:
    try:
        stockData(input)
    except:
        print("not string exiting")
        sys.exit()
else:
    data = readFile(input)
    for d in data:
        stockData(d)
