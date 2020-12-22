import sys
import os
import yfinance as yf
import pandas as pd

msft = yf.Ticker("MSFT")

hist = msft.history(period="1y")

for date,hi,lo in zip(hist.index, hist["High"], hist["Low"]):
    HLPCT = (hi - lo) / lo 
    print("{} with HLPCT {}".format(date, HLPCT))
