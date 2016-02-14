from pymongo import MongoClient
import datetime
from bson.code import Code


MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DBS_NAME = 'twitter'
COLLECTION_NAME = 'election'
# FIELDS = {'school_state': True, 'resource_type': True, 'poverty_level': True, 'time': True, 'total_donations': True, '_id': False}
connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
collection = connection[DBS_NAME][COLLECTION_NAME]


def total_data():
    return collection.count()

def impact_hour():
    result=collection.aggregate([
     {
       '$group':
         {
           "_id":"$candidate","impact":{"$sum":"$impact"},"score":{"$sum":"$score"},"volume":{"$sum":1}
         }
     }
   ])
    for document in result:
        print(document)

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


impact_hour()