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
