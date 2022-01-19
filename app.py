from flask_pymongo import PyMongo
from flask import Flask, jsonify, request

app = Flask(__name__)

## MongoDB setup
app.config["MONGO_URI"] = "mongodb://localhost:27017/rithm_challenge"
mongo = PyMongo(app)

@app.route("/")
def home_route():
  return jsonify(message="Welcome to the API") 


import users.routes
