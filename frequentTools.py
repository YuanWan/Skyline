import nltk
from pymongo import MongoClient
import json
from bson import json_util
from collections import Counter
import re
from nltk.corpus import stopwords

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DBS_NAME = 'test'
connection = MongoClient(MONGODB_HOST, MONGODB_PORT)


def find_frequent_word():
    default_stopwords = set(nltk.corpus.stopwords.words('english'))
    # We're adding some on our own - could be done inline like this...
    custom_stopwords = set(('price', '/', 'charts','\'s','\\','\"',"''",'rt','inc.','...','--'))
    # ... but let's read them from a file instead (one stopword per line, UTF-8)
    # stopwords_file = './stopwords.txt'
    # custom_stopwords = set(codecs.open(stopwords_file, 'r', 'utf-8').read().splitlines())

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

    # Stemming words seems to make matters worse, disabled
    # stemmer = nltk.stem.snowball.SnowballStemmer('german')
    # words = [stemmer.stem(word) for word in words]

    # Remove stopwords
    words = [word for word in words if word not in all_stopwords]

    # Calculate frequency distribution
    fdist = nltk.FreqDist(words)

    # Output top 50 words

    # for word, frequency in fdist.most_common(50):
    #     print('%s;%d' % (word, frequency)).encode('utf-8')

    str2 = ' + '.join(str(word) for word, frequency in fdist.most_common(100))

    #str2 = ''.join(str(e) for e in raw_words)

    connection.close()
    return str2;