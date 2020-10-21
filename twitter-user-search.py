'''THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, TITLE AND
NON-INFRINGEMENT. IN NO EVENT SHALL THE COPYRIGHT HOLDERS OR ANYONE
DISTRIBUTING THE SOFTWARE BE LIABLE FOR ANY DAMAGES OR OTHER LIABILITY,
WHETHER IN CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.'''

# Bitcoin Cash (BCH)   qpz32c4lg7x7lnk9jg6qg7s4uavdce89myax5v5nuk
# Ether (ETH) -        0x843d3DEC2A4705BD4f45F674F641cE2D0022c9FB
# Litecoin (LTC) -     Lfk5y4F7KZa9oRxpazETwjQnHszEPvqPvu
# Bitcoin (BTC) -      34L8qWiQyKr8k4TnHDacfjbaSqQASbBtTd

# contact :- github@jamessawyer.co.uk



#!/usr/bin/python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------
# twitter-user-search
#  - performs a search for users matching a certain query
# -----------------------------------------------------------------------
# Want to show your support? Donate via PayPal or Bitcoin
# 1BHD7LQS9UkZvDXtoNjKrFMogJjPxz6aMj
# Have comments or questions? https://github.com/tg12

import random
from twitter import *

word_file = "/usr/share/dict/words"
WORDS = open(word_file).read().splitlines()

random_word = random.choice(WORDS)

# -----------------------------------------------------------------------
# load our API credentials
# -----------------------------------------------------------------------
config = {}
execfile("config.py", config)

# -----------------------------------------------------------------------
# create twitter API object
# -----------------------------------------------------------------------
twitter = Twitter(auth=OAuth(
    config["access_key"],
    config["access_secret"],
    config["consumer_key"],
    config["consumer_secret"],
))

# -----------------------------------------------------------------------
# perform a user search
# twitter API docs: https://dev.twitter.com/rest/reference/get/users/search
# -----------------------------------------------------------------------

for x in range(0, 8):
    results = twitter.users.search(q=random_word)

    # -----------------------------------------------------------------------
    # loop through each of the users, and print their details
    # -----------------------------------------------------------------------
    for user in results:
        # print "@%s (%s): %s" % (user["screen_name"], user["name"], user["location"])
        open("/root/LearningPython/users.txt", "a+").write(
            str(user["name"]) + " " + "@" + user["screen_name"] + "\n")
        # new_status = "Hi" + " @" + user["screen_name"] + " How are you today?"
        # results = twitter.statuses.update(status = new_status)
        # print "updated status: %s" % new_status
