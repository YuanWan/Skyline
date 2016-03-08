import json

import math
from bson import json_util, ObjectId
from pymongo import MongoClient
import datetime
from bson.code import Code
from datetime import date
from datetime import timedelta


MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DBS_NAME = 'twitter'
COLLECTION_NAME = 'election'
# FIELDS = {'school_state': True, 'resource_type': True, 'poverty_level': True, 'time': True, 'total_donations': True, '_id': False}
connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
collection = connection[DBS_NAME][COLLECTION_NAME]

candidates=['Trump','Clinton','Sanders','Cruz','Bush','Carson','Kasich','Rubio']


def total_data():
    return collection.count()

epoch = datetime.datetime.utcfromtimestamp(0)

def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0


def objectIdWithTimestamp(timestamp):
    # Convert string date to Date object (otherwise assume timestamp is a date)
    if isinstance(timestamp, str):
        timestamp =  datetime.datetime.strptime(timestamp,"YYYY/MM/DD")

    # Convert date object to hex seconds since Unix epoch
    hexSeconds = hex(math.floor(unix_time_millis(timestamp)/1000))[2:];

    # Create an ObjectId with that hex timestamp
    constructedObjectId = ObjectId(hexSeconds + "0000000000000000");
    return constructedObjectId



def impact_60000():
    result=collection.aggregate([
        {'$sort': {'_id':-1}},
        {'$limit' : 60000 },
     {
       '$group':
         {
           "_id":"$candidate","impact":{"$sum":"$impact"},"score":{"$sum":"$score"},"volume":{"$sum":1}
         }
     }
   ])
    data = {}
    for document in result:
        temp={candidates[document.get('_id')]:{'score':document.get('score'),'impact':document.get('impact'),'volume':document.get('volume')}}
        data.update(temp)
    return data


def impact_240000():
    result=collection.aggregate([
        {'$sort': {'_id':-1}},
        {'$limit' : 240000 },
     {
       '$group':
         {
           "_id":"$candidate","impact":{"$sum":"$impact"},"score":{"$sum":"$score"},"volume":{"$sum":1}
         }
     }
   ])
    data = {}
    for document in result:
        temp={candidates[document.get('_id')]:{'score':document.get('score'),'impact':document.get('impact'),'volume':document.get('volume')}}
        data.update(temp)
    return data



def impact():
    result=collection.aggregate([
        {'$sort': {'_id':-1}},
        {'$limit' : 2000000 },
     {
       '$group':
         {
           "_id":"$candidate","impact":{"$sum":"$impact"},"score":{"$sum":"$score"},"volume":{"$sum":1}
         }
     }
   ])
    data = {}
    for document in result:
        temp={candidates[document.get('_id')]:{'score':document.get('score'),'impact':document.get('impact'),'volume':document.get('volume')}}
        data.update(temp)
    return data


def impact_lastweek():
    timenow = datetime.datetime.now()
    last_week = timenow - timedelta(days=7)
    result=collection.aggregate([
        {'$match':{ '_id': { '$gt': objectIdWithTimestamp(last_week) } }},
     {
       '$group':
         {
           "_id":"$candidate","impact":{"$sum":"$impact"},"score":{"$sum":"$score"},"volume":{"$sum":1}
         }
     }
   ])
    data = {}
    for document in result:
        temp={candidates[document.get('_id')]:{'score':document.get('score'),'impact':document.get('impact'),'volume':document.get('volume')}}
        data.update(temp)
    return data


def impact_last3day():
    timenow = datetime.datetime.now()
    last_day = timenow - timedelta(days=3)
    result=collection.aggregate([
        {'$match':{ '_id': { '$gt': objectIdWithTimestamp(last_day) } }},
     {
       '$group':
         {
           "_id":"$candidate","impact":{"$sum":"$impact"},"score":{"$sum":"$score"},"volume":{"$sum":1}
         }
     }
   ])
    data = {}
    for document in result:
        temp={candidates[document.get('_id')]:{'score':document.get('score'),'impact':document.get('impact'),'volume':document.get('volume')}}
        data.update(temp)
    return data


def impact_lastday():
    timenow = datetime.datetime.now()
    last_day = timenow - timedelta(days=1)
    result=collection.aggregate([
        {'$match':{ '_id': { '$gt': objectIdWithTimestamp(last_day) } }},
     {
       '$group':
         {
           "_id":"$candidate","impact":{"$sum":"$impact"},"score":{"$sum":"$score"},"volume":{"$sum":1}
         }
     }
   ])
    data = {}
    for document in result:
        temp={candidates[document.get('_id')]:{'score':document.get('score'),'impact':document.get('impact'),'volume':document.get('volume')}}
        data.update(temp)
    return data



# No use for now
def last_hour():
    mapper = Code("""
               function () {
                 this.tags.forEach(function(z) {
                   emit(z, 1);
                 });
               }
               """)
    reducer = Code("""
                function (key, values) {
                  var total = 0;
                  for (var i = 0; i < values.length; i++) {
                    total += values[i];
                  }
                  return total;
                }
                """)
    result = collection.map_reduce(mapper, reducer, "myresults",{"candidates.Trump":1})
    for doc in result.find():
        print(doc)



# timenow = datetime.datetime.now()
# last_week = timenow - timedelta(days=7)
# print(last_week)
# collection.find({ '_id': { '$gt': objectIdWithTimestamp(last_week) } });