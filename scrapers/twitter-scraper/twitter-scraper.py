# Scrape

from twitterscraper import query_tweets

def load_stock_symbols():
    symbols = []
    f = open("../symbol-only-nasdaq-100-index-12-10-2020(1).csv", 'r')
    for line in f:
        symbols.append(line);
    f.close()
    return symbols;
 "$TSLA OR Tesla from:wsj OR from:reuters OR from:business OR from:cnbc OR from:RANsquawk OR from:wsjmarkets" -o tsla_tweets.json -l 10000
