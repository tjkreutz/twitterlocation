import config
import tweepy

auth = tweepy.OAuthHandler(config.TWITTER_CONSUMER_KEY, config.TWITTER_CONSUMER_SECRET)
auth.set_access_token(config.TWITTER_ACCESS_TOKEN, config.TWITTER_ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

def get_country_from_search(search):
    if search:
        first_result = search[0]
        return first_result.country
    return None

def guess_country(id):
    status = api.get_status(id)

    # see if the tweet has a geotag enabled
    if status.coordinates:
        lon, lat = status.coordinates['coordinates']
        search = api.geo_search(lon=lon, lat=lat, granularity="country")
        return get_country_from_search(search)
    # if not, see if the tweet has a location attached
    if status.place:
        bbox = status.place.bounding_box.coordinates
        lon, lat = bbox[0][0]
        search = api.geo_search(lon=lon, lat=lat, granularity="country")
        return get_country_from_search(search)
    # if not check if the user has a location attached
    if status.user:
        user = status.user
        if user.location:
            search = api.geo_search(query=user.location, granularity="country")
            return get_country_from_search(search)
        locations_vote = []
        # otherwise try to extract locations for their followers
        for follower in tweepy.Cursor(api.followers, id=user.id).items():
            if len(locations_vote) == 10:
                break
            if follower.location:
                search = api.geo_search(query=follower.location, granularity="country")
                locations_vote.append(get_country_from_search(search))

        return max(set(locations_vote), key = locations_vote.count)
    return None

if __name__ == "__main__":
    try:
        country = guess_country(1318879612194226176)
        print(country)
    except BaseException as e:
        print(f"Some Tweepy error: {e}")