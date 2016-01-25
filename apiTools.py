import tweepy
from tweepy import OAuthHandler

access_token = "3220384082-tbVafpAHKF2OMyv3m68cUa1xLfTmJ8Riz6bry6l"
access_token_secret = "Eb1LiineWIRngaOwju91tEV3cexAcJhvCoxW4dNJ5UQMu"
consumer_key = "Ghy8tbRezuJH0AtSL1qcPjqm8"
consumer_secret = "bURQpyYNU7ZbPbZVLiCagInnbM4yZvK9hAFlhToLoZ3XjOCqSy"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


def trends_us():
    result=api.trends_place(23424977)
    return result


def trends_global():
    result=api.trends_place(1)
    return result


def trends_sg():
    result=api.trends_place(23424948)
    return result