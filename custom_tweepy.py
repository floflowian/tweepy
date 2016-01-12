# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 13:28:47 2016

@author: Florian
"""

import time
from datetime import date

def download_tweets(api,path, mode, search_terms, start_date, end_date = date.today().strftime("%Y-%m-%d"), limit = 100 ):
    f = open(path, mode)
    for tweet in tweepy.Cursor(api.search,q=search_terms,since=start_date,until=end_date).items(limit):
        print json.dumps(tweet._json)
        f.write(json.dumps(tweet._json))
        f.write('\n')
    f.close()
