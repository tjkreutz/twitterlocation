import config
import tweepy
import googlemaps

auth = tweepy.OAuthHandler(config.TWITTER_CONSUMER_KEY, config.TWITTER_CONSUMER_SECRET)
auth.set_access_token(config.TWITTER_ACCESS_TOKEN, config.TWITTER_ACCESS_TOKEN_SECRET)

twitter = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
gmaps = googlemaps.Client(key=config.GMAPS_ACCESS_TOKEN)

def get_address_component(search, level="country"):
    names = []
    for result in search:
        for component in result["address_components"]:
            if component["types"][0] == level and component["types"][1] == "political":
                names.append(component["long_name"])
    if not names:
        return "UNK"
    return max(set(names), key = names.count) 

def from_latlon(lat, lon):
    search = gmaps.reverse_geocode((lat, lon))
    return search

def from_coordinates(coordinates):
    lon, lat = status.coordinates['coordinates']
    search = from_latlon(lat, lon)
    return search

def from_place(place):
    bbox = status.place.bounding_box.coordinates
    lat = bbox[0][0][1]
    lon = bbox[0][0][0]
    search = from_latlon(lat, lon)
    return search

def from_user_location(user_location):
    search = gmaps.places(query=user_location)
    if search["status"] == "OK":
        result = search["results"][0]
        lat = result["geometry"]["location"]["lat"]
        lon = result["geometry"]["location"]["lng"]
        return from_latlon(lat, lon)

def from_followers(followers):
    search = []
    for follower in followers:
        if follower.location:
            add = from_user_location(follower.location)
            if add:
                search += add
    return search

def from_user(user):
    if user.location:
        search = from_user_location(user.location)
        if search:
            return search
    followers = [follower for follower in tweepy.Cursor(twitter.followers, id=user.id).items(10)]
    search = from_followers(followers)
    return search
    
def from_status(status):
    if status.coordinates:
        return from_coordinates(status.coordinates)
    if status.place:
        return from_place(status.place)
    if status.user:
        return from_user(status.user)
    
def main():
    example_status = twitter.search(q="example", count=1)[0]
    search = from_status(example_status)
    country = get_address_component(search, level="country")
    locality = get_address_component(search, level="locality")
    print(f"https://www.twitter.com/user/status/{example_status.id_str} from {locality}, {country}")

if __name__ == "__main__":
    main()