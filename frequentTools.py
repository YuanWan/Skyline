import nltk
from pymongo import MongoClient
import json
from bson import json_util
from collections import Counter
import re
from nltk.corpus import stopwords
import codecs
import os

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DBS_NAME = 'test'
connection = MongoClient(MONGODB_HOST, MONGODB_PORT)


def find_frequent_word():
    default_stopwords = set(nltk.corpus.stopwords.words('english'))
    # We're adding some on our own - could be done inline like this...
    #custom_stopwords = set(('price', '/', 'charts','\'s','\\','\"',"''",'rt','inc.','...','--'))
    # ... but let's read them from a file instead (one stopword per line, UTF-8)
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    rel_path = "stopwords.txt"
    stopwords_file = os.path.join(script_dir, rel_path)
    custom_stopwords = set(codecs.open(stopwords_file, 'r', 'utf-8').read().splitlines())

    all_stopwords = default_stopwords | custom_stopwords

    result = []
    collection = connection[DBS_NAME]['twitter']
    twitters = collection.find({}, {'text': 1, '_id': 0}, limit=500000)
    for twitter in twitters:
        result.append(twitter.get('text'))
    str1 = ' '.join(str(e) for e in result)
    nltk.data.path.append('./nltk_data/')  # set the path
    words = nltk.word_tokenize(str1)

    # Remove single-character tokens (mostly punctuation)
    words = [word for word in words if len(word) > 1]

    # Remove numbers
    words = [word for word in words if not word.isnumeric()]

    # Lowercase all words (default_stopwords are lowercase too)
    words = [word.lower() for word in words]

    # TODO: remove punctuation
    punctuation = re.compile(r'[-+.?!\\/,":;()|0-9]')
    words = [punctuation.sub("", word) for word in words]

    # Stemming words seems to make matters worse, disabled
    # stemmer = nltk.stem.snowball.SnowballStemmer('english')
    # words = [stemmer.stem(word) for word in words]

    # Remove stopwords
    words = [word for word in words if word not in all_stopwords]

    # Calculate frequency distribution
    fdist = nltk.FreqDist(words)

    # Output top 100 words
    word_list=[]
    for word, frequency in fdist.most_common(100):
        data = {}
        data['text'] = word
        data['weight'] = frequency
        word_list.append(data)

    #str2 = ' + '.join(str(word) for word, frequency in fdist.most_common(100))

    connection.close()
    return word_list;

def single_news_frequent_word(stackname,link_hash):
    default_stopwords = set(nltk.corpus.stopwords.words('english'))
    # We're adding some on our own - could be done inline like this...
    #custom_stopwords = set(('price', '/', 'charts','\'s','\\','\"',"''",'rt','inc.','...','--'))
    # ... but let's read them from a file instead (one stopword per line, UTF-8)
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    rel_path = "stopwords.txt"
    stopwords_file = os.path.join(script_dir, rel_path)
    custom_stopwords = set(codecs.open(stopwords_file, 'r', 'utf-8').read().splitlines())

    all_stopwords = default_stopwords | custom_stopwords

    result = []
    collection = connection['news'][stackname]
    news = collection.find({"link_hash":link_hash})
    for article in news:
        result.append(article.get('text'))
    str1 = ' '.join(str(e) for e in result)
    nltk.data.path.append('./nltk_data/')  # set the path
    words = nltk.word_tokenize(str1)

    # Remove single-character tokens (mostly punctuation)
    words = [word for word in words if len(word) > 1]

    # Remove numbers
    words = [word for word in words if not word.isnumeric()]

    # Lowercase all words (default_stopwords are lowercase too)
    words = [word.lower() for word in words]

    # TODO: remove punctuation
    punctuation = re.compile(r'[-+.?!\\/,":;()|0-9]')
    words = [punctuation.sub("", word) for word in words]

    # Stemming words seems to make matters worse, disabled
    # stemmer = nltk.stem.snowball.SnowballStemmer('english')
    # words = [stemmer.stem(word) for word in words]

    # Remove stopwords
    words = [word for word in words if word not in all_stopwords]

    # Calculate frequency distribution
    fdist = nltk.FreqDist(words)

    # Output top 100 words
    word_list=[]
    for word, frequency in fdist.most_common(100):
        data = {}
        data['text'] = word
        data['weight'] = frequency
        word_list.append(data)

    #str2 = ' + '.join(str(word) for word, frequency in fdist.most_common(100))

    connection.close()
    return word_list;


def quick(text):
    if text is None:
        return

    default_stopwords = set(nltk.corpus.stopwords.words('english'))
    # We're adding some on our own - could be done inline like this...
    #custom_stopwords = set(('price', '/', 'charts','\'s','\\','\"',"''",'rt','inc.','...','--'))
    # ... but let's read them from a file instead (one stopword per line, UTF-8)
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    rel_path = "stopwords.txt"
    stopwords_file = os.path.join(script_dir, rel_path)
    custom_stopwords = set(codecs.open(stopwords_file, 'r', 'utf-8').read().splitlines())

    all_stopwords = default_stopwords | custom_stopwords

    nltk.data.path.append('./nltk_data/')  # set the path
    words = nltk.word_tokenize(text)

    # Remove single-character tokens (mostly punctuation)
    words = [word for word in words if len(word) > 1]

    # Remove numbers
    words = [word for word in words if not word.isnumeric()]

    # Lowercase all words (default_stopwords are lowercase too)
    words = [word.lower() for word in words]

    # TODO: remove punctuation
    punctuation = re.compile(r'[-+.?!\\/,":;()|0-9]')
    words = [punctuation.sub("", word) for word in words]

    # Stemming words seems to make matters worse, disabled
    # stemmer = nltk.stem.snowball.SnowballStemmer('english')
    # words = [stemmer.stem(word) for word in words]

    # Remove stopwords
    words = [word for word in words if word not in all_stopwords]

    # Calculate frequency distribution
    fdist = nltk.FreqDist(words)

    # Output top 100 words
    word_list=[]
    for word, frequency in fdist.most_common(100):
        data = {}
        data['text'] = word
        data['weight'] = frequency
        word_list.append(data)

    #str2 = ' + '.join(str(word) for word, frequency in fdist.most_common(100))

    connection.close()
    return word_list;