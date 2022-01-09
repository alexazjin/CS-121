"""
CS 121: Analyzing Election Tweets
Zqian (Alexa) Jin
Analyze module
Functions to analyze tweets. 
Changes made since last submission:
1. removed instances of <boolean expression> == False
2. removed placeholder codes
3. used strip(PUNCTUATION) instead of using a loop to check for each punctuation mark
4. changed while loop to for loop in find_n_gram function
"""

import unicodedata
import sys

from basic_algorithms import find_top_k, find_min_count, find_salient, tf, idf
import math
from util import sort_count_pairs

##################### DO NOT MODIFY THIS CODE #####################

def keep_chr(ch):
    '''
    Find all characters that are classifed as punctuation in Unicode
    (except #, @, &) and combine them into a single string.
    '''
    return unicodedata.category(ch).startswith('P') and \
        (ch not in ("#", "@", "&"))

PUNCTUATION = " ".join([chr(i) for i in range(sys.maxunicode)
                        if keep_chr(chr(i))])

# When processing tweets, ignore these words
STOP_WORDS = ["a", "an", "the", "this", "that", "of", "for", "or",
              "and", "on", "to", "be", "if", "we", "you", "in", "is",
              "at", "it", "rt", "mt", "with"]

# When processing tweets, words w/ a prefix that appears in this list
# should be ignored.
STOP_PREFIXES = ("@", "#", "http", "&amp")


#####################  MODIFY THIS CODE #####################


############## Part 2 ##############

# Task 2.1

def count_entities(tweets, entity_desc):
    """ 
    Sort the corresponding entities 
    Inputs:
    tweets: a list of tweets
    entity_desc: a triple such as ("hashtags", "text", True),
          ("user_mentions", "screen_name", False), etc.
    outputs: a list of tuples (entity, counts) in dercreasing order of counts
     """
    (key, subkey, sensitivity) = entity_desc
    counts = {}
    for tweet in tweets:
        for x in tweet['entities'][key]:
            if not sensitivity:
                x[subkey] = x[subkey].lower()
            counts[x[subkey]] = counts.get(x[subkey], 0)
            counts[x[subkey]] += 1
    lst = []
    for token in counts:
        lst.append((token, counts[token]))
    ordered_lst = sort_count_pairs(lst)

    return ordered_lst


    
def find_top_k_entities(tweets, entity_desc, k):
    '''
    Find the k most frequently occuring entitites.
    Inputs:
        tweets: a list of tweets
        entity_desc: a triple such as ("hashtags", "text", True),
          ("user_mentions", "screen_name", False), etc.
        k: integer
    Returns: list of entities
    '''
    ordered_lst = count_entities(tweets, entity_desc)
    lst = []
    for x in ordered_lst:
        if len(lst) < k:
            lst.append(x[0])

    return lst


# Task 2.2
def find_min_count_entities(tweets, entity_desc, min_count):
    '''
    Find the entitites that occur at least min_count times.
    Inputs:
        tweets: a list of tweets
        entity_desc: a triple such as ("hashtags", "text", True),
          ("user_mentions", "screen_name", False), etc.
        min_count: integer
    Returns: set of entities
    '''
    ordered_lst = count_entities(tweets, entity_desc)
    output = set() 
    for entity in ordered_lst:
        if entity[1] >= min_count:
            output.add(entity[0])

    return output




############## Part 3 ##############

# Pre-processing step and representing n-grams

# YOUR HELPER FUNCTIONS HERE
def no_hash(word):
    """ 
    
     """
    long_enough = len(word) >= 4
    no_hash_at = word[0] != "#" and word[0] != "@"
    no_url = word[:4] != 'http' and word[:4] != "&amp"
    if no_hash_at:
        if long_enough:
            if no_url:
                return True
        else:
            return True
    return False

import string

def clean_text(text, case_sensitive, stop_word):
    """ 
    clean the text according to given criterions
    Inputs:
    text (string): a string
    case_sensitive (boolean): whether the function is case sensitive
    stop_word (boolean): whether stop words are removed
    Returns: a list of words (strings) processed according to the criterions
    """
    words = text.split() 
    cleaned_words = []
    for word in words:
        if not case_sensitive:
            word = word.lower()
        
        while word[0] in PUNCTUATION or word[-1] in PUNCTUATION:
            word = word.strip(PUNCTUATION)
            if word == '':
                break 

        if word != '':
            if no_hash(word):
                if stop_word:
                    if word not in STOP_WORDS:
                        cleaned_words.append(word)
                else:
                    cleaned_words.append(word)

    return cleaned_words

def find_n_gram(text, case_sensitive, stop_word, n):
    """ 
    Find all the n grams in a text
    Inputs:
    text (string): a string
    case_sensitive (boolean): whether it's case sensitive
    stop_word (boolean): whether stop words are removed
    n (int): n-gram
    Returns:
    a list of all the n-grams in tuples
    
     """
    cleaned_words = clean_text(text, case_sensitive, stop_word)
    output = []
    for i, word in enumerate(cleaned_words):
        if i <= len(cleaned_words) - n:
            lst = []
            for x in range(n):
                lst.append(cleaned_words[i])
                i +=1
            t = tuple(lst)
            output.append(t)

    return output


# Task 3.1
def find_top_k_ngrams(tweets, n, case_sensitive, k):
    '''
    Find k most frequently occurring n-grams.
    Inputs:
        tweets: a list of tweets
        n: integer
        case_sensitive: boolean
        k: integer
    Returns: list of n-grams
    '''
    all_n_grams= []
    for tweet in tweets:
        text = tweet['abridged_text']
        n_grams = find_n_gram(text, case_sensitive, True, n)
        all_n_grams += n_grams
    output = find_top_k(all_n_grams, k)

    return output 


# Task 3.2
def find_min_count_ngrams(tweets, n, case_sensitive, min_count):
    '''
    Find n-grams that occur at least min_count times.
    Inputs:
        tweets: a list of tweets
        n: integer
        case_sensitive: boolean
        min_count: integer
    Returns: set of n-grams
    '''
    all_n_grams= []
    for tweet in tweets:
        text = tweet['abridged_text']
        n_grams = find_n_gram(text, case_sensitive, True, n)
        all_n_grams += n_grams
    output = find_min_count(all_n_grams, min_count)

    return output


# Task 3.3

def find_salient_ngrams(tweets, n, case_sensitive, threshold):
    '''
    Compute the salient words for each document.  A word is salient if
    its tf-idf score is strictly above a given threshold.
    Inputs:
      docs: list of list of tokens
      threshold: float
    Returns: list of sets of salient words
    '''
    all_n_grams =[]
    for tweet in tweets:
        text = tweet['abridged_text']
        n_grams = find_n_gram(text, case_sensitive, False, n)
        all_n_grams.append(n_grams)
    
    lst = find_salient(all_n_grams, threshold)
    
    return lst
