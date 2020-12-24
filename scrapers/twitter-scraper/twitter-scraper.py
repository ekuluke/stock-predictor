# Scrape

import twint
import datetime as dt
import nltk
import pandas as pd
import sys

fname = "symbol-only-nasdaq-100-index-12-10-2020(1).csv"
def load_stock_symbols():

    stocks = []
    try:
        if sys.argv[1] == "-c":
            f = open("../c-" + fname, 'r')

    except IndexError:
        f = open("../symbol-only-nasdaq-100-index-12-10-2020(1).csv", 'r')
    for line in f:
        stocks.append(line.split(','));
    f.close()
    return stocks;
# format = stock tag/identifier, company name

def save_progress(stocks):
    with open("../c-symbol-only-nasdaq-100-index-12-10-2020(1).csv", 'w') as f:
        for stock in stocks:
            f.write(f"{stock[0]},{stock[1]}\n")

def scrape_tweets(stocks):
    # Configure
    c = twint.Config()
    c.Lang='en'
    stocks = stocks[1:]
        

    # Run
        #source_list = pd.read_csv()
    tweet_map = {}
    bdate=dt.date(2020,12,1)
    edate=dt.date(2020,12,12)
    date_range = pd.date_range(bdate, edate)
    for idx,stock in enumerate(stocks):
        save_progress(stocks[idx:])
        #c.Search = "{0} OR {1}".format(stock[0], stock[1])
        print(stock[0])
        c.Search=stock[0]
        c.Since = "2020-01-01"
        c.Until = "2020-12-20"
        c.Lang = "en"
        c.Store_json = True
        c.Output = "{0}_tweets.json".format(stock[0])
        twint.run.Search(c)
        
        # $TSLA/2020-1233 etc
        query = "${0} OR {1}".format(stock[0], stock[1]) 
        #from:wsj OR from:reuters OR from:business OR from:cnbc OR from:RANsquawk OR from:wsjmarkets
        print(query)
        '''
        tweet_map[stock[0]] = query_tweets(query, limit=50, begindate=begin_date, enddate=end_date, poolsize=50, lang='en')
        for tweet in tweet_map[stock[0]]:
            # Tokenization
            tweet = nltk.word_tokenize(tweet)
            print(tweet)
            # Remove stopwords(irrelevant words)
            for idx, word in tweet:
                stopwords = nltk.corpus.stopwords.words('english')
                if (word in stopwords):
                    del tweet[idx]
                # remove usertags
                elif(word[0] == '@'): 
                    del tweet[idx]
                # remove urls
                elif(word.contains('.com')):
                    del tweet[idx]
                
            print(tweet)
'''
stocks = load_stock_symbols()
scrape_tweets(stocks)

# "$TSLA OR Tesla from:wsj OR from:reuters OR from:business OR from:cnbc OR from:RANsquawk OR from:wsjmarkets" -o tsla_tweets.json -l 10000
