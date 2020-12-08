# Twitterlocation.py

Tries to guess a country where are tweet originated. Reasonably accurate. Pseudo code:

1. Use coordinates of tweet if available
2. (else) Use tagged location of tweet if available
3. (else) Use user profile location if available
4. (else) Use location of up to ten followers if available

Make sure to install Tweepy, enter your own API keys in config.py, and catch exceptions when importing as a module.