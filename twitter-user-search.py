#!/usr/bin/python
# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------
# twitter-user-search
#  - performs a search for users matching a certain query
#-----------------------------------------------------------------------
#Want to show your support? Donate via PayPal or Bitcoin
#1BHD7LQS9UkZvDXtoNjKrFMogJjPxz6aMj
#Have comments or questions? https://github.com/tg12



import random
from twitter import *
word_file = "/usr/share/dict/words"
WORDS = open(word_file).read().splitlines()

random_word =  random.choice(WORDS)

#-----------------------------------------------------------------------
# load our API credentials 
#-----------------------------------------------------------------------
config = {}
execfile("config.py", config)

#-----------------------------------------------------------------------
# create twitter API object
#-----------------------------------------------------------------------
twitter = Twitter(
		auth = OAuth(config["access_key"], config["access_secret"], config["consumer_key"], config["consumer_secret"]))

#-----------------------------------------------------------------------
# perform a user search 
# twitter API docs: https://dev.twitter.com/rest/reference/get/users/search
#-----------------------------------------------------------------------

for x in range(0, 8):
	results = twitter.users.search(q = random_word)

#-----------------------------------------------------------------------
# loop through each of the users, and print their details
#-----------------------------------------------------------------------
	for user in results:
		#print "@%s (%s): %s" % (user["screen_name"], user["name"], user["location"])
		open('/root/LearningPython/users.txt', 'a+').write(str(user["name"]) + " " + "@" + user["screen_name"] + '\n')
		#new_status = "Hi" + " @" + user["screen_name"] + " How are you today?"
		#results = twitter.statuses.update(status = new_status)
		#print "updated status: %s" % new_status
