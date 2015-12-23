import nltk
from pymongo import MongoClient
import json
from bson import json_util
from collections import Counter
import re

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DBS_NAME = 'test'
connection = MongoClient(MONGODB_HOST, MONGODB_PORT)


def find_frequent_word():
    result = []
    collection = connection[DBS_NAME]['twitter']
    twitters = collection.find({}, {'text': 1, '_id': 0}, limit=10000)
    for twitter in twitters:
        result.append(twitter.get('text'))
    # json_twitters = []
    # for twitter in twitters:
    #     json_twitters.append(twitter)
    # json_twitters = json.dumps(json_twitters, default=json_util.default)
    # nltk.data.path.append('./nltk_data/')  # set the path
    # tokens = nltk.word_tokenize(json_twitters)
    # text = nltk.Text(tokens)
    # nonPunct = re.compile('.*[A-Za-z].*')
    # raw_words = [w for w in text if nonPunct.match(w)]
    # raw_word_count = Counter(raw_words)
    str1 = ''.join(str(e) for e in result)
    connection.close()
    return str1;