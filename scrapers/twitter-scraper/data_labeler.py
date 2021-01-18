import json
import os
import pandas as pd
import ast
from tqdm import tqdm
import sys
import faulthandler
faulthandler.enable()





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

                    


#    print(corpus)
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
    with open('tweet_data/' + stock, 'r') as f:
            tweets = ast.literal_eval(f.read())
            '''
            batch_count = len(contents)/20
            for i in range(1,6):
                tweet_batch = {}
                start = int(batch_count*(i-1))
                end = int(batch_count*i)
                batch = contents[start:end] 
                tweet_batch(ast.literal_eval(batch))
                tweets.update(tweet_batch)
            '''
    # parse to 
    print(tweets)
    return tweets
#        with open('tweet_data/{}'.format(stock) as f:

    
def extract_features(tweet):
    ngram = {}
    for ngram_size in range(1,3):
        for idx,word in enumerate(tweet):
            phrase = tweet[idx:idx+ngram_size]
            #print(phrase)
            query = ' '.join(phrase)
            if query in corpus:
                ngram[query] = corpus[query]
    #print(ngram)
    return ngram
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
    if not os.path.exists('processed_data'):
        os.mkdir('processed_data')
        
    for key, tweet in tqdm(tweets.items()):
        #print(tweet)
        ngram = extract_features(tweet)
        if len(ngram) > 0:
            #print(ngram)
            total_valence = sum([int(i) for i in ngram.values()])
            data[total_valence] = tweet
            #print(data[total_valence])
            if len(data) == 100:
                print("saving batch of labelled data")
                with open('labelled_data/{}'.format(stock), 'a+') as f:
                    print(data)
                    json.dump(data, f)
                    ngrams.clear()
                    data.clear()


            
