#!/usr/bin/env python3
import json
import tweepy
import pytz
import settings
import time
import traceback

from CreateGraph import create_graph
from CreateImage import create_image
from datetime import datetime
from OpenAQAPI import API
import pprint

CONSUMER_KEY = settings.CONSUMER_KEY
CONSUMER_SECRET = settings.CONSUMER_SECRET
ACCESS_TOKEN = settings.ACCESS_TOKEN
ACCESS_TOKEN_SECRET = settings.ACCESS_TOKEN_SECRET
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
twitter = tweepy.API(auth)

last_accessed = datetime.now(tz=pytz.UTC)

while True:
    mentions = twitter.mentions_timeline(count=20)
    tmp_time = datetime.now(tz=pytz.UTC)
    for mention in mentions:
        twitter_data = json.dumps(mention._json)
        twitter_data = json.loads(twitter_data)
        # pprint.pprint(twitter_data)
        # print(twitter_data['user']['screen_name'])
        text = ''
        created = datetime.strptime(twitter_data['created_at'], '%a %b %d %H:%M:%S %z %Y')

        try:
            coordinates = twitter_data['coordinates']['coordinates']
            location = coordinates
        except:
            pass
        try:
            place = twitter_data['place']['bounding_box']['coordinates']
            place = [sum(x)/len(x) for x in zip(*place[0])]
            location = place
        except:
            location = None

        if created > last_accessed:
            try:
                location = str(location[1]) + ', ' + str(location[0])

                openaq = API()
                location = openaq.locations(coordinates=location,
                                            nearest=1,
                                            radius=100
                                            )

                week = openaq.measurements(location=location['results'][0]['location'], limit=1000)
                create_graph(location, week)
                # create_image(location['results'][0], created, week)

                twitter.update_with_media('tweet.png',
                                          status='@' + str(twitter_data['user']['screen_name']) + ' Oh my!')
                print('tweeted!')
            except Exception as e:
                print(e)
                traceback.print_exc()
                text = '@' + str(twitter_data['user']['screen_name']) + ' '
                text += "I can't find you :(, pls enable location"
                # twitter.update_status(text)
                print('Tweeted!')
        else:
            pass
    last_accessed = tmp_time
    time.sleep(15)
