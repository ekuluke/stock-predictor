#scrape
import sys
import os
import errno
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
        print("File does not exist")
        return None

def initStockData(stockName):
    if not os.path.exists(os.cwd() + stockName):
        try:
            os.mkdir(os.cwd() + stockName)
        except OSError:
            raise
        else:
            print("Created directory for " + stockName + " data")


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
    print("----------------------------------------")
    print(stockName + " Open Prices")
    print("----------------------------------------")
    print(hist["Open"])
    print("----------------------------------------")
    print(stockName + " Close Prices")
    print("----------------------------------------")
    print(hist["Close"])
    print("----------------------------------------")
    print(stockName + " Volumes")
    print("----------------------------------------")
    print(hist["Volume"])
    print("----------------------------------------")
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
        print(input + " hlpct")
        print("----------------------")
        print(hlpct)
        print("----------------------")
        print(input + " pctchange")
        print("----------------------")
        print(pctchange)
        print("----------------------")
    except:
        print("not valid input exiting")
        sys.exit()
else:
    data = readFile(input)
    for d in data:
        open, close, high, low, vol, dates = stockData(d)
        pctchange = calculate_pctchange(dates, high, low)
        hlpct = calculate_hlpct(dates, high, low)
        print(d + " hlpct")
        print("--------------------")
        print(hlpct)
        print("--------------------")
        print(d + " pctchange")
        print("--------------------")
        print(pctchange)
        print("--------------------")
