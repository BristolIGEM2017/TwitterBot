#!/usr/bin/env python3
import json
import tweepy
import pytz
import settings
import time
from datetime import datetime
from OpenAQ import API
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
    for mention in mentions:
        twitter_data = json.dumps(mention._json)
        twitter_data = json.loads(twitter_data)
        # pprint.pprint(data)
        try:
            location = twitter_data['coordinates']['coordinates']
            created = datetime.strptime(twitter_data['created_at'], '%a %b %d %H:%M:%S %z %Y')
            if created > datetime.now(tz=pytz.UTC):
                location = str(location[1]) + ', ' + str(location[0])

                openaq = API()
                location = openaq.locations(coordinates=location,
                                            nearest=1,
                                            radius=100
                                            )
                data = openaq.latest(location=location['results'][0]['location'])

                text = '@' + twitter_data['user']['screen_name'] + ' '
                text += str(data['results'][0]['location']) + ' - '
                for measurement in data['results'][0]['measurements']:
                    text += str(measurement['parameter']) + ': '
                    text += str(measurement['value']) + ' '
                    text += str(measurement['unit']) + ', '

                twitter.update_status(text)
        except:
            print("User has not enabled geoservices")

        last_accessed = datetime.now(tz=pytz.UTC)

    time.sleep(15)
