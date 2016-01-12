import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import StreamListener
import json
import os
import operator 
import string
from collections import Counter

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import bigrams


execfile('H:/Dropbox/Dropbox/Code/Python/custom_tokenize.py')
execfile('H:/Dropbox/Dropbox/Code/Python/custom_tweepy.py')


consumer_key = 'ju00Vnyb5lFOwmuOMCNN6E5t0'
consumer_secret = 'rbTES9x0sfWkgIiFncmcdaWW0FZzrzmA7gFpUE01FsN3Oygf8d'
access_token = '43913055-KxAWZNwrywP3ap21xafbY336AzPe8ODeEfumZt5CA'
access_secret = '65wuDUe9ZWyVmo4Mwd5fuyztGAFMBCNKNv5xcnzpi6QCs'
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth, wait_on_rate_limit  = True, wait_on_rate_limit_notify=True)

tweet_file_path = 'H:/Downloads/tmp/es.json'
download_tweets(api, tweet_file_path, 'w', '$ES','2016-01-01','2016-01-10', 1000)

punctuation = list(string.punctuation)
stop = set(stopwords.words('english') + stopwords.words('french') +  punctuation + ['rt', 'via', 'RT'+ ''])
with open(tweet_file_path, 'r') as f:
    count_all = Counter()
    count_bigrams = Counter()
    for line in f:
        tweet_json = json.loads(line)
        #print tweet_json['text']
        tweet = preprocess(tweet_json['text'].lower())
        
        terms_stop = [term for term in tweet if term not in stop and
              not term.startswith(('#', '@','$')) and 
              not len(term.encode('ascii','ignore')) == 0]
        terms_bigram = bigrams(terms_stop)
        count_all.update(terms_stop)
        count_bigrams.update(terms_bigram)
        
    print(count_all.most_common(50))
    #print(count_bigrams.most_common(50))    
f.close()
