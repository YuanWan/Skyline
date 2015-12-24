from flask import Flask
from flask import render_template
from pymongo import MongoClient
import json
from bson import json_util
from bson.json_util import dumps
from flask import request
import frequentTools

app = Flask(__name__)

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DBS_NAME = 'test'
# COLLECTION_NAME = 'projects'
# FIELDS = {'school_state': True, 'resource_type': True, 'poverty_level': True, 'date_posted': True, 'total_donations': True, '_id': False}
connection = MongoClient(MONGODB_HOST, MONGODB_PORT)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/stats")
def stats():
    return render_template("stats.html")


@app.route('/api/frequent/', methods=['GET'])
def call_frequent():
    word_list=frequentTools.find_frequent_word()
    return render_template("word_cloud.html",word_list=json.dumps(word_list))


@app.route("/db/twitter")
def db_twitter():
    collection = connection[DBS_NAME]['twitter']
    twitters = collection.find(limit=10000)
    #projects = collection.find(projection=FIELDS)
    json_twitters = []
    for twitter in twitters:
        json_twitters.append(twitter)
    json_twitters = json.dumps(json_twitters, default=json_util.default)
    connection.close()
    return json_twitters


@app.route("/db/news")
def db_news():
    collection = connection[DBS_NAME]['news']
    news = collection.find(limit=100)
    #projects = collection.find(projection=FIELDS)
    json_news = []
    for new in news:
        json_news.append(new)
    json_news = json.dumps(json_news, default=json_util.default)
    connection.close()
    return json_news

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)