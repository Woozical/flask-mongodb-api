from app import mongo
from utils import haversine_distance, coord_str_to_tuple


class User:
  @staticmethod
  def find(args:dict):
    RESULTS_PER_PAGE = 5
    # Convert our query arguments to MongoDB filters
    expected = 1 if "page" in args else 0 # args must have 1 k:v pair, not counting page argument, to warrant a mongo query
    mongo_filters = { "$and": [] } if (len(args) > expected) else {}
    
    if "fav_color" in args:
      mongo_filters["$and"].append({ "fav_color": { "$eq": args["fav_color"] } })
    if "min_age" in args:
      mongo_filters["$and"].append({ "age": { "$gte": args["min_age"] } })
    if "max_age" in args:
      mongo_filters["$and"].append({ "age": { "$lte": args["max_age"] } })
    
    page = args.get("page", 0)

    # Convert db result to list
    users = [user for user in mongo.db.users.find(mongo_filters).limit(RESULTS_PER_PAGE).skip(page * RESULTS_PER_PAGE)]

    ### Here we have some options regarding the distance filter, I'm not sure which functionality is desired
    if ("dist" in args and "origin" in args):
      origin = coord_str_to_tuple(args["origin"])
      max_dist = args["dist"]

      # A) Filter out users who's latest location history is beyond our distance filter, or who have no location history
      working_users = []
      for user in users:
        if (user.get("loc_history")):
          latest = len(user["loc_history"]) - 1 # This assumes latest location is stored last in DB document, if first, use 0 as idx
          point = (float(user["loc_history"][latest]["long"]),  float(user["loc_history"][latest]["lat"]))
          distance = haversine_distance(origin, point)
          if (distance <= max_dist) :
            working_users.append(user)
      users = working_users
      
      # B) Filter out location history features on users if that point is beyond our distance filter
      # for user in users:
      #   user["loc_history"] = [
      #     loc for loc in user["loc_history"]
      #     if (haversine_distance(origin, ( float(loc["long"]), float(loc["lat"]) )) <= max_dist)
      #   ]
    return users

  @staticmethod
  def db_user_to_geoJSON(db_user):
    """ Converts a user dict that is the result of a MongoDB query into GeoJSON format"""
    features = []
    for loc in db_user.get("loc_history", []):
      feature = {
        "type": "Feature",
        "properties": {},
        "geometry": {}
      }

      if ("name" in loc):
        feature["properties"] = {
          "city": loc["name"]
        }
      
      if ("long" in loc and "lat" in loc):
        feature["geometry"] = {
          "type": "Point",
          "coordinates": [float(loc["long"]), float(loc["lat"])]
        }

      features.append(feature)

    return {
      "type": "user",
      "locationHistory" : {
        "type": "FeatureCollection",
        "features": features
      },
      "properties": {
        "id": db_user["_id"],
        "name": db_user.get("name"),
        "age": db_user.get("age"),
        "fav_color": db_user.get("fav_color")
      }
    }