# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 03:18:44 2016

@author: Florian
"""

import re

emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
 
regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r'(?:\$[\w_]+)', # $-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]
    
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)

def tokenize(s):
    return tokens_re.findall(s)
 
def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens
    
    
def update_occurence_matrix(matrix, terms):
    for i in range(len(terms)-1):
            for j in range(i+1, len(terms)):
                w1, w2 = sorted([terms[i], terms[j]])
                if w1 != w2:
                    matrix[w1][w2] += 1
                    
def create_probability_matrix(p_t,p_t_coms,c_matrix,count_all,n_docs):                    
    for term, n in count_all.items():
            p_t[term] = n/n_docs
            for t2 in c_matrix[term]:
                p_t_com[term][t2] = float(c_matrix[term][t2]) / float(n_docs)