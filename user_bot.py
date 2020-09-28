# Want to show your support? Donate via PayPal or Bitcoin
# 1BHD7LQS9UkZvDXtoNjKrFMogJjPxz6aMj
# Have comments or questions? https://github.com/tg12

import sys
import tweepy
import random
import names
from twitter import *
from random import randint
from time import sleep

CONSUMER_KEY = "<<<REMOVED>>>"
CONSUMER_SECRET = "<<<REMOVED>>>"
ACCESS_TOKEN = "<<<REMOVED>>>"
ACCESS_TOKEN_SECRET = "<<<REMOVED>>>"

AUTH = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
AUTH.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
USER = tweepy.API(AUTH)

lines = open("/root/LearningPython/users.txt").read().splitlines()

for x in range(0, 3):
    user_info = random.choice(lines)
    firstname = names.get_first_name()
    # TEST - WORKING
    # USER.send_direct_message(screen_name="<<<REMOVED>>>", text="Test")
    # USER.send_direct_message(screen_name=screen_name_to, text="Hi, I'm looking for " + firstname + "?")
    screen_name_to = "@" + user_info.split("@", 1)[1]
    username = user_info.split("@", 1)[0]
    message = "Hello, " + screen_name_to + " Thanks for the interest " + username + "!"
    print message
    USER.update_status(message)
    print("Tweeted: {0}".format(message))
    sleep(randint(10, 100))
