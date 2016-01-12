import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import StreamListener
import json
import os
import operator 
import string
from collections import Counter
from collections import defaultdict

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import bigrams


execfile('H:/Dropbox/Dropbox/Code/Python/tweepy/custom_tokenize.py')
execfile('H:/Dropbox/Dropbox/Code/Python/tweepy/custom_tweepy.py')


consumer_key = 'ju00Vnyb5lFOwmuOMCNN6E5t0'
consumer_secret = 'rbTES9x0sfWkgIiFncmcdaWW0FZzrzmA7gFpUE01FsN3Oygf8d'
access_token = '43913055-KxAWZNwrywP3ap21xafbY336AzPe8ODeEfumZt5CA'
access_secret = '65wuDUe9ZWyVmo4Mwd5fuyztGAFMBCNKNv5xcnzpi6QCs'
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth, wait_on_rate_limit  = True, wait_on_rate_limit_notify=True)

n_docs = 1000
tweet_file_path = 'H:/Dropbox/Dropbox/Code/Python/tweepy/data/es.json'
download_tweets(api, tweet_file_path, 'w', '$ES','2016-01-01','2016-01-10', n_docs)

punctuation = list(string.punctuation)
stop = set(stopwords.words('english') + stopwords.words('french') +  punctuation + ['rt', 'via', 'RT'+ ''])
with open(tweet_file_path, 'r') as f:
    
    count_all = Counter()
    count_bigrams = Counter()
    c_matrix = defaultdict(lambda: defaultdict(int))
    
    for line in f:
        tweet_json = json.loads(line)
        #print tweet_json['text']
        tweet = preprocess(tweet_json['text'].lower())
        
        terms_stop = [term for term in tweet if term not in stop and
              not term.startswith(('#', '@','$')) and 
              not len(term.encode('ascii','ignore')) == 0]
        terms_bigram = bigrams(terms_stop)
        update_occurence_matrix(c_matrix, terms_stop)
        count_all.update(terms_stop)
        count_bigrams.update(terms_bigram)        
        
    p_t = {}
    p_t_com = defaultdict(lambda: defaultdict(float))
    for term, n in count_all.items():
        p_t[term] = n/n_docs
        for t2 in c_matrix[term]:
            print c_matrix[term][t2]
            p_t_com[term][t2] = float(c_matrix[term][t2]) / float(n_docs)
            
        
        
        
    print(count_all.most_common(50))
    #print(count_bigrams.most_common(50))    
f.close()
