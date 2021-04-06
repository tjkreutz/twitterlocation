from twitterlocation import apis, guess

# Twitter keys
TWITTER_CONSUMER_KEY = ""
TWITTER_CONSUMER_SECRET = ""
TWITTER_ACCESS_TOKEN = ""
TWITTER_ACCESS_TOKEN_SECRET = ""

# Gmaps places + geolocate key
GMAPS_ACCESS_TOKEN = ""

# Connect to Twitter and Google services
twitter = apis.twitter_api(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
gmaps = apis.gmaps_api(GMAPS_ACCESS_TOKEN)

# Attempt to retrieve country of a tweet by id
example = guess.from_id("", twitter, gmaps)
country = guess.get_address_component(example, "country")
print(country)