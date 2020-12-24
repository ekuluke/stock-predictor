# Scrape

from twitterscraper import query_tweets
import datetime as dt
import nltk

def load_stock_symbols():
    stocks = []
    f = open("../symbol-only-nasdaq-100-index-12-10-2020(1).csv", 'r')
    for line in f:
        stocks.append(line.split(','));
    f.close()
    return stocks;
    # format = stock tag/identifier, company name

def scrape_tweets(stocks):
    #source_list = pd.read_csv()
    tweet_map = {}
    for stock in stocks:
        query = "${0} OR {1}".format(stock[0], stock[1]) 
        #from:wsj OR from:reuters OR from:business OR from:cnbc OR from:RANsquawk OR from:wsjmarkets
        print(query)
        begin_date=dt.date(2020,12,1)
        end_date=dt.date(2020,12,12)

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

stocks = load_stock_symbols()
scrape_tweets(stocks)

# "$TSLA OR Tesla from:wsj OR from:reuters OR from:business OR from:cnbc OR from:RANsquawk OR from:wsjmarkets" -o tsla_tweets.json -l 10000
