import flask
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
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import apiTools
import analytics
import math

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'doc', 'docx'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
msgpool = []

access_token = "3220384082-tbVafpAHKF2OMyv3m68cUa1xLfTmJ8Riz6bry6l"
access_token_secret = "Eb1LiineWIRngaOwju91tEV3cexAcJhvCoxW4dNJ5UQMu"
consumer_key = "Ghy8tbRezuJH0AtSL1qcPjqm8"
consumer_secret = "bURQpyYNU7ZbPbZVLiCagInnbM4yZvK9hAFlhToLoZ3XjOCqSy"


class StdOutListener(StreamListener):
    def on_data(self, data):
        # socketio.emit('message', {'msg': data})
        # trigger_msg(data)
        d = json.loads(data)
        if d.get("text") is not None:
            print(data)
            analyzer = TextBlob(d.get("text"))
            d['analyzer'] = analyzer.sentiment
            score = analyzer.sentiment[0] * analyzer.sentiment[1]
            d['score'] = score
            user = d.get("user")
            follower = user.get("followers_count", 0)
            favorite_count = d.get("favorite_count", 0)
            impact_factor = (1 + follower / 100 + favorite_count)
            impact_size = math.log(impact_factor + 1, 10)
            d['impact_size'] = impact_size
            if d.get("coordinates") is not None:
                print(d.get("coordinates"))
            if d.get("place") is not None:
                print(d.get("place.full_name"))
            global msgpool
            msgpool.append(json.dumps(d))
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


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/election")
def election():
    word_list = frequentTools.find_frequent_word()
    return render_template("election.html", word_list=json.dumps(word_list))


@app.route("/case")
def case():
    return render_template("case.html")


@app.route("/newspaper/<stackname>")
def newspaper(stackname):
    return render_template("newspaper.html", stackname=stackname)


@app.route("/upload")
def upload():
    return render_template("stats.html")


@app.route("/quick")
def quick_analysis():
    return render_template("quick.html")


@app.route("/map")
def gmonitor():
    # This handles Twitter authetification and the connection to Twitter Streaming API

    l = StdOutListener()
    global msgpool
    msgpool = []
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    streamfire = stream.filter(track=['selfie'], async=True)
    return render_template("gmonitor.html")


@app.route('/api/frequent/', methods=['GET'])
def call_frequent():
    word_list = frequentTools.find_frequent_word()
    return render_template("word_cloud.html", word_list=json.dumps(word_list))


@app.route('/api/election_frequent/<candidate>', methods=['GET'])
def call_election_frequent(candidate):
    word_list = frequentTools.candidate_frequent_word(candidate)
    return json.dumps(word_list)


@app.route('/api/trends_us/', methods=['GET'])
def trends_us():
    result = apiTools.trends_us()
    return json.dumps(result)


@app.route('/api/trends_sg/', methods=['GET'])
def trends_sg():
    result = apiTools.trends_sg()
    return json.dumps(result)


@app.route('/api/trends_global/', methods=['GET'])
def trends_global():
    result = apiTools.trends_global()
    return json.dumps(result)


@app.route('/api/quick/', methods=['POST'])
def quick_service():
    type = request.form['type']
    text = None
    if type == "text":
        text = request.form['content']
    if type == "url":
        url = request.form['url']
    word_list = frequentTools.quick(text)

    analyzer_pa = TextBlob(text)
    # analyzer_nb = TextBlob(text, analyzer=NaiveBayesAnalyzer())
    print(analyzer_pa.sentiment)
    # print(analyzer_nb.sentiment)
    sentiments = {
        "pa_polarity": analyzer_pa.sentiment.polarity,
        "pa_subjectivity": analyzer_pa.sentiment.subjectivity,
        "score": analyzer_pa.sentiment.polarity * analyzer_pa.sentiment.subjectivity
        # "nb_classification":analyzer_nb.sentiment.classification,
        # "nb_p_pos":analyzer_nb.sentiment.p_pos,
        # "nb-p_neg":analyzer_nb.sentiment.p_neg
    }
    word_list.append(sentiments)
    quick_result = json.dumps(word_list)
    return quick_result;


@app.route('/api/frequent_news/', methods=['GET'])
def call_frequent_news():
    word_list = frequentTools.find_frequent_word()
    return render_template("word_cloud.html", word_list=json.dumps(word_list))


@app.route('/test/coor', methods=['GET'])
def test_coor():
    coor = [2.34321, 5.3454]
    json_coor = json.dumps(coor, default=json_util.default)
    return json_coor


@app.route("/db/twitter")
def db_twitter():
    collection = connection[DBS_NAME]['twitter']
    twitters = collection.find(limit=10000).sort([('time', pymongo.DESCENDING)]);
    # projects = collection.find(projection=FIELDS)
    json_twitters = []
    for twitter in twitters:
        json_twitters.append(twitter)
    json_twitters = json.dumps(json_twitters, default=json_util.default)
    connection.close()
    return json_twitters


@app.route("/db/news/<stackname>")
def db_news(stackname):
    collection = connection['news'][stackname]
    news = collection.find(limit=100)
    # projects = collection.find(projection=FIELDS)
    json_news = []
    for new in news:
        json_news.append(new)
    json_news = json.dumps(json_news, default=json_util.default)
    connection.close()
    return json_news


@app.route("/db/article/<stackname>/<link_hash>")
def db_article(stackname, link_hash):
    collection = connection['news'][stackname]
    news = collection.find({"link_hash": link_hash})
    # projects = collection.find(projection=FIELDS)
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
    msgpool = []
    return json_pool


@app.route("/election_api/total")
def election_api_total():
    total = analytics.total_data()
    result = {
        "total": total
    }
    json_result = json.dumps(result, default=json_util.default)
    return json_result


@app.route("/election_api/impact")
def election_api_impact():
    impact = analytics.impact()
    json_response = json.dumps(impact)
    return json_response


@app.route("/election_api/impact_60000")
def election_api_impact_60000():
    impact = analytics.impact_60000()
    json_response = json.dumps(impact)
    return json_response


@app.route("/election_api/impact_240000")
def election_api_impact_240000():
    impact = analytics.impact_240000()
    json_response = json.dumps(impact)
    return json_response


@app.route("/election_api/impact_week")
def election_api_impact_lastweek():
    impact = analytics.impact_lastweek()
    json_response = json.dumps(impact)
    return json_response


@app.route("/election_api/impact_last3day")
def election_api_impact_last3day():
    impact = analytics.impact_last3day()
    json_response = json.dumps(impact)
    return json_response


@app.route("/election_api/impact_lastday")
def election_api_impact_lastday():
    impact = analytics.impact_lastday()
    json_response = json.dumps(impact)
    return json_response


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
    emit('status', {'msg': ' has left the room.'})


def trigger_msg(msg):
    sock(msg)


if __name__ == "__main__":
    socketio.run(app)
    app.run(host='0.0.0.0', port=5000, debug=True)
