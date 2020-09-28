# A bot that tweets the most popular hashtags with the latest Reddit post titles.
# Want to show your support? Donate via PayPal or Bitcoin
# 1BHD7LQS9UkZvDXtoNjKrFMogJjPxz6aMj
# Have comments or questions? https://github.com/tg12


import csv
import time

import requests
import tweepy

# Main Constants
DB_FILE_NAME = "britishproblems.csv"
SUBREDDIT_NAME = "britishproblems"

# Twitter Credentials
CONSUMER_KEY = "<<<REMOVED>>>"
CONSUMER_SECRET = "<<<REMOVED>>>"
ACCESS_TOKEN = "<<<REMOVED>>>"
ACCESS_TOKEN_SECRET = "<<<REMOVED>>>"

AUTH = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
AUTH.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
USER = tweepy.API(AUTH)


def load_trends():
    """Returns a list of the trending topics that contain a hashtag and are ordered by most popular."""

    trends = USER.trends_place(2450022)
    temp_list = list()

    for trend in trends[0]["trends"]:

        if trend["tweet_volume"] is not None and " " not in trend["name"]:
            temp_list.append((trend["name"], trend["tweet_volume"]))

    temp_list.sort(key=lambda tup: tup[1], reverse=True)

    return [item[0] for item in temp_list]


def load_csv():
    """Loads the csv file and return a list of Reddit posts id's."""
    with open(DB_FILE_NAME, "r", newline="") as csv_contents:
        return [item[0] for item in csv.reader(csv_contents)]


def save_csv(post_id):
    """Updates the csv file with the processed Reddit post id."""
    with open(DB_FILE_NAME, "a", newline="") as csv_contents:
        csv_writer = csv.writer(csv_contents)
        csv_writer.writerow([post_id])


def load_latest_posts():
    """Loads the latest posts from the given subreddit."""

    url = "https://www.reddit.com/r/{0}/new/.json".format(SUBREDDIT_NAME)
    headers = {"User-Agent": "SimpleBot 0.1"}

    response = requests.get(url, headers=headers)

    for item in response.json()["data"]["children"]:
        post_id = item["data"]["id"]

        if post_id not in PROCESSED_POSTS:

            post_title = item["data"]["title"]
            post_url = "https://redd.it/" + item["data"]["id"]

            message = "{0} {1} {2}".format(
                post_title, " ".join(TRENDS_LIST), post_url)

            if len(message) <= 140:
                tweet_message(message, post_id)
                time.sleep(5)


def tweet_message(message, post_id):
    """Tweets the message composed by the title, hashtags and url."""
    USER.update_status(message)
    save_csv(post_id)
    print("Tweeted: {0}".format(message))


if __name__ == "__main__":
    PROCESSED_POSTS = load_csv()
    TRENDS_LIST = load_trends()
    load_latest_posts()
