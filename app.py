import pymongo
from flask import Flask
from flask import render_template
from pymongo import MongoClient
import json
from bson import json_util
from bson.json_util import dumps
from flask import request
import frequentTools
from flask import session
from flask.ext.socketio import emit, join_room, leave_room
from flask_socketio import SocketIO
import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream





app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
msgpool=[]


access_token = "3220384082-tbVafpAHKF2OMyv3m68cUa1xLfTmJ8Riz6bry6l"
access_token_secret = "Eb1LiineWIRngaOwju91tEV3cexAcJhvCoxW4dNJ5UQMu"
consumer_key = "Ghy8tbRezuJH0AtSL1qcPjqm8"
consumer_secret = "bURQpyYNU7ZbPbZVLiCagInnbM4yZvK9hAFlhToLoZ3XjOCqSy"

class StdOutListener(StreamListener):
    def on_data(self, data):
        # socketio.emit('message', {'msg': data})
        # trigger_msg(data)
        global msgpool
        msgpool.append(data)
        print(data)
        return True
    def on_error(self, status):
        print(status)


class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print(status.text)


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

@app.route("/sock")
def gmonitor():
    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    global msgpool
    msgpool = []
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    streamfire = stream.filter(track=['python', 'javascript', 'ruby'], async=True)
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


@app.route("/db/pool")
def db_pool():
    global msgpool
    json_pool = []
    for msg in msgpool:
        json_pool.append(msg)
    json_pool = json.dumps(json_pool, default=json_util.default)
    msgpool=[]
    return json_pool


# @socketio.on('message', namespace='/sock')
# def handle_message(message):
#     print('received message: ' + message)


# @socketio.on('my event', namespace='/sock')
# def handle_my_custom_namespace_event(json):
#     print('received json: ' + str(json))




# @socketio.on('connect', namespace='/sock')
# def test_connect():
#     socketio.emit('listening',{})

#
# @socketio.on('tracking', namespace='/sock')
# def tracking():
#     socketio.emit('my response','sdfsdfsdf')
#
#
# @socketio.on('disconnect', namespace='/test')
# def test_disconnect():
#     print('Client disconnected')


@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    # room = session.get('room')
    # join_room(room)
    emit('status', {'msg': ' has entered the room.'})


@socketio.on('text', namespace='/chat')
def sock(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    # room = session.get('room')
    emit('message', {'msg': ':' + message['msg']})


@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    # A status message is broadcast to all people in the room."""
    # room = session.get('room')
    # leave_room(room)
    emit('status', {'msg':  ' has left the room.'})


def trigger_msg(msg):
    sock(msg)


if __name__ == "__main__":
    # from gevent import monkey
    # monkey.patch_all()
    # stream = Stream(auth, l)
    # streamfire = stream.filter(track=['python', 'javascript', 'ruby'], async=True)
    socketio.run(app)
    app.run(host='0.0.0.0',port=5000,debug=True)