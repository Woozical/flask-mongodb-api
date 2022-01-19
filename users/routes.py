from flask import request, jsonify
from app import app
from users.models import User
from utils import validate_num, validate_origin

@app.route("/users")
def users_find():
  args = validate_and_type_args(request)
  users = User.find(args)
  response_obj = {
    "metadata": {
      "path": "/users",
      "page": args.get("page", 0),
      "query": args
    },
    "num_results" : len(users),
    "results": [User.db_user_to_geoJSON(user) for user in users]
  }
  return jsonify(response_obj)


def validate_and_type_args(request):
  """ Typecasts query params on the request object to their expected types, ignoring unsupported or invalid arguments """
  typed_args = dict()
  
  if "fav_color" in request.args:
    typed_args["fav_color"] = request.args["fav_color"]
  
  if "dist" in request.args and validate_num(request.args["dist"]):
    typed_args["dist"] = int(request.args["dist"])
  
  if "origin" in request.args and validate_origin(request.args["origin"]):
    typed_args["origin"] = request.args["origin"]
  
  if "min_age" in request.args and validate_num(request.args["min_age"]):
    typed_args["min_age"] = int(request.args["min_age"])
  
  if "max_age" in request.args and validate_num(request.args["max_age"]):
    typed_args["max_age"] = int(request.args["max_age"])
  
  if "page" in request.args and validate_num(request.args["page"]):
    typed_args["page"] = int(request.args["page"])

  return typed_args