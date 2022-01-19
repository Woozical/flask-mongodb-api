from math import cos, radians, sin, asin, sqrt

def validate_origin(origin:str):
  """
  Checks to see if the given string matches the expected format for the 'origin' query parameter.
  Returns True if the given string adheres to latitude, longitude format: comma separated
  numbers, in which the latitude is +/- 90 and the longitude is +/- 180. Returns False otherwise.

  >>> validate_origin("23.91231, -110.2343469")
  True

  >>> validate_origin("23.91, -110, 45")
  False

  >>> validate_origin("100.50, 50")
  False

  >>> validate_origin("45.69235, 200.123")
  False

  >>> validate_origin("23.91 -110.24")
  False

  >>> validate_origin("hello, world")
  False

  >>> validate_origin("550.23, twenty")
  False

  >>> validate_origin("23.91 -,110.24")
  False
  """
  
  nums = origin.split(",")
  if len(nums) != 2:
    return False
  
  if not (validate_num(nums[0]) and validate_num(nums[1])):
    return False

  lat = float(nums[0])
  long = float(nums[1])

  if ((lat > 90 or lat < -90) or (long > 180 or long < -180)):
    return False
  
  return True

def validate_num(num_str:str):
  """
  Checks to see if given string is castable to a numeric type
  Returns True / False
  >>> validate_num("0")
  True
  >>> validate_num("-1")
  True
  >>> validate_num("23.5123")
  True
  >>> validate_num("hello")
  False
  """
  try:
    float(num_str)
    return True
  except ValueError:
    return False

def coord_str_to_tuple(coord:str, lat_long=True):
  """ Converts a coordinate string (e.g. '23.56, 110.23') to a tuple. Optional parameter lat_long
      if the string is in (latitude, longitude) format (default), set to False is string is in (longitude, latitude) format.
      The function will always return a tuple in (longitude, latitude) format

      >>> coord_str_to_tuple("23.56, 110.23")
      (110.23, 23.56)
      >>> coord_str_to_tuple(coord="45.5, 67.9", lat_long=False)
      (45.5, 67.9)
  """
  if lat_long:
    lat, long = coord.split(",")
  else:
    long, lat = coord.split(",")
  
  return (float(long), float(lat))

def haversine_distance(origin, point, miles=True):
  """ Calculates the distance in miles (default) or kilometers from a given origin to a given point, using Haversine Formula.
      origin and point should be tuples in (long, lat) format

      >>> ('%.2f'%haversine_distance(origin=(2.2950, 48.8738), point=(2.3212, 48.8656), miles=False))
      '2.12'
  """
  #### Haversine Formula:
  #  dlon = lon2 - lon1
  #  dlat = lat2 - lat1
  #  a = sin^2(dlat/2) + cos(lat1) * cos(lat2) * sin^2(dlon/2)
  #  c = 2 * arcsin(min(1,sqrt(a)))
  #  d = R * c
  radius = 3956 if miles else 6367 # Radius of the earth, in miles (default) or kilometers

  # Convert degree long/lat to radians
  lon1, lat1 = [radians(p) for p in origin]
  lon2, lat2 = [radians(p) for p in point]

  # Apply Haversine Formula https://en.wikipedia.org/wiki/Haversine_formula
  delta_long = lon2 - lon1
  delta_lat = lat2 - lat1
  arc = (sin(delta_lat * 0.5) ** 2) + cos(lat1) * cos(lat2) * (sin(delta_long * 0.5) ** 2)
  circle_dist = 2 * asin(min(1, sqrt(arc)))
  distance = radius * circle_dist

  return distance