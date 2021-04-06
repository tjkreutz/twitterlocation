import tweepy

def get_address_component(search, level="country"):
    names = []
    for result in search:
        for component in result["address_components"]:
            if component["types"][0] == level and component["types"][1] == "political":
                names.append(component["long_name"])
    if not names:
        return "UNK"
    return max(set(names), key = names.count) 

def from_latlon(lat, lon, gmaps):
    search = gmaps.reverse_geocode((lat, lon))
    return search

def from_coordinates(coordinates, gmaps):
    lon, lat = coordinates['coordinates']
    search = from_latlon(lat, lon, gmaps)
    return search

def from_place(place, gmaps):
    bbox = place.bounding_box.coordinates
    lat = bbox[0][0][1]
    lon = bbox[0][0][0]
    search = from_latlon(lat, lon, gmaps)
    return search

def from_location(location, gmaps):
    search = gmaps.places(query=location)
    if search["status"] == "OK":
        result = search["results"][0]
        lat = result["geometry"]["location"]["lat"]
        lon = result["geometry"]["location"]["lng"]
        return from_latlon(lat, lon, gmaps)

def from_followers(followers, gmaps):
    search = []
    for follower in followers:
        if follower.location:
            add = from_location(follower.location, gmaps)
            if add:
                search += add
    return search

def from_user(user, twitter, gmaps):
    if user.location:
        search = from_location(user.location, gmaps)
        if search:
            return search
    followers = [follower for follower in tweepy.Cursor(twitter.followers, id=user.id).items(10)]
    search = from_followers(followers, gmaps)
    return search
    
def from_status(status, twitter, gmaps):
    if status.coordinates:
        return from_coordinates(status.coordinates, gmaps)
    if status.place:
        return from_place(status.place, gmaps)
    if status.user:
        return from_user(status.user, twitter, gmaps)
    
def from_id(id, twitter, gmaps):
    status = twitter.get_status(id)
    return from_status(status, twitter, gmaps)