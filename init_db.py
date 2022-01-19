''' Initializes the local MongoDB with a collection "users" '''

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
## The name of our Mongo database we will be using is defined here
DB_NAME = "rithm_challenge"
###################################################################
db = client[DB_NAME]

db.users.insert_many([
  {"_id": 1, "name": "Taylor Swift", "age": 27, "fav_color": "red", "loc_history": [
    {"name": "San Francisco", "lat": "37.774929", "long": "-122.419416"},
    {"name": "Oakland", "lat": "37.8044", "long": "-122.2711"}
  ]},
  {"_id": 2, "name": "Idris Elba", "age": 58, "fav_color": "green", "loc_history": [
    {"name": "Washington-DC", "lat": "38.89565", "long": "-76.943174"}
  ]},
  {"_id": 3, "name": "Emma Watson", "age": 28, "fav_color": "blue", "loc_history": [
    {"name": "Los Angeles", "lat": "34.062264", "long": "-118.340361"},
    {"name": "Daly City", "lat": "37.68941", "long": "-122.462532"}
  ]},
  {"_id": 4, "name": "Emilia Clarke", "age": 30, "fav_color": "magenta", "loc_history": [
    {"name": "Los Angeles", "lat": "34.043566", "long": "-118.391092"}
  ]},
  {"_id": 5, "name": "Chris Martin", "age": 40, "fav_color": "green", "loc_history": [
    {"name": "Whitestone, UK", "lat": "0", "long": "0"}
  ]}
])

client.close()