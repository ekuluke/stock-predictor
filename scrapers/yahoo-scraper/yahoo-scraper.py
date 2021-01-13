#scrape
import sys
import os
import yfinance as yf
import pandas as pd
from functools import reduce

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
        print("File does not exist")
        return None

def initStockData(stockName):
    if not os.path.exists(os.getcwd() +'/'+ stockName):
        try:
            os.mkdir(stockName)
        except OSError:
            raise OSError
        else:
            print("Created directory for " + stockName + " data")
    else:
        print("folder already exists!")


def mergeDataFrames(dataFrames):
    df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['Date'], how='outer'), dataFrames)
    return df_merged

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
    dates = hist.index

    return open, close, high, low, vol, dates

def calculate_hlpct(dates, high, low):
    hlpctData = []
    for date, hi, lo in zip(dates, high, low):
        hlpct = (hi - lo)/lo
        hlpctData.append(hlpct)
    dfHlpct = pd.DataFrame(hlpctData,index=dates,columns=["hlpct"])
    return dfHlpct

def calculate_pctchange(dates, open, close):
    pctchangeData = []
    for date, op, cl in zip(dates, open, close):
        pctchange = (cl - op)/op
        pctchangeData.append(pctchange)
    dfPctchange = pd.DataFrame(pctchangeData,index=dates,columns=["pctchange"])
    return dfPctchange

if input == None:
    print("no input exiting!")
    sys.exit()

if input.find("txt") == -1:
    try:
        open, close, high, low, vol, dates = stockData(input)
        pctchange = calculate_pctchange(dates, high, low)
        hlpct = calculate_hlpct(dates, high, low)
        initStockData(input)
        dataFrames = [open,close,high,low,vol,pctchange,hlpct]
        dfMerged = mergeDataFrames(dataFrames)
        dfMerged.to_csv(os.getcwd() + '/' + input + '/' + input+"StockData"+".csv")
    except:
        print("something went wrong exiting")
        sys.exit()
else:
    data = readFile(input)
    for d in data:
        try:
            open, close, high, low, vol, dates = stockData(d)
            initStockData(d)
            pctchange = calculate_pctchange(dates, high, low)
            hlpct = calculate_hlpct(dates, high, low)
            dataFrames = [open,close,high,low,vol,pctchange,hlpct]
            dfMerged = mergeDataFrames(dataFrames)
            dfMerged.to_csv(os.getcwd() + '/' + d + '/' + d + "StockData" + ".csv")
        except:
            raise Exception("something went wrong")
            sys.exit()
