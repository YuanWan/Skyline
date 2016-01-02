import pymongo
from flask import Flask
from flask import render_template
from pymongo import MongoClient
import json
from bson import json_util
from bson.json_util import dumps
from flask import request
import frequentTools
from flask_socketio import SocketIO
import birdy
from birdy.twitter import UserClient


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

client = UserClient('Ghy8tbRezuJH0AtSL1qcPjqm8',
                    'bURQpyYNU7ZbPbZVLiCagInnbM4yZvK9hAFlhToLoZ3XjOCqSy',
                    '3220384082-tbVafpAHKF2OMyv3m68cUa1xLfTmJ8Riz6bry6l',
                    'Eb1LiineWIRngaOwju91tEV3cexAcJhvCoxW4dNJ5UQMu')


MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DBS_NAME = 'test'
# COLLECTION_NAME = 'projects'
# FIELDS = {'school_state': True, 'resource_type': True, 'poverty_level': True, 'time': True, 'total_donations': True, '_id': False}
connection = MongoClient(MONGODB_HOST, MONGODB_PORT)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/stats")
def stats():
    return render_template("stats.html")

@app.route("/gmonitor")
def gmonitor():
    return render_template("gmonitor.html")


@app.route('/api/frequent/', methods=['GET'])
def call_frequent():
    word_list=frequentTools.find_frequent_word()
    return render_template("word_cloud.html",word_list=json.dumps(word_list))


@app.route("/db/twitter")
def db_twitter():
    collection = connection[DBS_NAME]['twitter']
    twitters = collection.find(limit=10000).sort([('time', pymongo.DESCENDING)]);
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


@socketio.on('message', namespace='/sock')
def handle_message(message):
    print('received message: ' + message)


@socketio.on('my event', namespace='/sock')
def handle_my_custom_namespace_event(json):
    print('received json: ' + str(json))


@socketio.on('tracking', namespace='/sock')
def handle_message(tracking):
    response = client.stream.statuses.filter.post(track='twitter')
    for data in response.stream():
        socketio.emit('my response', data, broadcast=True)


@socketio.on('connect', namespace='/sock')
def test_connect():
    response = client.stream.statuses.filter.post(track='twitter')
    for data in response.stream():
        socketio.emit('my response', data, broadcast=True)


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')

if __name__ == "__main__":
    socketio.run(app)
    app.run(host='0.0.0.0',port=5000,debug=True)