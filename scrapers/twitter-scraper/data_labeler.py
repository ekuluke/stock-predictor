import json
import os
import pandas as pd
import ast
from tqdm import tqdm
import sys
import faulthandler
import csv
import time
import collections
faulthandler.enable()
  

from sklearn.feature_selection import chi2, SelectKBest

import numpy as np
import pandas as pd





corpus_path = 'corpuses/AFINN/AFINN-165.txt'

def load_corpus_from_raw(path):
    #corpus = pd.read_csv(path, sep=" ", header=None)
    corpus = {}
    with open(path, 'r') as f:
        for l in tqdm(f):
            l = l.rstrip()
            phrase = ""
            for idx, char in enumerate(l):
                if char.isdigit(): # iterate until the valence for the phrase is reached

                    if l[idx-1] == '-':
                        phrase = l[:idx-1].rstrip()
                        corpus[phrase] = str(l[idx-1] + char)
                    else:
                        phrase = l[:idx].rstrip()
                        corpus[phrase] = str(char)
                    break
    return corpus

def save_corpus(corpus):
    if not os.path.exists('corpuses/set_corpuses'):
        os.mkdir('corpuses/set_corpuses')
    with open('corpuses/set_corpuses/' + corpus_path.rsplit('/')[-1], 'w') as f:
        json.dump(data, f)


def load_corpus(fname):
    corpus = {}
    with open('corpuses/set_corpuses/' + fname, 'r') as f:
        contents = f.read()
        corpus = ast.literal_eval(contents)
    return corpus

def load_tweets(stock):
    tweets = {}
    print("Loading " + stock)
    '''
    with open('tweet_data/' + stock, 'r') as f:
        for line in tqdm(f):
            tweets.update(ast.literal_eval(line))
    return tweets
    '''
    with open('tweet_data/' + stock, 'r') as f:
        tweets = json.load(f)

    return tweets

    '''
    #tweets = pd.read_csv('tweet_data/' + stock, header=None, index_col=0, squeeze=True).to_dict()   
    chunksize = 10 ** 6
    pd.read_csv('tweet_data/' + stock, header=None, chunksize=chunksize) as reader:
        return reader
    batch_count = len(contents)/20
    for i in range(1,6):
        tweet_batch = {}
        start = int(batch_count*(i-1))
        end = int(batch_count*i)
        batch = contents[start:end] 
        tweet_batch(ast.literal_eval(batch))
        tweets.update(tweet_batch)
    # parse to 
    #print(tweets)
    return tweets
#        with open('tweet_data/{}'.format(stock) as f:
    '''
    
def extract_features(tweet):
    ngram = {}
    for ngram_size in range(1,4):
        for idx,word in enumerate(tweet):
            phrase = tweet[idx:idx+ngram_size]
            #print(phrase)
            query = ' '.join(phrase)
            if query in corpus:
                ngram[query] = corpus[query]
            else:
                ngram[query] = 0
    #print(ngram)
    return ngram

    '''
    print("Loading " + stock)
    #tweets = pd.read_csv('tweet_data/' + stock, header=None, index_col=0, squeeze=True).to_dict()   
    chunksize = 10 ** 6
    for chunk in pd.read_csv('tweet_data/' + stock, header=None, chunksize=chunksize):     
    '''






try:
    if sys.argv[1] == '-r':
        corpus = load_corpus_from_raw(corpus_path)
        print("saving set corpus")
        save_corpus(corpus)
except IndexError:
    corpus = load_corpus(corpus_path.rsplit('/')[-1]) # split corpus path to get fname

stocks = os.listdir('tweet_data/');
for stock in stocks:
    ngrams = {}
    data = {}
    tweets = load_tweets(stock)
    if not os.path.exists('labelled_data'):
        os.mkdir('labelled_data')
     
    senti_df = pd.DataFrame()
    dfs = []
    super_dfs = []
    rows = {}
    for key, tweet in tqdm(tweets.items()):
      #print(tweet)
      ngram = extract_features(tweet)
      if len(ngram) > 0:
        #print(ngram)
        total_valence = sum([int(i) for i in ngram.values()])
        if total_valence >= 1:
          sentiment = '1'
        elif total_valence <= -1:
          sentiment = '-1'
        else:
          sentiment = '0'

        # convert ngram of features to one hot indicating the presence of a ngram in the tweet 
        ngram = {k:1 for k in ngram}
        #df_row = pd.DataFrame({'sentiment': sentiment,
        row = collections.OrderedDict()
        row['sentiment'] = sentiment
        row.update(ngram)

        rows[key] = row
        if len(rows) > 10000:
          break
        
        #df = pd.DataFrame.from_records([row], index='sentiment')
        #print(df)
        #dfs.append(df)
        ''' 
        if len(dfs) >= 1000:
          print("concating subframes")
          super_dfs.append(pd.concat(dfs, axis=0, ignore_index = True))
          dfs.clear()
        '''
        #senti_df = senti_df.append(row, ignore_index=True)
        #senti_df = pd.concat([senti_df,pd.Series(row)], axis=1, ignore_index=False)
        #print(total_valence)
        #data[' '.join(tweet)] = total_valence
        #print(data[total_valence])

    df = pd.DataFrame.from_dict(rows, orient="index", dtype=int)
    df = df.fillna(0)
    df.set_index('sentiment')
    idx = df.columns.get_loc("sentiment")
    selector = SelectKBest(chi2, k=70)
    selector.fit(df.iloc[:,idx+1:], df.iloc[:,idx])
    df = selector.get_support(indices=True)
    print(df)
    print(df)

    print("saving {}".format(stock))   
    df.to_csv('labelled_data/{}.csv'.format(stock.split('.')[0]))
    print("successfuly saved {}".format(stock))   



  
