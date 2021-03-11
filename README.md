# twitterlocation.py

Guesses the country and locality of where a tweet originated. Todo: test accuracy. Pseudo code:

1. Use coordinates of tweet if available
2. (else) Use tagged location of tweet if available
3. (else) Use user profile location if available
4. (else) Use location of up to ten followers if available

Make sure to install Tweepy and googlemaps, enter your own API keys in config.py, and catch exceptions when importing as a module.
