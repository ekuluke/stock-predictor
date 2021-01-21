# Scrape

import twint
import datetime as dt
import nltk
nltk.download('punkt')
nltk.download('stopwords')
import pandas as pd
import sys
import os
import json


fname = "symbol-only-nasdaq-100-index-12-10-2020(1).csv"
def load_stock_symbols():

    stocks = []
    try:
        if sys.argv[1] == "-n":
            f = open(fname, 'r')
    except IndexError:
            f = open("c-" + fname, 'r')
    for line in f:
        stocks.append(list(map(str.rstrip, line.split(','))));
    f.close()
    return stocks;
# format = stock tag/identifier, company name

def save_progress(stocks):
    print(stocks)
    with open("c-symbol-only-nasdaq-100-index-12-10-2020(1).csv", 'w') as f:
        for stock in stocks:
            stock = list(map(str.rstrip, stock))
            f.write(stock[0] + "," + stock[1] + "\n")

def scrape_tweets(stocks):
    # Configure
    c = twint.Config()
    c.Lang='en'
        

    # Run
        #source_list = pd.read_csv()
    tweet_map = {}
    bdate=dt.date(2020,12,1)
    edate=dt.date(2020,12,12)
    date_range = pd.date_range(bdate, edate)
    for idx,stock in enumerate(stocks):
        save_progress(stocks[idx:])
        #c.Search = "{0} OR {1}".format(stock[0], stock[1])
        c.Search= "$" + stock[0]
        c.Since = "2020-01-01"
        c.Until = "2021-01-01"
        c.Lang = "en"
        c.Min_likes = 1
        c.Store_object = True
        #c.Limit = 10
        #c.Output = "tweet_data/{0}_tweets.json".format(stock[0])
        try:
            twint.run.Search(c)
        except:
            os.execv(sys.executable, ['python3'] + sys.argv)
        tweets = twint.output.tweets_list
        
        buf = {}
        for tweet_data in tweets:
            # Tokenization
            print(tweet_data.tweet)
            #tweet = nltk.word_tokenize(tweet_data.tweet)
            tweet = tweet_data.tweet.split(' ')
            # Remove stopwords(irrelevant words)
            tweet_map = {} 

            for word in tweet[:]: # iterate over copy while modifying original
                if len(word) < 1:
                    tweet.remove(word)
                    continue
                '''
                stopwords = nltk.corpus.stopwords.words('english')
                if word in stopwords:
                    del temp_tweet[idx]
                '''
                # remove usertags
                if word[0] == '@': 
                    tweet.remove(word)
                    continue
                if word[0] == '$': 
                    tweet.remove(word)
                    continue
                # remove urls
                if ('.com' in word or 'https://t.co/' in word):
                    tweet.remove(word)
            buf[tweet_data.datestamp + '-' + tweet_data.timestamp] = tweet
            '''f.write(str(stock[0] + tweet_data.datestamp + '-' + tweet_data.timestamp + ','))
            for word in tweet:
                f.write(str(word) + ',')
            f.write('\n')
            '''
        #pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
        '''writer = csv.writer(f)
        for key, value in buf.items():
            writer.writerow([key, value])
        '''
        fname = "tweet_data/{0}.json".format(stock[0])
        try: 
            f = open(fname, 'w')
        except FileNotFoundError:
            os.makedirs(os.path.dirname(fname), exist_ok=True)
            f = open(fname, 'w')

        json.dump(buf, f)
        f.close()


        
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
